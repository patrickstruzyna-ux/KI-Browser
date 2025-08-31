from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
import logging

logger = logging.getLogger(__name__)

class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers
    """
    
    def __init__(self, api_key: str, models: List[str]):
        self.api_key = api_key
        self.models = models
        self.current_model_index = 0
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = 0
        
    @abstractmethod
    def send_request(self, prompt: str, image_b64: str) -> str:
        """
        Send a request to the LLM provider
        
        Args:
            prompt: The text prompt
            image_b64: Base64 encoded screenshot
            
        Returns:
            Raw response string from the API
        """
        pass
    
    @abstractmethod
    def handle_rate_limit(self) -> bool:
        """
        Handle rate limit by switching models or implementing backoff
        
        Returns:
            True if rate limit was handled, False if no more options
        """
        pass
    
    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.models[self.current_model_index]
    
    def switch_model(self) -> bool:
        """
        Switch to the next available model
        
        Returns:
            True if switched successfully, False if no more models
        """
        if self.current_model_index < len(self.models) - 1:
            self.current_model_index += 1
            logger.info(f"Switched to model: {self.get_current_model()}")
            return True
        return False
    
    def reset_model_index(self):
        """Reset to the first model"""
        self.current_model_index = 0
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return self.models.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics"""
        return {
            'provider': self.__class__.__name__,
            'current_model': self.get_current_model(),
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.request_count, 1),
            'last_request_time': self.last_request_time
        }
    
    def _log_request(self, success: bool = True):
        """Log request statistics"""
        self.request_count += 1
        self.last_request_time = time.time()
        if not success:
            self.error_count += 1
    
    def _implement_backoff(self, attempt: int) -> float:
        """
        Calculate backoff delay for retries
        
        Args:
            attempt: Current attempt number (starting from 1)
            
        Returns:
            Delay in seconds
        """
        base_delay = 1.0
        max_delay = 30.0
        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
        return delay