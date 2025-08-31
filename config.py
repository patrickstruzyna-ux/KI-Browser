#!/usr/bin/env python3
"""
Konfigurationsdatei für die LLM-Automatisierungs-App
"""

import os
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

class Config:
    """Enhanced configuration management for LLM automation"""
    
    # OpenRouter Konfiguration (kostenlose Modelle mit Vision)
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_MODELS = [
        'meta-llama/llama-3.2-11b-vision-instruct:free',
        'google/gemini-2.0-flash-exp:free'
    ]
    OPENROUTER_API_URL = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
    
    # Google Gemini Konfiguration (kostenlose Modelle)
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_MODELS = [
        'gemini-2.0-flash-exp',
        'gemini-1.5-flash',
        'gemini-1.5-flash-8b'
    ]
    GOOGLE_API_URL = os.getenv('GOOGLE_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent')
    
    # Aktuelle Modell-Indizes für Rate-Limit-Switching
    _current_openrouter_model_index = 0
    _current_google_model_index = 0
    
    # App-Einstellungen
    MAX_ITERATIONS = int(os.getenv('MAX_ITERATIONS', 20))
    DELAY_BETWEEN_ACTIONS = float(os.getenv('DELAY_BETWEEN_ACTIONS', 1.0))  # Sekunden
    SCREENSHOT_QUALITY = os.getenv('SCREENSHOT_QUALITY', 'PNG')  # PNG oder JPEG
    SCREENSHOT_CACHE_SIZE = int(os.getenv('SCREENSHOT_CACHE_SIZE', 5))
    SCREENSHOT_CHANGE_THRESHOLD = float(os.getenv('SCREENSHOT_CHANGE_THRESHOLD', 0.1))
    
    # PyAutoGUI-Einstellungen
    FAILSAFE_ENABLED = os.getenv('FAILSAFE_ENABLED', 'True').lower() == 'true'
    PAUSE_BETWEEN_ACTIONS = float(os.getenv('PAUSE_BETWEEN_ACTIONS', 0.5))
    
    # Logging-Konfiguration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # DEBUG, INFO, WARNING, ERROR
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', 'automation.log')
    
    # Modell-Konfiguration
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', "google/gemini-2.0-flash-exp:free")
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 500))
    
    # Safety and Validation Settings
    MAX_WAIT_TIME = float(os.getenv('MAX_WAIT_TIME', 30.0))
    
    # API Settings
    REQUEST_TIMEOUT = float(os.getenv('REQUEST_TIMEOUT', 30.0))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = float(os.getenv('RETRY_DELAY', 1.0))
    RATE_LIMIT_BACKOFF = float(os.getenv('RATE_LIMIT_BACKOFF', 60.0))
    
    # Performance Settings
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'True').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 300))  # 5 minutes
    OPTIMIZE_SCREENSHOTS = os.getenv('OPTIMIZE_SCREENSHOTS', 'True').lower() == 'true'
    
    # Monitoring Settings
    ENABLE_TELEMETRY = os.getenv('ENABLE_TELEMETRY', 'False').lower() == 'true'
    TELEMETRY_ENDPOINT = os.getenv('TELEMETRY_ENDPOINT', '')
    
    @classmethod
    def get_current_openrouter_model(cls) -> str:
        """Gibt das aktuelle OpenRouter-Modell zurück"""
        return cls.OPENROUTER_MODELS[cls._current_openrouter_model_index]
    
    @classmethod
    def get_current_google_model(cls) -> str:
        """Gibt das aktuelle Google-Modell zurück"""
        return cls.GOOGLE_MODELS[cls._current_google_model_index]
    
    @classmethod
    def switch_openrouter_model(cls):
        """Wechselt zum nächsten OpenRouter-Modell"""
        cls._current_openrouter_model_index = (cls._current_openrouter_model_index + 1) % len(cls.OPENROUTER_MODELS)
    
    @classmethod
    def switch_google_model(cls):
        """Wechselt zum nächsten Google-Modell"""
        cls._current_google_model_index = (cls._current_google_model_index + 1) % len(cls.GOOGLE_MODELS)
    
    @classmethod
    def get_api_config(cls, provider: str = 'openrouter') -> Dict[str, Any]:
        """
        Gibt die API-Konfiguration für den gewählten Provider zurück
        
        Args:
            provider: 'openrouter' oder 'google'
            
        Returns:
            Dictionary mit API-Konfiguration
        """
        if provider.lower() == 'openrouter':
            return {
                'api_key': cls.OPENROUTER_API_KEY,
                'api_url': cls.OPENROUTER_API_URL,
                'model': cls.get_current_openrouter_model()
            }
        elif provider.lower() == 'google':
            current_model = cls.get_current_google_model()
            return {
                'api_key': cls.GOOGLE_API_KEY,
                'api_url': cls.GOOGLE_API_URL.format(model=current_model),
                'model': current_model
            }
        else:
            raise ValueError(f"Unbekannter Provider: {provider}. Nur 'openrouter' und 'google' werden unterstützt.")
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Enhanced configuration validation"""
        status = {
            'openrouter_available': bool(cls.OPENROUTER_API_KEY),
            'google_available': bool(cls.GOOGLE_API_KEY),
            'valid_max_iterations': 1 <= cls.MAX_ITERATIONS <= 1000,
            'valid_delay': 0 <= cls.DELAY_BETWEEN_ACTIONS <= 10,
            'valid_cache_size': 1 <= cls.SCREENSHOT_CACHE_SIZE <= 20,
            'valid_change_threshold': 0.01 <= cls.SCREENSHOT_CHANGE_THRESHOLD <= 1.0,
            'valid_timeout': 1 <= cls.REQUEST_TIMEOUT <= 300,
            'valid_retries': 0 <= cls.MAX_RETRIES <= 10,
            'valid_wait_time': 0 <= cls.MAX_WAIT_TIME <= 300
        }
        return status
    
    @classmethod
    def get_performance_config(cls) -> Dict:
        """Get performance-related configuration"""
        return {
            'enable_caching': cls.ENABLE_CACHING,
            'cache_ttl': cls.CACHE_TTL,
            'optimize_screenshots': cls.OPTIMIZE_SCREENSHOTS,
            'screenshot_cache_size': cls.SCREENSHOT_CACHE_SIZE,
            'change_threshold': cls.SCREENSHOT_CHANGE_THRESHOLD
        }
    
    @classmethod
    def get_safety_config(cls) -> Dict:
        """Get safety-related configuration"""
        return {
            'max_wait_time': cls.MAX_WAIT_TIME,
            'failsafe_enabled': cls.FAILSAFE_ENABLED,
            'request_timeout': cls.REQUEST_TIMEOUT,
            'max_retries': cls.MAX_RETRIES
        }

# Enhanced .env file structure:
ENV_EXAMPLE = """
# .env Datei - Kopieren Sie diese Vorlage und fügen Sie Ihre API-Schlüssel ein

