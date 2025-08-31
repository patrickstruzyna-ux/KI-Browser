import requests
import json
import time
import logging
from typing import Dict, Any
from .base_provider import BaseLLMProvider

logger = logging.getLogger(__name__)

class OpenRouterProvider(BaseLLMProvider):
    """
    OpenRouter API provider implementation
    """
    
    def __init__(self, api_key: str, models: list, api_url: str = None):
        super().__init__(api_key, models)
        self.api_url = api_url or 'https://openrouter.ai/api/v1/chat/completions'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/ki-browser',
            'X-Title': 'KI-Browser Automation'
        }
    
    def send_request(self, prompt: str, image_b64: str) -> str:
        """
        Send request to OpenRouter API
        """
        payload = {
            'model': self.get_current_model(),
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/png;base64,{image_b64}'
                            }
                        }
                    ]
                }
            ],
            'max_tokens': 500,
            'temperature': 0.1
        }
        
        try:
            logger.debug(f"Sending request to OpenRouter with model: {self.get_current_model()}")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            self._log_request(response.status_code == 200)
            
            if response.status_code == 429:
                logger.warning("Rate limit hit on OpenRouter")
                raise RateLimitError("OpenRouter rate limit exceeded")
            elif response.status_code != 200:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                raise APIError(f"OpenRouter API error: {response.status_code}")
            
            response_data = response.json()
            
            if 'choices' not in response_data or not response_data['choices']:
                logger.error("Invalid OpenRouter response structure")
                raise APIError("Invalid response structure from OpenRouter")
            
            content = response_data['choices'][0]['message']['content']
            logger.debug(f"Received response from OpenRouter: {len(content)} characters")
            
            return content
            
        except requests.exceptions.Timeout:
            self._log_request(False)
            logger.error("OpenRouter request timeout")
            raise APIError("OpenRouter request timeout")
        except requests.exceptions.RequestException as e:
            self._log_request(False)
            logger.error(f"OpenRouter request failed: {e}")
            raise APIError(f"OpenRouter request failed: {e}")
        except json.JSONDecodeError as e:
            self._log_request(False)
            logger.error(f"Failed to parse OpenRouter response: {e}")
            raise APIError(f"Invalid JSON response from OpenRouter: {e}")
    
    def handle_rate_limit(self) -> bool:
        """
        Handle rate limit by switching models or implementing backoff
        """
        logger.info("Handling OpenRouter rate limit")
        
        # Try switching to next model
        if self.switch_model():
            logger.info(f"Switched to OpenRouter model: {self.get_current_model()}")
            return True
        
        # If no more models, implement backoff
        logger.warning("No more OpenRouter models available, implementing backoff")
        backoff_time = self._implement_backoff(1)
        time.sleep(backoff_time)
        
        # Reset to first model after backoff
        self.reset_model_index()
        return True

class RateLimitError(Exception):
    """Raised when API rate limit is exceeded"""
    pass

class APIError(Exception):
    """Raised when API returns an error"""
    pass