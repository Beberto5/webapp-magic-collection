from fastapi import FastAPI, Request, Depends, Query, Form, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select, func
from typing import Optional
import csv
import io

from database import create_db, get_session
from models import Card, CollectionEntry
from scryfall import get_sets, get_cards_by_set, get_cards_by_set_lang, parse_card

app = FastAPI(title="Magic Collection")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    create_db()


# ── HELPERS ───────────────────────────────────────────────────────────────────

def get_lang(site_lang: Optional[str] = Cookie(default="en")) -> str:
    return "it" if site_lang == "it" else "en"


def _apply_filters(query, set_code, color, rarity, name, sort, lang):
    if set_code:
        query = query.where(Card.set_code == set_code)
    if color:
        query = query.where(Card.color_identity.contains(color))
    if rarity:
        query = query.where(Card.rarity == rarity)
    if name:
        if lang == "it":
            query = query.where(
                ((Card.name_it != None) & Card.name_it.contains(name)) |
                Card.name.contains(name)
            )
        else:
            query = query.where(Card.name.contains(name))
    if sort == "name":
        query = query.order_by(Card.name)
    elif sort == "cmc":
        query = query.order_by(Card.cmc, Card.name)
    elif sort == "rarity":
        query = query.order_by(Card.rarity, Card.name)
    else:
        query = query.order_by(Card.set_code, Card.collector_number)
    return query


def _owned_map(session: Session) -> dict:
    entries = session.exec(select(CollectionEntry)).all()
    return {e.card_scryfall_id: e.quantity for e in entries}


def _stats(session: Session, set_code: Optional[str] = None):
    q_total = select(func.count(Card.id))
    q_owned = select(func.count(CollectionEntry.id))
    if set_code:
        q_total = q_total.where(Card.set_code == set_code)
        q_owned = (q_owned
                   .join(Card, Card.scryfall_id == CollectionEntry.card_scryfall_id)
                   .where(Card.set_code == set_code))
    return session.exec(q_total).one(), session.exec(q_owned).one()


# ── SET LINGUA (cookie server-side, poi redirect) ─────────────────────────────

@app.get("/set-lang/{lang}")
def set_lang(lang: str, request: Request):
    """Imposta il cookie lingua lato server e torna alla pagina precedente."""
    lang = "it" if lang == "it" else "en"
    referer = request.headers.get("referer", "/")
    response = RedirectResponse(url=referer, status_code=303)
    response.set_cookie("site_lang", lang, max_age=60 * 60 * 24 * 365, path="/")
    return response


# ── PAGINE PRINCIPALI ─────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
    page: int = Query(1, ge=1),
    q: Optional[str] = Query(None),
):
    PAGE_SIZE = 24
    all_sets = await get_sets()

    if q:
        all_sets = [s for s in all_sets if q.lower() in s["name"].lower()]

    total_sets = len(all_sets)
    total_pages = max(1, -(-total_sets // PAGE_SIZE))
    page = min(page, total_pages)
    sets_page = all_sets[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]

    imported = session.exec(select(Card.set_code).distinct()).all()
    total, owned = _stats(session)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "sets": sets_page,
        "imported_sets": set(imported),
        "total_cards": total,
        "owned_cards": owned,
        "site_lang": lang,
        "page": page,
        "total_pages": total_pages,
        "total_sets": total_sets,
        "q": q or "",
    })


@app.get("/collection", response_class=HTMLResponse)
async def collection(
    request: Request,
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
    set_code: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    rarity: Optional[str] = Query(None),
    owned: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    sort: str = Query("collector"),
):
    query = _apply_filters(select(Card), set_code, color, rarity, name, sort, lang)
    cards = session.exec(query).all()
    owned_map = _owned_map(session)

    if owned == "yes":
        cards = [c for c in cards if c.scryfall_id in owned_map]
    elif owned == "no":
        cards = [c for c in cards if c.scryfall_id not in owned_map]

    set_codes = session.exec(select(Card.set_code, Card.set_name).distinct()).all()
    total, owned_count = _stats(session, set_code)

    return templates.TemplateResponse("collection.html", {
        "request": request,
        "cards": cards,
        "owned_map": owned_map,
        "set_codes": set_codes,
        "total_cards": total,
        "owned_cards": owned_count,
        "site_lang": lang,
        "filters": {
            "set_code": set_code, "color": color, "rarity": rarity,
            "owned": owned, "name": name, "sort": sort,
        },
    })


@app.get("/stats", response_class=HTMLResponse)
async def stats(
    request: Request,
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
):
    # Statistiche per espansione
    all_cards = session.exec(select(Card)).all()
    owned_map = _owned_map(session)

    sets_data: dict[str, dict] = {}
    for card in all_cards:
        key = card.set_code
        if key not in sets_data:
            sets_data[key] = {
                "set_name": card.set_name,
                "set_code": card.set_code,
                "total": 0, "owned": 0,
                "by_rarity": {
                    "mythic":   {"total": 0, "owned": 0},
                    "rare":     {"total": 0, "owned": 0},
                    "uncommon": {"total": 0, "owned": 0},
                    "common":   {"total": 0, "owned": 0},
                }
            }
        sets_data[key]["total"] += 1
        if card.scryfall_id in owned_map:
            sets_data[key]["owned"] += 1
        r = card.rarity if card.rarity in sets_data[key]["by_rarity"] else "common"
        sets_data[key]["by_rarity"][r]["total"] += 1
        if card.scryfall_id in owned_map:
            sets_data[key]["by_rarity"][r]["owned"] += 1

    # Ordina per % completamento decrescente
    sets_list = sorted(
        sets_data.values(),
        key=lambda x: x["owned"] / x["total"] if x["total"] else 0,
        reverse=True
    )

    total_cards = sum(s["total"] for s in sets_list)
    total_owned = sum(s["owned"] for s in sets_list)

    return templates.TemplateResponse("stats.html", {
        "request": request,
        "sets_list": sets_list,
        "total_cards": total_cards,
        "owned_cards": total_owned,
        "site_lang": lang,
    })


