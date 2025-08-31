import requests
import json
import time
import logging
from typing import Dict, Any
from .base_provider import BaseLLMProvider
from .openrouter_provider import RateLimitError, APIError

logger = logging.getLogger(__name__)

class GoogleProvider(BaseLLMProvider):
    """
    Google Gemini API provider implementation
    """
    
    def __init__(self, api_key: str, models: list, api_url_template: str = None):
        super().__init__(api_key, models)
        self.api_url_template = api_url_template or 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
    
    def _get_api_url(self) -> str:
        """Get API URL for current model"""
        return self.api_url_template.format(model=self.get_current_model())
    
    def send_request(self, prompt: str, image_b64: str) -> str:
        """
        Send request to Google Gemini API
        """
        payload = {
            'contents': [{
                'parts': [
                    {
                        'text': prompt
                    },
                    {
                        'inline_data': {
                            'mime_type': 'image/png',
                            'data': image_b64
                        }
                    }
                ]
            }],
            'generationConfig': {
                'maxOutputTokens': 500,
                'temperature': 0.1
            }
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {
            'key': self.api_key
        }
        
        try:
            logger.debug(f"Sending request to Google with model: {self.get_current_model()}")
            response = requests.post(
                self._get_api_url(),
                headers=headers,
                params=params,
                json=payload,
                timeout=30
            )
            
            self._log_request(response.status_code == 200)
            
            if response.status_code == 429:
                logger.warning("Rate limit hit on Google Gemini")
                raise RateLimitError("Google Gemini rate limit exceeded")
            elif response.status_code != 200:
                logger.error(f"Google API error: {response.status_code} - {response.text}")
                raise APIError(f"Google API error: {response.status_code}")
            
            response_data = response.json()
            
            if 'candidates' not in response_data or not response_data['candidates']:
                logger.error("Invalid Google response structure")
                raise APIError("Invalid response structure from Google")
            
            candidate = response_data['candidates'][0]
            if 'content' not in candidate or 'parts' not in candidate['content']:
                logger.error("Missing content in Google response")
                raise APIError("Missing content in Google response")
            
            content = candidate['content']['parts'][0]['text']
            logger.debug(f"Received response from Google: {len(content)} characters")
            
            return content
            
        except requests.exceptions.Timeout:
            self._log_request(False)
            logger.error("Google request timeout")
            raise APIError("Google request timeout")
        except requests.exceptions.RequestException as e:
            self._log_request(False)
            logger.error(f"Google request failed: {e}")
            raise APIError(f"Google request failed: {e}")
        except json.JSONDecodeError as e:
            self._log_request(False)
            logger.error(f"Failed to parse Google response: {e}")
            raise APIError(f"Invalid JSON response from Google: {e}")
        except KeyError as e:
            self._log_request(False)
            logger.error(f"Missing key in Google response: {e}")
            raise APIError(f"Missing key in Google response: {e}")
    
    def handle_rate_limit(self) -> bool:
        """
        Handle rate limit by switching models or implementing backoff
        """
        logger.info("Handling Google rate limit")
        
        # Try switching to next model
        if self.switch_model():
            logger.info(f"Switched to Google model: {self.get_current_model()}")
            return True
        
        # If no more models, implement backoff
        logger.warning("No more Google models available, implementing backoff")
        backoff_time = self._implement_backoff(1)
        time.sleep(backoff_time)
        
        # Reset to first model after backoff
        self.reset_model_index()
        return True