@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    LLM GUI Automation - Installation
echo ========================================
echo.

REM Überprüfe Python-Installation
echo [1/6] Überprüfe Python-Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ist nicht installiert oder nicht im PATH!
    echo Bitte installieren Sie Python 3.8+ von https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% gefunden
echo.

REM Überprüfe pip
echo [2/6] Überprüfe pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip ist nicht verfügbar!
    echo Bitte installieren Sie pip oder verwenden Sie python -m pip
    pause
    exit /b 1
)
echo ✅ pip verfügbar
echo.

REM Erstelle virtuelle Umgebung (optional)
echo [3/6] Virtuelle Umgebung...
set /p CREATE_VENV="Möchten Sie eine virtuelle Umgebung erstellen? (j/n): "
if /i "!CREATE_VENV!"=="j" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Fehler beim Erstellen der virtuellen Umgebung
        pause
        exit /b 1
    )
    echo ✅ Virtuelle Umgebung erstellt
    echo Aktiviere virtuelle Umgebung...
    call venv\Scripts\activate.bat
    echo ✅ Virtuelle Umgebung aktiviert
) else (
    echo Verwende System-Python
)
echo.

REM Installiere Abhängigkeiten
echo [4/6] Installiere Python-Pakete...
echo Installiere Abhängigkeiten aus requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Fehler beim Installieren der Abhängigkeiten
    echo Versuche einzelne Installation...
    pip install pyautogui
    pip install Pillow
    pip install requests
    pip install python-dotenv
    if errorlevel 1 (
        echo ❌ Installation fehlgeschlagen
        pause
        exit /b 1
    )
)
echo ✅ Abhängigkeiten installiert
echo.

REM Erstelle .env-Datei
echo [5/6] Konfiguration...
if not exist ".env" (
    echo Erstelle .env-Datei aus Vorlage...
    copy ".env.example" ".env" >nul
    if errorlevel 1 (
        echo ❌ Fehler beim Erstellen der .env-Datei
    ) else (
        echo ✅ .env-Datei erstellt
        echo.
        echo ⚠️  WICHTIG: Bitte bearbeiten Sie die .env-Datei und fügen Sie Ihren OpenAI API-Schlüssel hinzu!
        echo    Öffnen Sie .env in einem Texteditor und ersetzen Sie:
        echo    OPENAI_API_KEY=sk-your-openai-api-key-here
        echo    mit Ihrem echten API-Schlüssel.
    )
) else (
    echo ✅ .env-Datei bereits vorhanden
)
echo.

REM Teste Installation
echo [6/6] Teste Installation...
echo Führe Basis-Test durch...
python -c "import pyautogui, PIL, requests, dotenv; print('✅ Alle Module erfolgreich importiert')"
if errorlevel 1 (
    echo ❌ Test fehlgeschlagen - Module können nicht importiert werden
    pause
    exit /b 1
)

echo Teste Konfiguration...
python -c "from config import Config; print('✅ Konfiguration geladen')"
if errorlevel 1 (
    echo ❌ Konfigurationstest fehlgeschlagen
    pause
    exit /b 1
)

echo.
echo ========================================
echo           Installation abgeschlossen!
echo ========================================
echo.
echo ✅ Alle Komponenten erfolgreich installiert
echo.
echo Nächste Schritte:
echo 1. Bearbeiten Sie die .env-Datei und fügen Sie Ihren OpenAI API-Schlüssel hinzu
echo 2. Führen Sie 'python main.py' aus, um die App zu starten
echo 3. Oder führen Sie 'python test_app.py' aus, um die Installation zu testen
echo 4. Oder führen Sie 'python examples.py' aus, um Beispiele anzusehen
echo.
echo Dokumentation: README.md
echo Support: Überprüfen Sie die Konfiguration in config.py
echo.

REM Frage nach sofortigem Test
set /p RUN_TEST="Möchten Sie jetzt einen Test ausführen? (j/n): "
if /i "!RUN_TEST!"=="j" (
    echo.
    echo Starte Test...
    python test_app.py
)

echo.
echo Installation beendet. Drücken Sie eine beliebige Taste zum Beenden.
pause >nul