# ── HTMX: griglia carte ───────────────────────────────────────────────────────

@app.get("/cards/grid", response_class=HTMLResponse)
async def card_grid(
    request: Request,
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
    set_code: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    rarity: Optional[str] = Query(None),
    owned: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    sort: str = Query("collector"),
):
    query = _apply_filters(select(Card), set_code, color, rarity, name, sort, lang)
    cards = session.exec(query).all()
    owned_map = _owned_map(session)

    if owned == "yes":
        cards = [c for c in cards if c.scryfall_id in owned_map]
    elif owned == "no":
        cards = [c for c in cards if c.scryfall_id not in owned_map]

    total, owned_count = _stats(session, set_code)

    return templates.TemplateResponse("card_grid.html", {
        "request": request,
        "cards": cards,
        "owned_map": owned_map,
        "lang": lang,
        "site_lang": lang,
        "total_cards": total,
        "owned_cards": owned_count,
    })


# ── IMPORT ────────────────────────────────────────────────────────────────────

@app.post("/import/{set_code}", response_class=HTMLResponse)
async def import_set(
    set_code: str,
    request: Request,
    session: Session = Depends(get_session),
):
    en_cards = await get_cards_by_set(set_code)
    it_cards_by_oracle = await get_cards_by_set_lang(set_code, "it")

    imported = 0
    for raw in en_cards:
        oracle_id = raw.get("oracle_id", "")
        it_card = it_cards_by_oracle.get(oracle_id)
        parsed = parse_card(raw, it_card)
        if not parsed:
            continue
        existing = session.exec(
            select(Card).where(Card.scryfall_id == parsed["scryfall_id"])
        ).first()
        if not existing:
            session.add(Card(**parsed))
            imported += 1
    session.commit()
    it_count = sum(
        1 for c in session.exec(select(Card).where(Card.set_code == set_code)).all()
        if c.image_uri_it
    )
    return HTMLResponse(
        f'<span class="badge-ok">✓ {imported} carte importate'
        f'{f" ({it_count} con img IT)" if it_count else ""}</span>'
    )


# ── ESPORTAZIONE CSV ──────────────────────────────────────────────────────────

@app.get("/export/csv")
def export_csv(session: Session = Depends(get_session)):
    cards = session.exec(select(Card)).all()
    owned_map = _owned_map(session)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "name", "name_it", "set_code", "set_name", "collector_number",
        "rarity", "type_line", "mana_cost", "cmc",
        "colors", "color_identity", "quantity"
    ])
    for card in sorted(cards, key=lambda c: (c.set_code, c.collector_number)):
        qty = owned_map.get(card.scryfall_id, 0)
        writer.writerow([
            card.name, card.name_it or "", card.set_code, card.set_name,
            card.collector_number, card.rarity, card.type_line,
            card.mana_cost or "", card.cmc or 0,
            card.colors or "", card.color_identity or "", qty
        ])

    content = output.getvalue()
    return HTMLResponse(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=magic_collection.csv"}
    )


# ── COLLEZIONE UPDATE ─────────────────────────────────────────────────────────

@app.post("/collection/update", response_class=HTMLResponse)
async def update_collection(
    scryfall_id: str = Form(...),
    quantity: int = Form(...),
    session: Session = Depends(get_session),
):
    entry = session.exec(
        select(CollectionEntry).where(CollectionEntry.card_scryfall_id == scryfall_id)
    ).first()

    if quantity <= 0:
        if entry:
            session.delete(entry)
            session.commit()
        return HTMLResponse(_qty_html(scryfall_id, 0))

    if entry:
        entry.quantity = quantity
    else:
        entry = CollectionEntry(card_scryfall_id=scryfall_id, quantity=quantity)
        session.add(entry)
    session.commit()
    return HTMLResponse(_qty_html(scryfall_id, quantity))


def _qty_html(scryfall_id: str, qty: int) -> str:
    owned_class = "owned" if qty > 0 else ""
    return f"""
    <div class="qty-control {owned_class}" id="qty-{scryfall_id}">
        <form hx-post="/collection/update" hx-target="#qty-{scryfall_id}" hx-swap="outerHTML">
            <input type="hidden" name="scryfall_id" value="{scryfall_id}">
            <button type="submit" name="quantity" value="{max(0, qty-1)}" class="qty-btn">−</button>
            <span class="qty-value">{qty}</span>
            <button type="submit" name="quantity" value="{qty+1}" class="qty-btn">+</button>
        </form>
    </div>
    """