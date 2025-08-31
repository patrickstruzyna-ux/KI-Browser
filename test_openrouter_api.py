#!/usr/bin/env python3
"""
Test-Script für OpenRouter API mit verschiedenen Modellen
"""

import requests
import json
import base64
from config import Config
from PIL import Image
from io import BytesIO
import pyautogui
import time

def test_openrouter_model(model_name):
    """Testet ein spezifisches OpenRouter-Modell"""
    
    print(f"\n=== Teste Modell: {model_name} ===")
    
    # Kleinen Screenshot erstellen (reduzierte Größe für Tests)
    screenshot = pyautogui.screenshot()
    # Verkleinern für schnellere Tests
    screenshot = screenshot.resize((400, 300))
    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-repo",
        "X-Title": "LLM GUI Automation Test"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "Du bist ein hilfreicher Assistent. Antworte kurz und präzise."},
            {"role": "user", "content": [
                {"type": "text", "text": "Beschreibe kurz was du in diesem Screenshot siehst. Antworte mit maximal einem Satz."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
            ]}
        ],
        "max_tokens": 100
    }
    
    try:
        response = requests.post(Config.OPENROUTER_API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"✅ Erfolg: {content[:100]}...")
                return True
            else:
                print(f"❌ Unerwartete Response-Struktur: {result}")
                return False
        elif response.status_code == 429:
            print(f"⚠️ Rate Limit erreicht")
            return False
        else:
            print(f"❌ Fehler {response.status_code}: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_all_openrouter_models():
    """Testet alle verfügbaren OpenRouter-Modelle"""
    
    print("🚀 Teste OpenRouter API mit verschiedenen Modellen...")
    print(f"API Key vorhanden: {bool(Config.OPENROUTER_API_KEY)}")
    
    working_models = []
    
    for model in Config.OPENROUTER_MODELS:
        success = test_openrouter_model(model)
        if success:
            working_models.append(model)
        
        # Kurze Pause zwischen Tests
        time.sleep(2)
    
    print(f"\n📊 Zusammenfassung:")
    print(f"Getestete Modelle: {len(Config.OPENROUTER_MODELS)}")
    print(f"Funktionierende Modelle: {len(working_models)}")
    
    if working_models:
        print(f"\n✅ Verfügbare Modelle:")
        for model in working_models:
            print(f"  - {model}")
    else:
        print(f"\n❌ Keine funktionierenden Modelle gefunden")
    
    return working_models

if __name__ == "__main__":
    test_all_openrouter_models()