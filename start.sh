#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo ">>> Creazione virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo ">>> Verifica dipendenze..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║        Magic Collection — avvio           ║"
echo "║  Apri il browser su http://localhost:8000  ║"
echo "║  Premi Ctrl+C per fermare                 ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload