#!/usr/bin/env python3
"""
Test-Script für API-Verbindungen
"""

import base64
import json
import requests
from io import BytesIO
from PIL import Image
import pyautogui
from config import Config

def create_test_screenshot():
    """Erstellt einen kleinen Test-Screenshot"""
    # Kleinen Screenshot machen (100x100 Pixel)
    screenshot = pyautogui.screenshot(region=(0, 0, 100, 100))
    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def test_openrouter():
    """Testet OpenRouter API"""
    if not Config.OPENROUTER_API_KEY:
        print("❌ OpenRouter API Key nicht konfiguriert")
        return False
    
    try:
        screenshot_b64 = create_test_screenshot()
        
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/test-repo",
            "X-Title": "API Test"
        }
        
        payload = {
            "model": Config.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Beschreibe dieses Bild in einem Wort."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{screenshot_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 50
        }
        
        response = requests.post(Config.OPENROUTER_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ OpenRouter erfolgreich: {content[:50]}...")
            return True
        else:
            print(f"❌ OpenRouter Fehler {response.status_code}: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter Exception: {e}")
        return False

def test_openai():
    """Testet OpenAI API"""
    if not Config.OPENAI_API_KEY:
        print("❌ OpenAI API Key nicht konfiguriert")
        return False
    
    try:
        screenshot_b64 = create_test_screenshot()
        
        headers = {
            "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": Config.OPENAI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Beschreibe dieses Bild in einem Wort."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{screenshot_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 50
        }
        
        response = requests.post(Config.OPENAI_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ OpenAI erfolgreich: {content[:50]}...")
            return True
        else:
            print(f"❌ OpenAI Fehler {response.status_code}: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI Exception: {e}")
        return False

def test_anthropic():
    """Testet Anthropic API"""
    if not Config.ANTHROPIC_API_KEY:
        print("❌ Anthropic API Key nicht konfiguriert")
        return False
    
    try:
        screenshot_b64 = create_test_screenshot()
        
        headers = {
            "x-api-key": Config.ANTHROPIC_API_KEY,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": Config.ANTHROPIC_MODEL,
            "max_tokens": 50,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Beschreibe dieses Bild in einem Wort."
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": screenshot_b64
                            }
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(Config.ANTHROPIC_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            print(f"✅ Anthropic erfolgreich: {content[:50]}...")
            return True
        else:
            print(f"❌ Anthropic Fehler {response.status_code}: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Anthropic Exception: {e}")
        return False

def test_google():
    """Testet Google Gemini API"""
    if not Config.GOOGLE_API_KEY:
        print("❌ Google API Key nicht konfiguriert")
        return False
    
    try:
        screenshot_b64 = create_test_screenshot()
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.GOOGLE_MODEL}:generateContent?key={Config.GOOGLE_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Beschreibe dieses Bild in einem Wort."},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": screenshot_b64
                        }
                    }
                ]
            }]
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                content = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Google Gemini erfolgreich: {content[:50]}...")
                return True
            else:
                print(f"❌ Google Gemini: Keine Antwort erhalten")
                return False
        else:
            print(f"❌ Google Gemini Fehler {response.status_code}: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Google Gemini Exception: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Teste API-Verbindungen...\n")
    
    print("📊 Konfiguration:")
    print(f"OpenAI Model: {Config.OPENAI_MODEL if Config.OPENAI_API_KEY else 'Nicht konfiguriert'}")
    print(f"Anthropic Model: {Config.ANTHROPIC_MODEL if Config.ANTHROPIC_API_KEY else 'Nicht konfiguriert'}")
    print(f"OpenRouter Model: {Config.OPENROUTER_MODEL if Config.OPENROUTER_API_KEY else 'Nicht konfiguriert'}")
    print(f"Google Model: {Config.GOOGLE_MODEL if Config.GOOGLE_API_KEY else 'Nicht konfiguriert'}")
    print(f"OpenAI Key: {'✅' if Config.OPENAI_API_KEY else '❌'}")
    print(f"Anthropic Key: {'✅' if Config.ANTHROPIC_API_KEY else '❌'}")
    print(f"OpenRouter Key: {'✅' if Config.OPENROUTER_API_KEY else '❌'}")
    print(f"Google Key: {'✅' if Config.GOOGLE_API_KEY else '❌'}")
    print()
    
    # Tests ausführen
    openai_ok = test_openai()
    anthropic_ok = test_anthropic()
    openrouter_ok = test_openrouter()
    google_ok = test_google()
    
    print("\n📋 Ergebnisse:")
    print(f"OpenAI: {'✅' if openai_ok else '❌'}")
    print(f"Anthropic: {'✅' if anthropic_ok else '❌'}")
    print(f"OpenRouter: {'✅' if openrouter_ok else '❌'}")
    print(f"Google: {'✅' if google_ok else '❌'}")
    
    working_providers = sum([openai_ok, anthropic_ok, openrouter_ok, google_ok])
    
    if working_providers > 0:
        print(f"\n🎉 {working_providers} von 4 Providern funktionieren!")
    else:
        print("\n❌ Alle Provider fehlgeschlagen!")