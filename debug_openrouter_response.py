#!/usr/bin/env python3
"""
Debug-Script für OpenRouter API Response
"""

import requests
import json
import base64
from config import Config
from PIL import Image
from io import BytesIO
import pyautogui

def debug_openrouter_response():
    """Debuggt die OpenRouter-Antwort im Detail"""
    
    print("🔍 Debug OpenRouter Response...")
    
    # Kleinen Screenshot erstellen
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((400, 300))
    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-repo",
        "X-Title": "LLM GUI Automation Debug"
    }
    
    # System-Prompt wie in der Hauptanwendung
    system_prompt = """
Du bist ein GUI-Automatisierungs-Assistent. Du erhältst Screenshots und sollst Aktionen ausführen.

Verfügbare Aktionen:
- click: {"action": "click", "x": 100, "y": 200}
- type: {"action": "type", "text": "Beispieltext"}
- scroll: {"action": "scroll", "direction": "down", "clicks": 3}
- complete: {"action": "complete", "message": "Aufgabe erfolgreich abgeschlossen"}
- error: {"action": "error", "message": "Fehlerbeschreibung"}

ANTWORTE NUR MIT GÜLTIGEM JSON! Keine Erklärungen, nur die JSON-Aktion.
"""
    
    user_prompt = "INITIALE MAUSBEWEGUNG ERFORDERLICH: Öffne die webseite deepseek.com. Führe zuerst eine move_mouse Aktion zu einem geeigneten Arbeitsbereich aus, um die Mausposition zu kalibrieren. Danach verwende next_prompt für den nächsten Schritt."
    
    payload = {
        "model": "meta-llama/llama-3.2-11b-vision-instruct:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
            ]}
        ],
        "max_tokens": 500
    }
    
    try:
        response = requests.post(Config.OPENROUTER_API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"\n📄 Raw Response Text:")
            raw_text = response.text
            print(f"'{raw_text}'")
            print(f"\nLength: {len(raw_text)}")
            print(f"First 100 chars: '{raw_text[:100]}'")
            print(f"Last 100 chars: '{raw_text[-100:]}'")
            
            try:
                result = response.json()
                print(f"\n✅ JSON Parse erfolgreich:")
                print(json.dumps(result, indent=2))
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"\n📝 LLM Content:")
                    print(f"'{content}'")
                    
                    # Versuche JSON aus Content zu extrahieren
                    print(f"\n🔧 JSON Extraction Test:")
                    try:
                        action_data = json.loads(content)
                        print(f"✅ Direct JSON parse erfolgreich: {action_data}")
                    except json.JSONDecodeError as e:
                        print(f"❌ Direct JSON parse fehlgeschlagen: {e}")
                        
                        # Versuche JSON-Block zu finden
                        start = content.find('{')
                        end = content.rfind('}') + 1
                        if start != -1 and end != 0:
                            json_str = content[start:end]
                            print(f"Extracted JSON: '{json_str}'")
                            try:
                                action_data = json.loads(json_str)
                                print(f"✅ Extracted JSON parse erfolgreich: {action_data}")
                            except json.JSONDecodeError as e2:
                                print(f"❌ Extracted JSON parse fehlgeschlagen: {e2}")
                        else:
                            print(f"❌ Kein JSON-Block gefunden")
                
            except json.JSONDecodeError as e:
                print(f"❌ Response JSON Parse fehlgeschlagen: {e}")
                print(f"Raw response: '{response.text}'")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_openrouter_response()