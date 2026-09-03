# DAHUA Camera Discovery Tool

Grafično in konzolno orodje za testiranje in odkrivanje DAHUA kamer v lokalni mreži.

## Značilnosti

- ✅ Grafični vmesnik (GUI) za enostavno uporabo
- ✅ Konzolna verzija (CLI) za avtomatizacijo
- ✅ Odkrivanje DAHUA kamer preko UDP
- ✅ Prikaz IP naslovov in portov odkritih kamer
- ✅ Shranjevanje rezultatov v JSON format
- ✅ Cross-platform podpora (Windows, Linux, macOS)
- ✅ Obsežno logiranje aktivnosti

## Zahteve

### Za poganjanje Python skript:
- Python 3.7 ali novejši
- Tkinter (navadno vključen v Python)
- Standardne Python biblioteke

### Za gradnjo EXE:
- PyInstaller: `pip install pyinstaller`

## Namestitev

### 1. Kloniraj repozitorij
```bash
git clone https://github.com/gregabahun/dahua-camera-discovery.git
cd dahua-camera-discovery
```

### 2. Namesti odvisnosti (opciono)
```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Uporaba

### GUI verzija (Grafični vmesnik)

#### Na Windows:
```bash
python dahua_discovery_gui.py
```

#### Na Linux/Mac:
```bash
python3 dahua_discovery_gui.py
```

### CLI verzija (Konzola)

#### Na Windows:
```bash
python dahua_discovery.py
```

#### Na Linux/Mac:
```bash
python3 dahua_discovery.py
```

## Gradnja EXE za Windows

### Avtomatska gradnja:

#### Na Windows (PowerShell ali CMD):
```bash
build.bat
```

#### Na Linux/Mac:
```bash
bash build.sh
```

### Ročna gradnja:

#### GUI verzija:
```bash
pyinstaller --onefile --windowed --name="DAHUA_Discovery" dahua_discovery_gui.py
```

#### CLI verzija:
```bash
pyinstaller --onefile --console --name="DAHUA_Discovery_CLI" dahua_discovery.py
```

Gradljene EXE datoteke se nahajajo v `dist/` mapi.

## Kako deluje?

1. Program pošlje UDP paket na broadcast naslov (privzeto `255.255.255.255`)
2. DAHUA kamere prejmejo paket in pošljejo odgovor
3. Program zbira odgovore v določenem času (privzeto 5 sekund)
4. Prikaže seznam najdenih kamer z IP naslovom in portom
5. Rezultate shrani v JSON datoteko

## Nastavitve

### Broadcast naslov
- Privzeto: `255.255.255.255`
- Možno je tudi specifičiti subnet broadcast naslov, npr. `192.168.1.255`

### Timeout
- Privzeto: 5 sekund
- Razpon: 1-60 sekund
- Daljši timeout omogoča odkrivanje počasnejših kamer

## Rezultati

Rezultati se samodejno shranijo v JSON datoteko z imenom:
```
dahua_cameras_YYYYMMDD_HHMMSS.json
```

Primer vsebine:
```json
[
  {
    "ip": "192.168.1.100",
    "port": 37810,
    "timestamp": "2026-09-03 10:30:45",
    "status": "Aktivna"
  }
]
```

## Zaslonske slike

### GUI Verzija
- Nastavitve za broadcast in timeout
- Tabela z najdenimi kamerama
- Real-time log aktivnosti
- Statistika odkritih kamer
- Možnost shranjevanja rezultatov

## Varnost

⚠️ **Opozorilo**: To orodje je namenjeno samo za testiranje in diagnostiko v kontroliranem omrežnem okolju.

- Uporabi samo v privatnih omrežjih, ki ti pripadajo
- Ne uporabljaj za nepooblaščeno dostopanje do omrežij
- Spoštuj lokalne zakone in politike varnosti

## Rešavanje problemov

### Nobena kamera ni bila najdena
- Preveri ali so kamere priključene na isto omrežje
- Poskusi spremeniti broadcast naslov na subnet broadcast naslov
- Povečaj timeout na 10-15 sekund
- Preveri firewall nastavitve

### "Address already in use" napaka
- Port 37810 je že v uporabi
- Zaustavi druge programe, ki uporabljajo ta port
- Počakaj nekaj sekund in poskusi ponovno

### GUI ne odpre
- Preveri ali je Tkinter instaliran: `python -m tkinter`
- Na Linux sistemih moraš namestititi: `sudo apt-get install python3-tk`

## Licenca

MIT License - Prosto za uporabo in spreminjanje

## Prispevki

Dobrodošli so vsi prispevki! Kreiraj pull request z izboljšavami.

## Kontakt

Avtor: gregabahun
GitHub: https://github.com/gregabahun/dahua-camera-discovery

## Zahvale

- DAHUA za dokumentacijo o UDP discovery protokolu
- Python zajednici za odličnih orodja

---

**Verzija**: 1.0.0  
**Zadnja posodobitev**: 2026-09-03
