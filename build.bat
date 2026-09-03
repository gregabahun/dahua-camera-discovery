@echo off
REM Build script za gradnjo EXE za Windows
REM Zahtevani paketi: PyInstaller

echo.
echo ========================================
echo DAHUA Camera Discovery - Build Script
echo ========================================
echo.

REM Preveri ali je Python instaliran
python --version >nul 2>&1
if errorlevel 1 (
    echo [-] Python ni instaliran!
    echo [*] Prenesi Python z https://www.python.org/
    pause
    exit /b 1
)

echo [+] Python je instaliran
echo.

REM Preveri ali je PyInstaller instaliran
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [*] PyInstaller ni instaliran. Nameščam...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo [-] Napaka pri nameščanju PyInstaller!
        pause
        exit /b 1
    )
)

echo [+] PyInstaller je instaliran
echo.

REM Kreiraj dist folder
if exist "dist" (
    echo [*] Brišem staro dist mapo...
    rmdir /s /q dist
)

if exist "build" (
    echo [*] Brišem staro build mapo...
    rmdir /s /q build
)

echo.
echo [*] Gradim GUI verzijo...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name="DAHUA_Discovery" ^
    --add-data "." ^
    dahua_discovery_gui.py

if errorlevel 1 (
    echo [-] Napaka pri gradnji GUI verzije!
    pause
    exit /b 1
)

echo [+] GUI verzija uspešno zgrajena!
echo.

echo [*] Gradim CLI verzijo...
python -m PyInstaller ^
    --onefile ^
    --console ^
    --name="DAHUA_Discovery_CLI" ^
    dahua_discovery.py

if errorlevel 1 (
    echo [-] Napaka pri gradnji CLI verzije!
    pause
    exit /b 1
)

echo [+] CLI verzija uspešno zgrajena!
echo.

echo ========================================
echo [+] Gradnja zaključena!
echo ========================================
echo.
echo EXE datoteki so v folder "dist\":
echo   - DAHUA_Discovery.exe (GUI verzija)
echo   - DAHUA_Discovery_CLI.exe (CLI verzija)
echo.

pause