# OpenRouter API-Schlüssel (empfohlen - kostenlose Modelle verfügbar)
OPENROUTER_API_KEY=

# Google Gemini API-Schlüssel (empfohlen - kostenlose Modelle verfügbar)
GOOGLE_API_KEY=your-google-api-key-here

# App-Einstellungen (optional)
MAX_ITERATIONS=20
DELAY_BETWEEN_ACTIONS=1.0
LOG_LEVEL=INFO
LOG_FILE=automation.log

# Screenshot Settings
SCREENSHOT_QUALITY=PNG
SCREENSHOT_CACHE_SIZE=5
SCREENSHOT_CHANGE_THRESHOLD=0.1

# PyAutoGUI Settings
FAILSAFE_ENABLED=True
PAUSE_BETWEEN_ACTIONS=0.5

# Safety Settings
MAX_WAIT_TIME=30.0

# API Settings
REQUEST_TIMEOUT=30.0
MAX_RETRIES=3
RETRY_DELAY=1.0
RATE_LIMIT_BACKOFF=60.0

# Performance Settings
ENABLE_CACHING=True
CACHE_TTL=300
OPTIMIZE_SCREENSHOTS=True

# Monitoring Settings
ENABLE_TELEMETRY=False
TELEMETRY_ENDPOINT=
"""

if __name__ == "__main__":
    # Konfiguration testen
    print("Konfiguration wird getestet...")
    
    validation_status = Config.validate_config()
    if all(validation_status.values()):
        print("✓ Konfiguration ist gültig")
        print(f"  Validation details: {validation_status}")
    else:
        print("⚠ Konfiguration hat Probleme:")
        for key, value in validation_status.items():
            status = "✓" if value else "✗"
            print(f"  {status} {key}: {value}")
        
        # API-Konfiguration anzeigen
        try:
            openrouter_config = Config.get_api_config('openrouter')
            print(f"✓ OpenRouter konfiguriert: {bool(openrouter_config['api_key'])}")
            print(f"  Aktuelles Modell: {openrouter_config['model']}")
            print(f"  Verfügbare Modelle: {len(Config.OPENROUTER_MODELS)}")
        except:
            print("✗ OpenRouter nicht konfiguriert")
        
        try:
            google_config = Config.get_api_config('google')
            print(f"✓ Google Gemini konfiguriert: {bool(google_config['api_key'])}")
            print(f"  Aktuelles Modell: {google_config['model']}")
            print(f"  Verfügbare Modelle: {len(Config.GOOGLE_MODELS)}")
        except:
            print("✗ Google Gemini nicht konfiguriert")
else:
    print("✗ Konfiguration ist ungültig")
    print("\nBeispiel für .env Datei:")
    print(ENV_EXAMPLE)