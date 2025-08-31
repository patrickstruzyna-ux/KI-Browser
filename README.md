# Enhanced LLM GUI Automation Tool

Ein verbessertes KI-gesteuertes GUI-Automatisierungstool mit modularer Architektur, robuster Fehlerbehandlung und intelligenter Screenshot-Verwaltung.

## 🚀 Features

### Kernfunktionen
- **Modulare Architektur**: Saubere Trennung von Verantwortlichkeiten
- **Multi-Provider Support**: OpenRouter und Google Gemini APIs
- **Intelligente Screenshot-Verwaltung**: Caching und Änderungserkennung
- **Robuste JSON-Parsing**: Mehrere Fallback-Strategien
- **Erweiterte Fehlerbehandlung**: Spezifische Exception-Klassen
- **Performance-Optimierung**: Caching und Komprimierung
- **Umfassende Protokollierung**: Detaillierte Session-Statistiken

### Verfügbare Aktionen
1. **click** - Klick auf Koordinaten
2. **double_click** - Doppelklick
3. **right_click** - Rechtsklick
4. **type** - Text eingeben
5. **key** - Tastenkombinationen
6. **scroll** - Scrollen
7. **move_mouse** - Mausbewegung
8. **navigate** - URL öffnen
9. **wait** - Warten
10. **next_prompt** - Nächste Anweisung
11. **complete** - Aufgabe abgeschlossen
12. **error** - Fehler melden

## 📁 Projektstruktur

```
KI-Browser/
├── main.py                    # Hauptanwendung
├── config.py                  # Konfigurationsverwaltung
├── requirements.txt           # Abhängigkeiten
├── .env                      # Umgebungsvariablen
├── README.md                 # Diese Datei
├── core/                     # Kernkomponenten
│   ├── __init__.py
│   ├── llm_manager.py        # LLM-Provider-Verwaltung
│   ├── screenshot_manager.py # Screenshot-Verwaltung
│   ├── action_executor.py    # Aktionsausführung
│   └── exceptions.py         # Custom Exceptions
├── providers/                # LLM-Provider
│   ├── __init__.py
│   ├── base_provider.py      # Basis-Provider-Klasse
│   ├── openrouter_provider.py
│   └── google_provider.py
└── utils/                    # Hilfsfunktionen
    ├── __init__.py
    └── json_parser.py        # Robuster JSON-Parser
```

## 🛠️ Installation

### Voraussetzungen
- Python 3.8+
- Windows (für PyAutoGUI)

### Schritt 1: Repository klonen
```bash
git clone <repository-url>
cd KI-Browser
```

### Schritt 2: Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### Schritt 3: Umgebungsvariablen konfigurieren
Kopieren Sie `.env.example` zu `.env` und fügen Sie Ihre API-Schlüssel hinzu:

```env
# OpenRouter API (optional)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=meta-llama/llama-3.2-11b-vision-instruct:free
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions

# Google Gemini API (optional)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-1.5-flash
GOOGLE_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
```

## 🚀 Verwendung

### Grundlegende Verwendung
```bash
python main.py "Öffne Google und suche nach Python"
```

### Erweiterte Optionen
```bash
# Spezifischen Provider verwenden
python main.py --provider google "Navigiere zu Wikipedia"

# Konfiguration validieren
python main.py --validate-config

# Log-Level überschreiben
python main.py --log-level DEBUG "Teste die Anwendung"

# Maximale Iterationen festlegen
python main.py --max-iterations 10 "Komplexe Aufgabe"
```

### Hilfe anzeigen
```bash
python main.py --help
```

## ⚙️ Konfiguration

### Wichtige Einstellungen in `.env`

#### Anwendungseinstellungen
```env
MAX_ITERATIONS=20              # Maximale Anzahl von Iterationen
DELAY_BETWEEN_ACTIONS=1.0      # Verzögerung zwischen Aktionen
```

#### Screenshot-Einstellungen
```env
SCREENSHOT_CACHE_ENABLED=True        # Screenshot-Caching aktivieren
SCREENSHOT_CHANGE_DETECTION=True     # Änderungserkennung
SCREENSHOT_OPTIMIZATION=True         # Bildoptimierung
SCREENSHOT_RESIZE_FACTOR=0.8         # Größenänderungsfaktor
SCREENSHOT_COMPRESSION_QUALITY=85    # Komprimierungsqualität
```

#### Sicherheitseinstellungen
```env
SAFE_CLICK_ZONES=True                    # Sichere Klickzonen
CONFIRMATION_REQUIRED_ACTIONS=navigate,key  # Bestätigung erforderlich
MAX_WAIT_TIME=30                        # Maximale Wartezeit
```

