#!/bin/bash
# Build script za gradnjo EXE za Windows na Linux/Mac sistemih

echo ""
echo "========================================"
echo "DAHUA Camera Discovery - Build Script"
echo "========================================"
echo ""

# Preveri ali je Python instaliran
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 ni instaliran!"
    echo "[*] Namesti Python3 preden nadaljuješ"
    exit 1
fi

echo "[+] Python je instaliran"
python3 --version
echo ""

# Preveri ali je PyInstaller instaliran
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo "[*] PyInstaller ni instaliran. Nameščam..."
    python3 -m pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "[-] Napaka pri nameščanju PyInstaller!"
        exit 1
    fi
fi

echo "[+] PyInstaller je instaliran"
echo ""

# Kreiraj dist folder
if [ -d "dist" ]; then
    echo "[*] Brišem staro dist mapo..."
    rm -rf dist
fi

if [ -d "build" ]; then
    echo "[*] Brišem staro build mapo..."
    rm -rf build
fi

echo ""
echo "[*] Gradim GUI verzijo..."
python3 -m PyInstaller \
    --onefile \
    --windowed \
    --name="DAHUA_Discovery" \
    --add-data "." \
    dahua_discovery_gui.py

if [ $? -ne 0 ]; then
    echo "[-] Napaka pri gradnji GUI verzije!"
    exit 1
fi

echo "[+] GUI verzija uspešno zgrajena!"
echo ""

echo "[*] Gradim CLI verzijo..."
python3 -m PyInstaller \
    --onefile \
    --console \
    --name="DAHUA_Discovery_CLI" \
    dahua_discovery.py

if [ $? -ne 0 ]; then
    echo "[-] Napaka pri gradnji CLI verzije!"
    exit 1
fi

echo "[+] CLI verzija uspešno zgrajena!"
echo ""

echo "========================================"
echo "[+] Gradnja zaključena!"
echo "========================================"
echo ""
echo "EXE datoteki so v folder 'dist':"
echo "  - DAHUA_Discovery (GUI verzija)"
echo "  - DAHUA_Discovery_CLI (CLI verzija)"
echo ""
