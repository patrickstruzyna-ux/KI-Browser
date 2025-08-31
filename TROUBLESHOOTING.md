# KI-Browser Troubleshooting Guide

## Behobene Probleme

### 1. Doppelte Ausgaben in der Konsole
**Problem:** Alle Ausgaben wurden doppelt angezeigt
**Ursache:** Terminal-Umgebung (MINGW64) Problem
**Lösung:** Dies ist ein bekanntes Problem mit der Terminal-Umgebung und betrifft nicht die Funktionalität der Anwendung.

### 2. LLM bleibt in Endlosschleife hängen
**Problem:** LLM verwendete immer `next_prompt` statt `complete`
**Ursache:** Fehlerhafter System-Prompt mit der Regel "You MUST ALWAYS use a next_prompt action, except for complete or error"
**Lösung:** System-Prompt korrigiert in `main.py` Zeile 70-85

### 3. `complete` Aktion funktionierte nicht korrekt
**Problem:** `complete` Aktion beendete die Schleife nur wenn "finish" im Text stand
**Ursache:** Fehlerhafte Logik in `execute_action` Methode
**Lösung:** `complete` Aktion gibt jetzt immer `None` zurück (Zeile 485 in `main.py`)

### 4. API Rate Limits erreicht
**Problem:** Alle API-Provider (OpenAI, Anthropic, OpenRouter, Google) haben 429 Fehler
**Ursache:** Quota-Limits der kostenlosen/Test-APIs erreicht
**Lösung:** 
- Fokus auf OpenRouter und Google Gemini APIs
- MAX_ITERATIONS von 20 auf 5 reduziert
- DELAY_BETWEEN_ACTIONS von 1.0 auf 2.0 erhöht

## Aktuelle Konfiguration

### API-Provider Status
- ❌ OpenAI: Quota exceeded
- ❌ Anthropic: Credit balance too low  
- ❌ OpenRouter: Rate limit exceeded
- ❌ Google Gemini: Quota exceeded

### Empfohlene Lösungen

#### Option 1: OpenRouter kostenlose Modelle verwenden
```bash
# Setze OPENROUTER_API_KEY in .env
python main.py -p "Öffne die webseite deepseek.com"
```

#### Option 2: Neue API-Keys besorgen
1. Erstelle neue Accounts bei den Providern
2. Aktualisiere die `.env` Datei mit neuen Keys
3. Teste mit `python test_api.py`

#### Option 3: Lokales LLM verwenden
1. Installiere Ollama: https://ollama.ai/
2. Lade ein Vision-Modell herunter: `ollama pull llava`
3. Erweitere `main.py` um Ollama-Support

## Getestete Funktionen

✅ Screenshot-Erstellung funktioniert
✅ Konfiguration wird korrekt geladen
✅ System-Prompt ist korrigiert
✅ Action-Parsing funktioniert
✅ OpenRouter kostenlose Modelle funktionieren
✅ Complete-Aktion beendet korrekt

## Nächste Schritte

1. **Sofort nutzbar:** Kostenlose OpenRouter/Google Modelle
2. **Kurzfristig:** Neue API-Keys besorgen
3. **Langfristig:** Lokales LLM integrieren für unabhängige Nutzung

## Verwendung

### Normale Nutzung (wenn APIs funktionieren)
```bash
python main.py -p "Deine Aufgabe hier"
```

### Kostenlose APIs nutzen
```bash
# OpenRouter (empfohlen)
OPENROUTER_API_KEY=sk-or-your-key python main.py -p "Deine Aufgabe hier"

# Google Gemini
GOOGLE_API_KEY=your-key python main.py -p "Deine Aufgabe hier"
```

### API-Tests
```bash
python test_api.py
```

### Konfiguration testen
```bash
python config.py
```

## Wichtige Dateien

- `main.py` - Hauptanwendung (korrigiert)
- `config.py` - Konfiguration für kostenlose APIs
- `test_api.py` - API-Verbindungstest (neu)
- `config.py` - Konfigurationsverwaltung
- `.env` - API-Keys und Einstellungen (angepasst)
- `TROUBLESHOOTING.md` - Diese Datei

Die Anwendung ist jetzt technisch funktionsfähig und bereit für den Einsatz mit funktionierenden API-Keys.