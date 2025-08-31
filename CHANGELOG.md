# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Geplant
- Unterstützung für Claude/Anthropic API
- GUI-Interface für einfachere Bedienung
- Aufgaben-Vorlagen und -Bibliothek
- Erweiterte Fehlerbehandlung
- Performance-Optimierungen

## [1.0.0] - 2024-01-XX

### Hinzugefügt
- **Kern-Funktionalität**
  - LLM-gesteuerte GUI-Automatisierung
  - Screenshot-Analyse mit OpenAI GPT-4 Vision
  - Automatische Aktionsausführung (Klicks, Tastatureingaben, etc.)
  - Selbst-triggernde LLM-Loops
  - JSON-basierte Aktionsstruktur

- **Konfiguration**
  - Umfassende Konfigurationsdatei (`config.py`)
  - Umgebungsvariablen-Unterstützung (`.env`)
  - Anpassbare Timeouts und Verzögerungen
  - PyAutoGUI-Sicherheitseinstellungen

- **Benutzerfreundlichkeit**
  - Interaktives Hauptmenü
  - Vordefinierte Aufgaben-Beispiele
  - Countdown vor Automatisierung
  - Notfall-Stopp-Funktion

- **Sicherheit**
  - Failsafe-Mechanismus (Maus in Ecke)
  - Iterationslimits
  - API-Schlüssel-Validierung
  - Sichere Konfigurationsverwaltung

- **Dokumentation**
  - Umfassende README mit Installationsanleitung
  - Schnellstart-Anleitung (`QUICKSTART.md`)
  - Beispielsammlung (`examples.py`)
  - Inline-Code-Dokumentation

- **Testing und Entwicklung**
  - Umfassendes Testskript (`test_app.py`)
  - Rate-Limit-Handling für kostenlose APIs
  - Beispiel-Automatisierungen
  - Debugging-Funktionen

- **Installation und Wartung**
  - Automatisches Installationsskript (`install.bat`)
  - Deinstallationsskript (`uninstall.bat`)
  - Requirements-Management
  - Git-Integration (`.gitignore`)

### Unterstützte Aktionen
- **Maus-Interaktionen**
  - `click` - Einfacher Klick
  - `double_click` - Doppelklick
  - `right_click` - Rechtsklick
  - `scroll` - Scrollen

- **Tastatur-Interaktionen**
  - `type` - Text eingeben
  - `key` - Einzelne Tasten/Shortcuts

- **Ablaufsteuerung**
  - `wait` - Warten/Pause
  - `next_prompt` - Nächster Automatisierungsschritt
  - `complete` - Aufgabe abgeschlossen
  - `error` - Fehler melden

### Technische Details
- **Abhängigkeiten**
  - Python 3.8+
  - PyAutoGUI für GUI-Automatisierung
  - Pillow für Bildverarbeitung
  - Requests für HTTP-Kommunikation
  - python-dotenv für Umgebungsvariablen

- **API-Unterstützung**
  - OpenAI GPT-4 Vision (primär)
  - Vorbereitung für Anthropic Claude

- **Plattform-Unterstützung**
  - Windows (primär getestet)
  - macOS (experimentell)
  - Linux (experimentell)

### Bekannte Einschränkungen
- Erfordert OpenAI API-Schlüssel mit GPT-4 Vision Zugang
- Funktioniert am besten mit Standard-Windows-Anwendungen
- Kann bei sehr schnellen Animationen Probleme haben
- Begrenzte Unterstützung für komplexe Web-Anwendungen

### Sicherheitshinweise
- **WICHTIG**: Niemals mit sensiblen Daten oder kritischen Systemen verwenden
- Immer in sicherer Umgebung testen
- API-Schlüssel sicher aufbewahren
- Regelmäßige Überwachung während Automatisierung

## Entwicklungshistorie

### Konzeptphase
- Grundidee: LLM-gesteuerte GUI-Automatisierung
- Anforderungsanalyse für Screenshot-basierte Steuerung
- Architektur-Design für modulare Struktur

### Implementierungsphase
- Kern-Engine für Screenshot-Analyse
- LLM-Integration mit strukturierter JSON-Ausgabe
- Aktions-Ausführungssystem
- Sicherheitsmechanismen

### Testing und Verfeinerung
- Umfassende Testsuite
- Beispiel-Automatisierungen
- Benutzerfreundlichkeits-Verbesserungen
- Dokumentation und Anleitungen

## Mitwirkende

- **Hauptentwicklung**: KI-Assistent (Claude)
- **Konzept und Anforderungen**: Benutzer-Input
- **Testing und Feedback**: Community

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe `LICENSE`-Datei für Details.

---

### Legende
- `Hinzugefügt` für neue Features
- `Geändert` für Änderungen an bestehender Funktionalität
- `Veraltet` für Features, die bald entfernt werden
- `Entfernt` für entfernte Features
- `Behoben` für Bugfixes
- `Sicherheit` für Sicherheits-Updates