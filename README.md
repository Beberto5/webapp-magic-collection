# Magic Collection

App web locale per gestire la tua collezione di carte **Magic: The Gathering**.  
Dati e immagini scaricati automaticamente da [Scryfall](https://scryfall.com) — gratuito, nessuna API key richiesta.

> Progetto personale / portfolio. Non affiliato con Wizards of the Coast o Scryfall.

---

## Stack tecnico

| Layer | Tecnologia |
|---|---|
| Backend | Python 3.10+ · [FastAPI](https://fastapi.tiangolo.com) |
| Database | SQLite via [SQLModel](https://sqlmodel.tiangolo.com) |
| Frontend | [Jinja2](https://jinja.palletsprojects.com) · [HTMX](https://htmx.org) · CSS puro |
| Simboli mana | [Mana Font](https://mana.andrewgioia.com/) (MIT / SIL OFL) |
| Dati carte | [Scryfall API](https://scryfall.com/docs/api) |

---

## Requisiti

- Python 3.10 o superiore
- Connessione internet (solo per importare espansioni da Scryfall)

---

## Avvio rapido

```bash
git clone https://github.com/TUO_USERNAME/magic-collection.git
cd magic-collection
chmod +x start.sh
./start.sh
```

Apri il browser su **http://localhost:8000**

### Avvio manuale

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Funzionalità

| Pagina | Descrizione |
|---|---|
| **Espansioni** | Sfoglia e importa espansioni da Scryfall (EN + IT dove disponibile) |
| **Collezione** | Gestisci le copie possedute, filtra per colore, rarità, tipo, nome |
| **Statistiche** | Completamento globale e per espansione con breakdown per rarità, esporta CSV |
| **Deck Builder** | Costruisci mazzi per qualsiasi formato, esporta `.txt` per Magic Arena |

### Note operative

- Il database `magic_collection.db` viene creato automaticamente al primo avvio e non è versionato.
- Reimportare un set già presente non crea duplicati.
- Il toggle **🇬🇧 EN / 🇮🇹 IT** in navbar cambia la lingua delle immagini; la preferenza è salvata come cookie.
- Nel Deck Builder, tasto destro su una carta per vederla ingrandita.

---

## Struttura del progetto

```
magic-collection/
├── main.py                 # App FastAPI — route e logica
├── models.py               # Modelli database (Card, CollectionEntry)
├── database.py             # Configurazione SQLite
├── scryfall.py             # Client API Scryfall
├── templates/
│   ├── base.html           # Layout base (navbar, stile globale)
│   ├── index.html          # Pagina espansioni
│   ├── collection.html     # Pagina collezione con filtri
│   ├── card_grid.html      # Griglia carte (partial HTMX)
│   ├── stats.html          # Pagina statistiche
│   └── deck_builder.html   # Costruttore mazzi
├── static/
├── requirements.txt
├── start.sh
├── CHANGELOG.md            # Storico delle modifiche per versione
└── CREDITS.md
```

---

## Licenze e crediti

Vedi [CREDITS.md](./CREDITS.md).  
Le carte Magic: The Gathering sono © Wizards of the Coast.  
Dati e immagini forniti da [Scryfall](https://scryfall.com).