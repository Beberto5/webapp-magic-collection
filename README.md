# Magic Collection

App web locale per gestire la tua collezione di carte Magic: The Gathering.  
Dati e immagini scaricati automaticamente da [Scryfall](https://scryfall.com) (gratuito, nessuna API key richiesta).

---

## Stack tecnico

| Layer | Tecnologia |
|---|---|
| Backend | Python 3.12 + FastAPI |
| Database | SQLite (file locale `magic_collection.db`) |
| Frontend | Jinja2 + HTMX + CSS puro |
| Dati carte | Scryfall API (pubblica) |

---

## Requisiti

- Python 3.10 o superiore
- Connessione internet (solo per importare le espansioni da Scryfall)

---

## Avvio rapido

```bash
# Clona o scarica il progetto, poi entra nella cartella
cd magic-collection

# Rendi eseguibile lo script (solo la prima volta)
chmod +x start.sh

# Avvia
./start.sh
```

Lo script si occupa automaticamente di:
- creare il virtual environment Python se non esiste
- installare tutte le dipendenze
- avviare il server sulla porta 8000

Apri il browser su **http://localhost:8000**

---

## Struttura del progetto

```
magic-collection/
├── main.py          # App FastAPI — route e logica
├── models.py        # Modelli database (Card, CollectionEntry)
├── database.py      # Configurazione SQLite
├── scryfall.py      # Client API Scryfall
├── templates/
│   ├── base.html        # Layout base (navbar, stile globale)
│   ├── index.html       # Pagina espansioni
│   ├── collection.html  # Pagina collezione con filtri
│   └── card_grid.html   # Griglia carte (partial HTMX)
├── static/          # CSS e JS aggiuntivi (attualmente vuoto)
├── start.sh         # Script di avvio
├── magic_collection.db  # Database SQLite (generato al primo avvio)
└── README.md
```

---

## Utilizzo

### 1. Importare un'espansione

Vai sulla pagina **Espansioni** (pagina iniziale).  
Clicca **Importa** accanto all'espansione che ti interessa.  
Le carte vengono scaricate da Scryfall con immagini in inglese e, dove disponibili, in italiano.  
L'importazione richiede qualche secondo a seconda della dimensione del set.

### 2. Gestire la collezione

Vai sulla pagina **Collezione**.  
Usa i bottoni `+` e `−` su ogni carta per aggiornare quante copie possiedi.  
Le carte possedute vengono evidenziate con un bordo verde.

### 3. Filtri disponibili

- **Espansione** — filtra per set importato
- **Colore** — bianco, blu, nero, rosso, verde
- **Rarità** — common, uncommon, rare, mythic
- **Possesso** — tutte / solo possedute / solo non possedute
- **Ordina per** — numero collezionatore, nome, costo mana, rarità
- **Nome** — ricerca testuale (funziona anche con il nome italiano)

### 4. Lingua immagini

Il toggle **🇬🇧 EN / 🇮🇹 IT** in alto a destra nella navbar cambia la lingua delle immagini delle carte per tutto il sito. La preferenza viene salvata e ricordata tra le sessioni.  
Nota: non tutte le espansioni sono disponibili in italiano su Scryfall.

### 5. Popup carta

Clicca su qualsiasi carta per vederla ingrandita con nome, espansione, rarità, costo mana e testo oracle.  
Chiudi con il tasto **Esc**, il pulsante ✕ o cliccando fuori dal popup.

---

## Note tecniche

- Il database SQLite viene creato automaticamente nella cartella del progetto al primo avvio.
- Scryfall impone un rate limit di 10 richieste/secondo: le importazioni rispettano questo limite automaticamente.
- Se rimuovi il file `.db` e reimporti, le espansioni vengono riscaricate da zero da Scryfall.
- Il campo `image_uri_it` può essere `null` per le carte di espansioni non tradotte in italiano: in quel caso viene mostrata automaticamente l'immagine inglese.

---

## Prossimi sviluppi previsti

- [ ] Supporto carte foil
- [ ] Esportazione collezione (CSV / JSON)
- [ ] Statistiche collezione (valore, completamento per set)
- [ ] Ricerca avanzata (tipo, sottotipo, testo oracle)
- [ ] Docker per deploy su altri dispositivi della rete locale