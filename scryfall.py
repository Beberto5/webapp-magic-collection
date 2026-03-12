import httpx
from typing import Optional

SCRYFALL_BASE = "https://api.scryfall.com"


async def get_sets() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SCRYFALL_BASE}/sets")
        response.raise_for_status()
        data = response.json()
        sets = [
            s for s in data["data"]
            if s["set_type"] in ("expansion", "core", "draft_innovation", "masters", "commander")
        ]
        return sorted(sets, key=lambda x: x["released_at"], reverse=True)


async def get_cards_by_set(set_code: str) -> list[dict]:
    """Scarica tutte le carte EN di un'espansione."""
    cards = []
    url = f"{SCRYFALL_BASE}/cards/search?q=set:{set_code}&unique=prints&order=collector_number"
    async with httpx.AsyncClient(timeout=60.0) as client:
        while url:
            response = await client.get(url)
            if response.status_code == 404:
                break
            response.raise_for_status()
            data = response.json()
            cards.extend(data.get("data", []))
            url = data.get("next_page")
    return cards


async def get_cards_by_set_lang(set_code: str, lang: str = "it") -> dict[str, dict]:
    """
    Scarica le carte in una lingua specifica e restituisce
    un dict { scryfall_id_originale: card_data_localizzata }.
    Scryfall usa l'id della stampa originale EN nel campo 'prints_search_uri'.
    Usiamo 'oracle_id' come chiave di collegamento.
    """
    cards_by_oracle: dict[str, dict] = {}
    url = (
        f"{SCRYFALL_BASE}/cards/search"
        f"?q=set:{set_code}+lang:{lang}&unique=prints&order=collector_number"
    )
    async with httpx.AsyncClient(timeout=60.0) as client:
        while url:
            response = await client.get(url)
            if response.status_code in (404, 422):
                break
            response.raise_for_status()
            data = response.json()
            for card in data.get("data", []):
                oracle_id = card.get("oracle_id", "")
                if oracle_id:
                    cards_by_oracle[oracle_id] = card
            url = data.get("next_page")
    return cards_by_oracle


def _extract_images(card_data: dict) -> dict:
    image_uris = card_data.get("image_uris", {})
    if not image_uris and "card_faces" in card_data:
        image_uris = card_data["card_faces"][0].get("image_uris", {})
    return image_uris


def parse_card(en_card: dict, it_card: Optional[dict] = None) -> Optional[dict]:
    """Costruisce il dict da salvare nel DB, con dati EN + opzionalmente IT."""
    en_images = _extract_images(en_card)
    it_images = _extract_images(it_card) if it_card else {}

    colors = en_card.get("colors", [])
    color_identity = en_card.get("color_identity", [])

    return {
        "scryfall_id":      en_card["id"],
        "name":             en_card.get("name", ""),
        "name_it":          it_card.get("printed_name") if it_card else None,
        "set_code":         en_card.get("set", ""),
        "set_name":         en_card.get("set_name", ""),
        "collector_number": en_card.get("collector_number", ""),
        "rarity":           en_card.get("rarity", ""),
        "type_line":        en_card.get("type_line", ""),
        "mana_cost":        en_card.get("mana_cost", ""),
        "cmc":              en_card.get("cmc", 0),
        "colors":           ",".join(colors) if colors else "",
        "color_identity":   ",".join(color_identity) if color_identity else "",
        "image_uri":        en_images.get("normal", ""),
        "image_uri_small":  en_images.get("small", ""),
        "image_uri_it":     it_images.get("normal", "") or None,
        "image_uri_small_it": it_images.get("small", "") or None,
        "oracle_text":      en_card.get("oracle_text", ""),
    }
