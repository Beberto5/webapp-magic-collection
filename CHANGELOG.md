# Changelog

Tutte le modifiche significative a questo progetto sono documentate qui.

Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
il versionamento segue [Semantic Versioning](https://semver.org/lang/it/).

> **Guida rapida al versionamento:**
> - `PATCH` (0.0.x) — bugfix, ritocchi estetici, testi
> - `MINOR` (0.x.0) — nuova funzionalità retrocompatibile
> - `MAJOR` (x.0.0) — cambiamento architetturale o breaking change

---

## [Unreleased]

Funzionalità in pianificazione o in sviluppo attivo.

### Planned
- Stampa PDF carte a grandezza naturale (proxy printing) — sia dal Deck Builder che da pagina dedicata
- Salvataggio mazzi nel database
- Sideboard nel Deck Builder con drag & drop main ↔ side
- Ricerca avanzata per sottotipo e testo oracle
- Esportazione in altri formati (JSON, Moxfield, Archidekt)
- Statistiche valore stimato collezione
- Supporto carte foil
- Docker per deploy in rete locale

---

## [0.3.0] — 2026-03-13

### Added
- **Deck Builder** (`/deck-builder`) — nuova pagina per la costruzione di mazzi
  - Selezione formato tra 12 opzioni: Standard, Pioneer, Modern, Legacy, Vintage, Historic, Alchemy, Explorer, Brawl, Historic Brawl, Commander, Pauper
  - Validazione automatica delle regole per ciascun formato (numero minimo carte, copie massime, sideboard)
  - Toggle "Arena only" per filtrare le carte disponibili su Magic Arena
  - Filtri: ricerca per nome, colore, rarità, tipo carta, solo possedute/non
  - Raggruppamento automatico in sezioni Maindeck / Terre / Sideboard
  - Contatore di validità live nella sidebar
  - Export `.txt` compatibile con Magic Arena (`Decks → Import`)
  - Zoom carta su tasto destro
  - Toast notifications per feedback immediato
- Voce **Deck Builder** aggiunta alla navbar in `base.html`
- Route `GET /deck-builder` in `main.py`

### Changed
- `README.md` ristrutturato: contenuto orientato all'utente finale, roadmap spostata nel `CHANGELOG.md`

---

## [0.2.0] — 2026-03-13

### Added
- **Simboli mana visivi** — integrazione [Mana Font](https://mana.andrewgioia.com/) (CDN jsDelivr)
  - Pip colore nel Deck Builder ora mostrano i simboli mana ufficiali (`ms-w`, `ms-u`, `ms-b`, `ms-r`, `ms-g`, `ms-c`) invece di lettere su sfondo colorato
  - Filtro colore in `collection.html` aggiornato con pip visivi; la `<select>` originale rimane hidden per mantenere la compatibilità con HTMX
  - Aggiunto link CDN in `base.html` `<head>` per disponibilità globale

### Technical
- I simboli mana sono © Wizards of the Coast; l'uso tramite Mana Font è conforme alle pratiche della community per progetti non commerciali (font SIL OFL, CSS MIT)

---

## [0.1.0] — 2026-03-13

Versione iniziale del progetto.

### Added
- **Pagina Espansioni** (`/`) — sfoglia tutti i set da Scryfall con paginazione e ricerca; importa con un click
- **Pagina Collezione** (`/collection`) — griglia carte con filtri (espansione, colore, rarità, possesso, ordinamento, nome); aggiornamento quantità con HTMX senza refresh
- **Pagina Statistiche** (`/stats`) — completamento globale e per espansione con barra di progresso e breakdown per rarità (M/R/U/C)
- **Export CSV** (`/export/csv`) — scarica l'intera collezione come file `.csv`
- Supporto immagini bilingue EN/IT con toggle in navbar, preferenza salvata come cookie
- Popup zoom carta con tasto ESC e click outside per chiudere
- Import dati da Scryfall API: carte EN + versioni IT dove disponibili (oracle_id come chiave di collegamento)
- Struttura database SQLite con `Card` e `CollectionEntry` via SQLModel
- Script `start.sh` per avvio automatico con virtualenv
- `base.html` con layout sticky navbar, design dark fantasy con CSS custom properties

### Technical stack
- FastAPI 0.111 + Uvicorn 0.29
- SQLModel 0.0.18 + SQLite
- Jinja2 3.1.4 + HTMX 1.9.12
- httpx 0.27 per chiamate async a Scryfall

---

[Unreleased]: https://github.com/TUO_USERNAME/magic-collection/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/TUO_USERNAME/magic-collection/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/TUO_USERNAME/magic-collection/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/TUO_USERNAME/magic-collection/releases/tag/v0.1.0