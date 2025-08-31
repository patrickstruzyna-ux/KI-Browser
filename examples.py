#!/usr/bin/env python3
"""
Beispiele für die LLM-Automatisierungs-App

Dieses Skript enthält vorgefertigte Beispiele für verschiedene
Automatisierungsaufgaben.
"""

import time
from main import LLMAutomationApp
from config import Config

def example_web_login():
    """
    Beispiel: Web-Login automatisieren
    """
    task = """
    Öffne einen Webbrowser und logge dich auf einer Website ein:
    1. Öffne den Browser (falls nicht bereits offen)
    2. Navigiere zu einer Login-Seite
    3. Fülle die Login-Felder aus
    4. Klicke auf den Login-Button
    5. Bestätige erfolgreichen Login
    
    Hinweis: Verwende kostenlose OpenRouter oder Google Gemini APIs.
    """
    
    return task

def example_form_filling():
    """
    Beispiel: Formular ausfüllen
    """
    task = """
    Fülle ein Webformular aus:
    1. Finde das Formular auf der aktuellen Seite
    2. Fülle alle erforderlichen Felder aus:
       - Name: Max Mustermann
       - E-Mail: max@example.com
       - Telefon: +49 123 456789
       - Nachricht: Dies ist eine Testnachricht
    3. Überprüfe die Eingaben
    4. Sende das Formular ab
    """
    
    return task

def example_file_management():
    """
    Beispiel: Datei-Management
    """
    task = """
    Führe Datei-Management-Aufgaben durch:
    1. Öffne den Datei-Explorer
    2. Navigiere zum Desktop
    3. Erstelle einen neuen Ordner namens 'Test_Automation'
    4. Öffne den Ordner
    5. Erstelle eine neue Textdatei namens 'test.txt'
    6. Öffne die Datei und schreibe 'Automatisierung erfolgreich'
    7. Speichere und schließe die Datei
    """
    
    return task

def example_email_compose():
    """
    Beispiel: E-Mail verfassen
    """
    task = """
    Verfasse eine E-Mail:
    1. Öffne das E-Mail-Programm oder Webmail
    2. Klicke auf 'Neue E-Mail' oder 'Verfassen'
    3. Fülle die E-Mail-Felder aus:
       - An: test@example.com
       - Betreff: Automatisierungstest
       - Text: Dies ist eine automatisch erstellte Test-E-Mail.
    4. Überprüfe die E-Mail
    5. Speichere als Entwurf (NICHT senden!)
    """
    
    return task

def example_calculator():
    """
    Beispiel: Taschenrechner verwenden
    """
    task = """
    Verwende den Windows-Taschenrechner:
    1. Öffne den Taschenrechner (Windows-Taste + R, dann 'calc')
    2. Berechne: 123 + 456
    3. Notiere das Ergebnis
    4. Berechne: 789 * 12
    5. Notiere das Ergebnis
    6. Schließe den Taschenrechner
    """
    
    return task

def example_notepad_automation():
    """
    Beispiel: Notepad-Automatisierung
    """
    task = """
    Automatisiere Notepad:
    1. Öffne Notepad
    2. Schreibe folgenden Text:
       'Dies ist ein automatisierter Test.
       Datum: [aktuelles Datum]
       Zeit: [aktuelle Zeit]
       Status: Erfolgreich'
    3. Speichere die Datei als 'automation_test.txt' auf dem Desktop
    4. Schließe Notepad
    5. Öffne die gespeicherte Datei erneut zur Überprüfung
    """
    
    return task

def example_browser_navigation():
    """
    Beispiel: Browser-Navigation
    """
    task = """
    Navigiere im Browser:
    1. Öffne einen Webbrowser
    2. Gehe zu google.com
    3. Suche nach 'Python automation'
    4. Klicke auf das erste Suchergebnis
    5. Scrolle auf der Seite nach unten
    6. Gehe zurück zu Google
    7. Öffne einen neuen Tab
    8. Gehe zu wikipedia.org
    9. Suche nach 'Artificial Intelligence'
    """
    
    return task

def example_system_info():
    """
    Beispiel: Systeminformationen abrufen
    """
    task = """
    Rufe Systeminformationen ab:
    1. Öffne die Systemsteuerung
    2. Navigiere zu 'System und Sicherheit'
    3. Klicke auf 'System'
    4. Notiere die Windows-Version
    5. Notiere den Prozessor-Typ
    6. Notiere die RAM-Größe
    7. Schließe die Systemsteuerung
    """
    
    return task

def run_example(example_name, task_description):
    """
    Führt ein Beispiel aus
    """
    print(f"\n🚀 Starte Beispiel: {example_name}")
    print("="*60)
    print(f"Aufgabe: {task_description.strip()}")
    print("="*60)
    
    # Sicherheitsabfrage
    print("\n⚠️  WARNUNG: Diese Automatisierung wird echte GUI-Aktionen ausführen!")
    print("Stellen Sie sicher, dass:")
    print("- Keine wichtigen Anwendungen geöffnet sind")
    print("- Keine ungespeicherten Daten verloren gehen können")
    print("- Sie bereit sind, die Automatisierung zu überwachen")
    
    response = input("\nMöchten Sie fortfahren? (j/n): ")
    
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("Beispiel abgebrochen.")
        return False
    
    # Countdown
    print("\nStarte in:")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Los!\n")
    
    try:
        # App initialisieren
        app = LLMAutomationApp('openai')
        
        # Automatisierung starten
        success = app.run_automation(task_description)
        
        if success:
            print(f"\n✅ Beispiel '{example_name}' erfolgreich abgeschlossen!")
        else:
            print(f"\n❌ Beispiel '{example_name}' fehlgeschlagen.")
        
        return success
        
    except KeyboardInterrupt:
        print("\n⏹️  Automatisierung durch Benutzer gestoppt.")
        return False
    except Exception as e:
        print(f"\n💥 Fehler bei Beispiel '{example_name}': {e}")
        return False

def main():
    """
    Hauptfunktion für Beispiele
    """
    print("🎯 LLM-Automatisierung - Beispiele")
    print("="*40)
    
    # Verfügbare Beispiele
    examples = {
        "1": ("Web-Login", example_web_login),
        "2": ("Formular ausfüllen", example_form_filling),
        "3": ("Datei-Management", example_file_management),
        "4": ("E-Mail verfassen", example_email_compose),
        "5": ("Taschenrechner", example_calculator),
        "6": ("Notepad-Automatisierung", example_notepad_automation),
        "7": ("Browser-Navigation", example_browser_navigation),
        "8": ("Systeminformationen", example_system_info)
    }
    
    # Konfiguration prüfen
    if not Config.validate_config():
        print("❌ Konfiguration ungültig. Bitte überprüfen Sie Ihre .env-Datei.")
        return
    
    while True:
        print("\nVerfügbare Beispiele:")
        for key, (name, _) in examples.items():
            print(f"{key}. {name}")
        print("0. Beenden")
        
        choice = input("\nWählen Sie ein Beispiel (0-8): ").strip()
        
        if choice == "0":
            print("Auf Wiedersehen!")
            break
        elif choice in examples:
            name, func = examples[choice]
            task = func()
            run_example(name, task)
        else:
            print("❌ Ungültige Auswahl. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()