#### API-Einstellungen
```env
API_REQUEST_TIMEOUT=30         # Request-Timeout
API_MAX_RETRIES=3             # Maximale Wiederholungen
API_RETRY_DELAY=2             # Verzögerung zwischen Wiederholungen
RATE_LIMIT_BACKOFF=5          # Rate-Limit-Backoff
```

## 🏗️ Architektur

### Kernkomponenten

#### LLMManager
- Verwaltet mehrere LLM-Provider
- Intelligente Fallback-Mechanismen
- Rate-Limit-Behandlung
- Statistiken und Monitoring

#### ScreenshotManager
- Intelligentes Caching
- Änderungserkennung
- Bildoptimierung
- Performance-Überwachung

#### ActionExecutor
- Validierung von Aktionsdaten
- Sichere Aktionsausführung
- Fehlerbehandlung
- Ausführungsstatistiken

#### RobustJSONParser
- Mehrere Parsing-Strategien
- Fallback-Mechanismen
- Validierung von Aktionsdaten
- Fehlertoleranz

### Provider-System

#### BaseLLMProvider
- Abstrakte Basisklasse
- Einheitliche Schnittstelle
- Rate-Limit-Behandlung
- Statistiken

#### OpenRouterProvider
- OpenRouter API-Integration
- Modell-Switching
- Fehlerbehandlung

#### GoogleProvider
- Google Gemini API-Integration
- Spezifische Payload-Formatierung
- Error-Handling

## 📊 Monitoring und Logging

### Session-Statistiken
- Ausführungsdauer
- Anzahl der Iterationen
- Screenshot-Aufnahmen
- LLM-Anfragen
- Aktionsausführungen
- Erfolgsraten
- Fehlerprotokollierung

### Komponentenstatistiken
- LLM-Manager-Metriken
- Screenshot-Manager-Performance
- Action-Executor-Erfolgsraten

### Log-Konfiguration
```env
LOG_LEVEL=INFO                                           # Log-Level
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s  # Format
LOG_FILE=automation.log                                  # Log-Datei
```

## 🔧 Entwicklung

### Entwicklungsumgebung einrichten
```bash
# Entwicklungsabhängigkeiten installieren
pip install -r requirements.txt pytest black flake8

# Code formatieren
black .

# Linting
flake8 .

# Tests ausführen
pytest
```

### Neue Provider hinzufügen
1. Erstellen Sie eine neue Klasse in `providers/`
2. Erben Sie von `BaseLLMProvider`
3. Implementieren Sie die erforderlichen Methoden
4. Registrieren Sie den Provider in `LLMManager`

### Neue Aktionen hinzufügen
1. Erweitern Sie `ActionExecutor.execute_action()`
2. Fügen Sie Validierung in `RobustJSONParser.validate_action()` hinzu
3. Aktualisieren Sie den System-Prompt
4. Dokumentieren Sie die neue Aktion

## 🚨 Fehlerbehebung

### Häufige Probleme

#### Konfigurationsfehler
```bash
# Konfiguration validieren
python main.py --validate-config
```

#### API-Schlüssel-Probleme
- Überprüfen Sie die `.env`-Datei
- Stellen Sie sicher, dass API-Schlüssel gültig sind
- Prüfen Sie API-Limits und Kontingente

#### Screenshot-Probleme
- Stellen Sie sicher, dass PyAutoGUI funktioniert
- Überprüfen Sie Bildschirmauflösung
- Deaktivieren Sie Caching bei Problemen

#### JSON-Parsing-Fehler
- Überprüfen Sie LLM-Antworten in den Logs
- Passen Sie System-Prompts an
- Verwenden Sie Debug-Modus

### Debug-Modus
```bash
python main.py --log-level DEBUG "Test-Aufgabe"
```

## 📝 Lizenz

MIT License - siehe LICENSE-Datei für Details.

## 🤝 Beitragen

1. Fork des Repositories
2. Feature-Branch erstellen
3. Änderungen committen
4. Tests ausführen
5. Pull Request erstellen

## 📞 Support

Bei Problemen oder Fragen:
1. Überprüfen Sie die Dokumentation
2. Suchen Sie in den Issues
3. Erstellen Sie ein neues Issue mit detaillierter Beschreibung

---

**Hinweis**: Dieses Tool automatisiert GUI-Interaktionen. Verwenden Sie es verantwortungsvoll und beachten Sie die Nutzungsbedingungen der verwendeten APIs und Anwendungen.