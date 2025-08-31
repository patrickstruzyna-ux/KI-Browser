"""Custom exceptions for the LLM automation application"""

class LLMAutomationError(Exception):
    """Base exception for LLM automation errors"""
    pass

class ConfigurationError(LLMAutomationError):
    """Raised when there's a configuration issue"""
    pass

class APIError(LLMAutomationError):
    """Base class for API-related errors"""
    def __init__(self, message: str, provider: str = None, status_code: int = None):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code

class RateLimitError(APIError):
    """Raised when API rate limit is exceeded"""
    def __init__(self, message: str, provider: str = None, retry_after: int = None):
        super().__init__(message, provider)
        self.retry_after = retry_after

class AuthenticationError(APIError):
    """Raised when API authentication fails"""
    pass

class InvalidResponseError(APIError):
    """Raised when API returns invalid response"""
    pass

class TimeoutError(APIError):
    """Raised when API request times out"""
    pass

class JSONParsingError(LLMAutomationError):
    """Raised when JSON parsing fails"""
    def __init__(self, message: str, raw_response: str = None):
        super().__init__(message)
        self.raw_response = raw_response

class ActionValidationError(LLMAutomationError):
    """Raised when action validation fails"""
    def __init__(self, message: str, action_data: dict = None):
        super().__init__(message)
        self.action_data = action_data

class ScreenshotError(LLMAutomationError):
    """Raised when screenshot capture fails"""
    pass

class ProviderUnavailableError(LLMAutomationError):
    """Raised when no LLM providers are available"""
    pass

class MaxIterationsError(LLMAutomationError):
    """Raised when maximum iterations are reached"""
    def __init__(self, message: str, iterations: int = None):
        super().__init__(message)
        self.iterations = iterations