# 🚀 Schnellstart-Anleitung

Eine einfache Anleitung, um die LLM GUI Automation App in wenigen Minuten zum Laufen zu bringen.

## ⚡ Express-Installation (5 Minuten)

### 1. Voraussetzungen prüfen
```bash
# Python-Version prüfen (benötigt 3.8+)
python --version

# Falls Python nicht installiert ist:
# Laden Sie es von https://python.org herunter
```

### 2. Automatische Installation
```bash
# Doppelklick auf install.bat ODER:
install.bat
```

### 3. API-Schlüssel konfigurieren

#### Option 1: OpenRouter (Empfohlen - Kostenlos)
1. **OpenRouter API-Schlüssel erhalten:**
   - Besuchen Sie [OpenRouter](https://openrouter.ai/)
   - Erstellen Sie ein kostenloses Konto
   - Gehen Sie zu "Keys" und erstellen Sie einen neuen API-Schlüssel
   - Kopieren Sie den Schlüssel (beginnt mit `sk-or-v1-`)

2. **Schlüssel in .env eintragen:**
   ```env
   OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here
   ```

#### Option 2: Google Gemini (Direkt)
1. **Google API-Schlüssel erhalten:**
   - Besuchen Sie [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Erstellen Sie einen neuen API-Schlüssel
   - Kopieren Sie den Schlüssel

2. **Schlüssel in .env eintragen:**
   ```env
   GOOGLE_API_KEY=your-google-api-key-here
   ```

#### Option 3: OpenAI (Kostenpflichtig)
1. **OpenAI API-Schlüssel erhalten:**
   - Besuchen Sie [OpenAI Platform](https://platform.openai.com/api-keys)
   - Erstellen Sie einen neuen API-Schlüssel
   - Kopieren Sie den Schlüssel (beginnt mit `sk-`)

2. **Schlüssel in .env eintragen:**
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### 4. Erste Ausführung
```bash
# Test der Installation
python test_app.py

# Erste Automatisierung
python main.py
```

## 🎯 Erste Schritte

### Einfacher Test
1. Starten Sie `python main.py`
2. Wählen Sie "Einfacher Test" aus dem Menü
3. Folgen Sie den Anweisungen auf dem Bildschirm

### Beispiele ausprobieren
```bash
python examples.py
```

Wählen Sie ein Beispiel aus:
- **Taschenrechner** (einfach, sicher)
- **Notepad-Automatisierung** (mittlere Komplexität)
- **Browser-Navigation** (fortgeschritten)

## 🛡️ Sicherheitshinweise

### ⚠️ Vor der ersten Nutzung
- **Schließen Sie wichtige Anwendungen**
- **Speichern Sie alle offenen Dokumente**
- **Testen Sie zuerst mit einfachen Aufgaben**

### 🚨 Notfall-Stopp
- **Maus in die obere linke Ecke bewegen** → Sofortiger Stopp
- **Strg+C** im Terminal → Programm beenden
- **Alt+Tab** → Zu anderem Fenster wechseln

## 📋 Häufige erste Aufgaben

### 1. Taschenrechner-Test
```
Aufgabe: "Öffne den Windows-Taschenrechner und berechne 123 + 456"
```

### 2. Notepad-Test
```
Aufgabe: "Öffne Notepad, schreibe 'Hello World' und speichere als test.txt"
```

### 3. Browser-Test
```
Aufgabe: "Öffne einen Browser und gehe zu google.com"
```

## 🔧 Schnelle Problemlösung

### Installation schlägt fehl
```bash
# Manuelle Installation
pip install pyautogui Pillow requests python-dotenv
```

### API-Fehler
- Überprüfen Sie Ihren OpenAI API-Schlüssel in `.env`
- Stellen Sie sicher, dass Sie Guthaben haben
- Testen Sie mit: `python -c "from config import Config; print(Config.validate_config())"`

### App reagiert nicht
- Bewegen Sie die Maus in die obere linke Ecke
- Drücken Sie Strg+C im Terminal
- Starten Sie neu

### Screenshots funktionieren nicht
- Stellen Sie sicher, dass keine anderen Programme den Bildschirm blockieren
- Überprüfen Sie die Bildschirmauflösung
- Testen Sie mit: `python -c "import pyautogui; pyautogui.screenshot().save('test.png')"`

## 📚 Nächste Schritte

### Nach dem ersten erfolgreichen Test
1. **Lesen Sie die vollständige Dokumentation**: `README.md`
2. **Experimentieren Sie mit Beispielen**: `python examples.py`
3. **Passen Sie die Konfiguration an**: `config.py`
4. **Erstellen Sie eigene Automatisierungen**

### Erweiterte Nutzung
- **Eigene Prompts schreiben**: Siehe Beispiele in `examples.py`
- **Konfiguration anpassen**: Timeouts, Modelle, etc. in `config.py`
- **Logging aktivieren**: Für Debugging und Analyse

## 🆘 Hilfe benötigt?

### Dokumentation
- **Vollständige Anleitung**: `README.md`
- **Konfiguration**: `config.py` (Kommentare lesen)
- **Beispiele**: `examples.py`

### Testen
- **Installationstest**: `python test_app.py`
- **Konfigurationstest**: `python -c "from config import Config; Config.validate_config()"`

### Häufige Probleme
1. **"Module not found"** → Führen Sie `install.bat` erneut aus
2. **"API key invalid"** → Überprüfen Sie `.env`-Datei
3. **"Permission denied"** → Führen Sie als Administrator aus
4. **App hängt** → Maus in obere linke Ecke bewegen

## 🎉 Erfolgreich gestartet?

Glückwunsch! Sie können jetzt:
- ✅ Einfache GUI-Automatisierungen durchführen
- ✅ Screenshots analysieren lassen
- ✅ LLM-gesteuerte Aktionen ausführen
- ✅ Eigene Automatisierungsaufgaben erstellen

**Nächster Schritt**: Probieren Sie komplexere Beispiele aus `examples.py` aus!

---

*💡 Tipp: Beginnen Sie immer mit einfachen Aufgaben und arbeiten Sie sich zu komplexeren vor. Die App lernt aus jedem Screenshot und wird mit der Zeit präziser.*