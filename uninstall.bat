@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   LLM GUI Automation - Deinstallation
echo ========================================
echo.

echo ⚠️  WARNUNG: Diese Aktion wird folgende Elemente entfernen:
echo - Virtuelle Umgebung (falls vorhanden)
echo - Installierte Python-Pakete (nur in venv)
echo - Temporäre Dateien und Screenshots
echo - Log-Dateien
echo.
echo Die folgenden Dateien bleiben erhalten:
echo - Quellcode-Dateien (.py)
echo - Konfigurationsdateien (.env, config.py)
echo - Dokumentation (README.md)
echo.

set /p CONFIRM="Möchten Sie wirklich deinstallieren? (j/n): "
if /i not "!CONFIRM!"=="j" (
    echo Deinstallation abgebrochen.
    pause
    exit /b 0
)

echo.
echo [1/5] Stoppe laufende Prozesse...
REM Versuche Python-Prozesse zu beenden (falls welche laufen)
tasklist /fi "imagename eq python.exe" 2>nul | find /i "python.exe" >nul
if not errorlevel 1 (
    echo Warnung: Python-Prozesse laufen noch. Bitte beenden Sie diese manuell.
    echo Drücken Sie eine Taste, wenn alle Python-Prozesse beendet sind...
    pause >nul
)
echo ✅ Prozesse überprüft
echo.

echo [2/5] Entferne virtuelle Umgebung...
if exist "venv" (
    echo Entferne virtuelle Umgebung...
    rmdir /s /q "venv" 2>nul
    if exist "venv" (
        echo ❌ Konnte virtuelle Umgebung nicht vollständig entfernen
        echo Möglicherweise sind noch Dateien in Verwendung
    ) else (
        echo ✅ Virtuelle Umgebung entfernt
    )
) else (
    echo ✅ Keine virtuelle Umgebung gefunden
)
echo.

echo [3/5] Entferne temporäre Dateien...
REM Entferne Screenshots
if exist "screenshot_*.png" (
    del /q "screenshot_*.png" 2>nul
    echo ✅ Screenshots entfernt
)
if exist "screenshot_*.jpg" (
    del /q "screenshot_*.jpg" 2>nul
)
if exist "temp_*.png" (
    del /q "temp_*.png" 2>nul
)
if exist "temp_*.jpg" (
    del /q "temp_*.jpg" 2>nul
)
if exist "debug_*.png" (
    del /q "debug_*.png" 2>nul
)
if exist "test_screenshot.*" (
    del /q "test_screenshot.*" 2>nul
)

REM Entferne Log-Dateien
if exist "*.log" (
    del /q "*.log" 2>nul
    echo ✅ Log-Dateien entfernt
)
if exist "logs" (
    rmdir /s /q "logs" 2>nul
    echo ✅ Log-Verzeichnis entfernt
)

REM Entferne Python-Cache
if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
    echo ✅ Python-Cache entfernt
)
if exist "*.pyc" (
    del /q "*.pyc" 2>nul
)

echo ✅ Temporäre Dateien entfernt
echo.

echo [4/5] Entferne Backup-Dateien...
if exist "*.bak" (
    del /q "*.bak" 2>nul
    echo ✅ Backup-Dateien entfernt
)
if exist "*.backup" (
    del /q "*.backup" 2>nul
)
if exist "*.old" (
    del /q "*.old" 2>nul
)
echo ✅ Backup-Dateien überprüft
echo.

echo [5/5] Abschluss...
echo.
echo ========================================
echo        Deinstallation abgeschlossen!
echo ========================================
echo.
echo ✅ Folgende Elemente wurden entfernt:
echo   - Virtuelle Umgebung
 echo   - Temporäre Dateien und Screenshots
echo   - Log-Dateien
echo   - Python-Cache
echo.
echo 📁 Folgende Dateien bleiben erhalten:
echo   - Quellcode (.py-Dateien)
echo   - Konfiguration (.env, config.py)
echo   - Dokumentation (README.md, .md-Dateien)
echo   - Abhängigkeiten (requirements.txt)
echo.
echo 💡 Um die App erneut zu installieren:
echo   1. Führen Sie 'install.bat' aus
echo   2. Oder installieren Sie manuell mit 'pip install -r requirements.txt'
echo.
echo 🗑️  Um alle Dateien zu entfernen:
echo   Löschen Sie das gesamte Projektverzeichnis manuell
echo.

REM Frage nach vollständiger Entfernung
set /p DELETE_ALL="Möchten Sie ALLE Dateien einschließlich Quellcode löschen? (j/n): "
if /i "!DELETE_ALL!"=="j" (
    echo.
    echo ⚠️  LETZTE WARNUNG: Dies wird ALLE Dateien in diesem Verzeichnis löschen!
    set /p FINAL_CONFIRM="Sind Sie absolut sicher? (j/n): "
    if /i "!FINAL_CONFIRM!"=="j" (
        echo Entferne alle Dateien...
        cd ..
        rmdir /s /q "KI-Browser" 2>nul
        if errorlevel 1 (
            echo ❌ Konnte nicht alle Dateien entfernen
            echo Möglicherweise sind noch Dateien in Verwendung
        ) else (
            echo ✅ Alle Dateien entfernt
            echo Das Projektverzeichnis wurde vollständig gelöscht.
        )
    ) else (
        echo Vollständige Löschung abgebrochen.
    )
) else (
    echo Quellcode-Dateien bleiben erhalten.
)

echo.
echo Deinstallation beendet. Drücken Sie eine beliebige Taste zum Beenden.
pause >nul