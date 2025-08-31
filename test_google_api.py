#!/usr/bin/env python3
"""
Test-Script für Google Gemini API
"""

import requests
import json
import base64
from config import Config
from PIL import Image
from io import BytesIO
import pyautogui

def test_google_api():
    """Testet die Google Gemini API mit einem einfachen Screenshot"""
    
    # Screenshot erstellen
    print("Erstelle Screenshot...")
    screenshot = pyautogui.screenshot()
    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # API-Konfiguration
    api_config = Config.get_api_config('google')
    
    headers = {
        "Content-Type": "application/json"
    }
    
    api_url = f"{api_config['api_url']}?key={api_config['api_key']}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Beschreibe was du in diesem Screenshot siehst. Antworte nur mit einem kurzen Satz."
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": img_str
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 100,
            "temperature": 0.1
        }
    }
    
    print(f"Sende Anfrage an: {api_url[:80]}...")
    print(f"Payload Größe: {len(json.dumps(payload))} Zeichen")
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"Fehler: {response.status_code}")
            print(f"Response Text: {response.text}")
            return
        
        print(f"Raw Response: {response.text[:500]}...")
        
        llm_response = response.json()
        print(f"Parsed Response: {llm_response}")
        
        # Google Gemini Response-Format prüfen
        if 'candidates' in llm_response and len(llm_response['candidates']) > 0:
            content = llm_response['candidates'][0]['content']['parts'][0]['text']
            print(f"Extrahierter Content: {content}")
        else:
            print(f"Unerwartete Response-Struktur: {llm_response}")
            
    except Exception as e:
        print(f"Fehler bei API-Anfrage: {e}")
        print(f"Exception Type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_google_api()