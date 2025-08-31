import logging
import time
from typing import Dict, List, Optional, Any
from providers.base_provider import BaseLLMProvider
from providers.openrouter_provider import OpenRouterProvider, RateLimitError, APIError
from providers.google_provider import GoogleProvider

logger = logging.getLogger(__name__)

class LLMManager:
    """
    Central manager for all LLM providers with intelligent fallback
    """
    
    def __init__(self, config):
        self.config = config
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.current_provider = None
        self.fallback_order = ['openrouter', 'google']
        self.total_requests = 0
        self.successful_requests = 0
        self.provider_switches = 0
        
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available providers based on configuration"""
        # Initialize OpenRouter if API key is available
        if self.config.OPENROUTER_API_KEY:
            try:
                self.providers['openrouter'] = OpenRouterProvider(
                    api_key=self.config.OPENROUTER_API_KEY,
                    models=self.config.OPENROUTER_MODELS,
                    api_url=self.config.OPENROUTER_API_URL
                )
                logger.info(f"OpenRouter provider initialized with {len(self.config.OPENROUTER_MODELS)} models")
            except Exception as e:
                logger.error(f"Failed to initialize OpenRouter provider: {e}")
        
        # Initialize Google if API key is available
        if self.config.GOOGLE_API_KEY:
            try:
                self.providers['google'] = GoogleProvider(
                    api_key=self.config.GOOGLE_API_KEY,
                    models=self.config.GOOGLE_MODELS,
                    api_url_template=self.config.GOOGLE_API_URL
                )
                logger.info(f"Google provider initialized with {len(self.config.GOOGLE_MODELS)} models")
            except Exception as e:
                logger.error(f"Failed to initialize Google provider: {e}")
        
        if not self.providers:
            raise ValueError("No LLM providers could be initialized. Check your API keys.")
        
        # Set initial provider based on DEFAULT_MODEL or first available
        self._set_initial_provider()
    
    def _set_initial_provider(self):
        """Set the initial provider based on configuration"""
        default_model = self.config.DEFAULT_MODEL.lower()
        
        # Try to match provider based on default model
        if 'gemini' in default_model and 'google' in self.providers:
            self.current_provider = 'google'
        elif ('openrouter' in default_model or 'llama' in default_model or 'qwen' in default_model) and 'openrouter' in self.providers:
            self.current_provider = 'openrouter'
        else:
            # Use first available provider
            self.current_provider = next(iter(self.providers.keys()))
        
        logger.info(f"Initial provider set to: {self.current_provider}")
    
    def send_request(self, prompt: str, image_b64: str, max_retries: int = 3) -> str:
        """
        Send request with intelligent fallback between providers
        
        Args:
            prompt: Text prompt for the LLM
            image_b64: Base64 encoded screenshot
            max_retries: Maximum number of retry attempts per provider
            
        Returns:
            Raw response string from LLM
        """
        self.total_requests += 1
        last_error = None
        
        # Try current provider first
        for provider_name in [self.current_provider] + [p for p in self.fallback_order if p != self.current_provider]:
            if provider_name not in self.providers:
                continue
                
            provider = self.providers[provider_name]
            
            for attempt in range(max_retries):
                try:
                    logger.info(f"Attempting request with {provider_name} (attempt {attempt + 1}/{max_retries})")
                    response = provider.send_request(prompt, image_b64)
                    
                    # Success - update current provider if it changed
                    if self.current_provider != provider_name:
                        logger.info(f"Switching primary provider from {self.current_provider} to {provider_name}")
                        self.current_provider = provider_name
                        self.provider_switches += 1
                    
                    self.successful_requests += 1
                    return response
                    
                except RateLimitError:
                    logger.warning(f"Rate limit hit on {provider_name}, attempt {attempt + 1}")
                    if provider.handle_rate_limit():
                        continue  # Try again with same provider
                    else:
                        break  # Move to next provider
                        
                except APIError as e:
                    logger.error(f"API error on {provider_name}: {e}")
                    last_error = e
                    if attempt < max_retries - 1:
                        backoff_time = provider._implement_backoff(attempt + 1)
                        logger.info(f"Retrying {provider_name} after {backoff_time}s backoff")
                        time.sleep(backoff_time)
                    break  # Move to next provider after max retries
                    
                except Exception as e:
                    logger.error(f"Unexpected error on {provider_name}: {e}")
                    last_error = e
                    break  # Move to next provider
        
        # All providers failed
        error_msg = f"All LLM providers failed. Last error: {last_error}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def get_current_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider"""
        if self.current_provider and self.current_provider in self.providers:
            provider = self.providers[self.current_provider]
            return {
                'name': self.current_provider,
                'current_model': provider.get_current_model(),
                'available_models': provider.get_available_models(),
                'stats': provider.get_stats()
            }
        return {}
    
    def get_all_provider_stats(self) -> Dict[str, Any]:
        """Get statistics for all providers"""
        stats = {
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'success_rate': self.successful_requests / max(self.total_requests, 1),
            'provider_switches': self.provider_switches,
            'current_provider': self.current_provider,
            'providers': {}
        }
        
        for name, provider in self.providers.items():
            stats['providers'][name] = provider.get_stats()
        
        return stats
    
    def switch_provider(self, provider_name: str) -> bool:
        """
        Manually switch to a specific provider
        
        Args:
            provider_name: Name of the provider to switch to
            
        Returns:
            True if switch was successful, False otherwise
        """
        if provider_name in self.providers:
            old_provider = self.current_provider
            self.current_provider = provider_name
            self.provider_switches += 1
            logger.info(f"Manually switched provider from {old_provider} to {provider_name}")
            return True
        else:
            logger.error(f"Provider {provider_name} not available")
            return False
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return list(self.providers.keys())