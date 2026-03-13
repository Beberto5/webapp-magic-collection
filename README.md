# Magic Collection

App web locale per gestire la tua collezione di carte **Magic: The Gathering**.  
Dati e immagini scaricati automaticamente da [Scryfall](https://scryfall.com) — gratuito, nessuna API key richiesta.

> Progetto personale / portfolio. Non affiliato con Wizards of the Coast o Scryfall.

---

## Screenshot

_Coming soon_

---

## Stack tecnico

| Layer | Tecnologia |
|---|---|
| Backend | Python 3.10+ · [FastAPI](https://fastapi.tiangolo.com) |
| Database | SQLite via [SQLModel](https://sqlmodel.tiangolo.com) |
| Frontend | [Jinja2](https://jinja.palletsprojects.com) · [HTMX](https://htmx.org) · CSS puro |
| Dati carte | [Scryfall API](https://scryfall.com/docs/api) |

Nessun build system, nessun npm, nessun webpack. Il frontend è HTML server-rendered con aggiornamenti parziali via HTMX.

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

Lo script crea automaticamente il virtual environment, installa le dipendenze e avvia il server.

Apri il browser su **http://localhost:8000**

### Avvio manuale (alternativa)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Struttura del progetto

```
magic-collection/
├── main.py              # App FastAPI — route e logica
├── models.py            # Modelli database (Card, CollectionEntry)
├── database.py          # Configurazione SQLite
├── scryfall.py          # Client API Scryfall
├── templates/
│   ├── base.html        # Layout base (navbar, stile globale)
│   ├── index.html       # Pagina espansioni
│   ├── collection.html  # Pagina collezione con filtri
│   ├── card_grid.html   # Griglia carte (partial HTMX)
│   └── stats.html       # Pagina statistiche
├── static/              # Asset statici (attualmente vuoto)
├── requirements.txt     # Dipendenze Python con versioni fisse
├── start.sh             # Script di avvio
├── .gitignore
├── CREDITS.md           # Licenze e attribuzioni
└── README.md
```

Il file `magic_collection.db` viene creato automaticamente al primo avvio e **non è versionato** — ogni utente costruisce la propria collezione.

---

## Funzionalità

### Importare un'espansione
Dalla pagina **Espansioni**, clicca _Importa_ accanto al set che ti interessa.  
Le carte vengono scaricate da Scryfall con immagini in inglese e, dove disponibili, in italiano.

### Gestire la collezione
Dalla pagina **Collezione**, usa `+` e `−` su ogni carta per aggiornare le copie possedute.  
Le carte possedute vengono evidenziate con un bordo verde.

### Filtri disponibili
- Espansione, colore, rarità, possesso
- Ordinamento per numero collezionatore, nome, costo mana, rarità
- Ricerca per nome (funziona anche con il nome italiano)

### Lingua immagini
Il toggle **🇬🇧 EN / 🇮🇹 IT** in navbar cambia la lingua delle immagini per tutto il sito.  
La preferenza viene salvata come cookie. Non tutte le espansioni sono disponibili in italiano su Scryfall.

### Statistiche ed esportazione
La pagina **Statistiche** mostra il completamento globale e per espansione, con breakdown per rarità.  
Il bottone **Esporta CSV** scarica l'intera collezione come file `.csv`.

### Popup carta
Clicca su qualsiasi carta per vederla ingrandita con nome, rarità, costo mana e testo oracle.  
Chiudi con `Esc`, il tasto ✕ o cliccando fuori.

---

## Note tecniche

- Il database SQLite viene creato nella cartella del progetto al primo avvio.
- Scryfall richiede max 10 request/secondo: le importazioni rispettano questo limite.
- Reimportare un set già presente non crea duplicati.
- Se rimuovi il `.db` e reimporti, le espansioni vengono riscaricate da zero.

---

## Roadmap

- [ ] Supporto carte foil
- [ ] Ricerca avanzata (tipo, sottotipo, testo oracle)
- [ ] Docker per deploy in rete locale
- [ ] Esportazione in altri formati (JSON, Moxfield)
- [ ] Statistiche valore stimato collezione

---

## Licenze e crediti

Vedi [CREDITS.md](./CREDITS.md) per il dettaglio completo di licenze e attribuzioni.

Le carte Magic: The Gathering sono © Wizards of the Coast.  
Dati e immagini forniti da [Scryfall](https://scryfall.com).