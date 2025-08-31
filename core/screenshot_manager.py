import pyautogui
import base64
import hashlib
import time
import logging
from typing import Optional, Tuple
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

class ScreenshotManager:
    """
    Manages screenshot capture with caching and optimization
    """
    
    def __init__(self, cache_size: int = 5, compression_quality: int = 85, resize_factor: float = 0.8):
        self.cache_size = cache_size
        self.compression_quality = compression_quality
        self.resize_factor = resize_factor
        self.cache = {}
        self.cache_order = []
        self.last_hash = None
        self.screenshot_count = 0
        self.cache_hits = 0
        
    def get_screenshot(self, force_new: bool = False) -> str:
        """
        Get a screenshot, using cache if possible
        
        Args:
            force_new: Force taking a new screenshot even if cached version exists
            
        Returns:
            Base64 encoded screenshot
        """
        self.screenshot_count += 1
        
        if not force_new:
            # Check if screen has changed
            current_hash = self._get_screen_hash()
            if current_hash == self.last_hash and self.last_hash in self.cache:
                logger.debug("Using cached screenshot (screen unchanged)")
                self.cache_hits += 1
                return self.cache[current_hash]
        
        # Take new screenshot
        screenshot_b64 = self._take_new_screenshot()
        
        # Update cache
        current_hash = self._get_screen_hash()
        self._update_cache(current_hash, screenshot_b64)
        self.last_hash = current_hash
        
        logger.debug(f"New screenshot taken and cached (hash: {current_hash[:8]}...)")
        return screenshot_b64
    
    def _take_new_screenshot(self) -> str:
        """
        Take a new screenshot and optimize it
        
        Returns:
            Base64 encoded optimized screenshot
        """
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Optimize screenshot
            optimized_screenshot = self._optimize_screenshot(screenshot)
            
            # Convert to base64
            buffer = BytesIO()
            optimized_screenshot.save(buffer, format='PNG', optimize=True)
            screenshot_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logger.debug(f"Screenshot taken: {optimized_screenshot.size}, {len(screenshot_b64)} chars")
            return screenshot_b64
            
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    def _optimize_screenshot(self, screenshot: Image.Image) -> Image.Image:
        """
        Optimize screenshot for better API performance
        
        Args:
            screenshot: PIL Image object
            
        Returns:
            Optimized PIL Image object
        """
        # Resize if factor is less than 1.0
        if self.resize_factor < 1.0:
            new_size = (
                int(screenshot.width * self.resize_factor),
                int(screenshot.height * self.resize_factor)
            )
            screenshot = screenshot.resize(new_size, Image.Resampling.LANCZOS)
            logger.debug(f"Screenshot resized to: {new_size}")
        
        # Convert to RGB if necessary (removes alpha channel)
        if screenshot.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', screenshot.size, (255, 255, 255))
            background.paste(screenshot, mask=screenshot.split()[-1] if screenshot.mode == 'RGBA' else None)
            screenshot = background
        
        return screenshot
    
    def _get_screen_hash(self) -> str:
        """
        Get a hash of the current screen for change detection
        
        Returns:
            MD5 hash of screen content
        """
        try:
            # Take a small screenshot for hashing
            small_screenshot = pyautogui.screenshot(region=(0, 0, 200, 200))
            
            # Convert to bytes
            buffer = BytesIO()
            small_screenshot.save(buffer, format='PNG')
            screenshot_bytes = buffer.getvalue()
            
            # Calculate hash
            return hashlib.md5(screenshot_bytes).hexdigest()
            
        except Exception as e:
            logger.warning(f"Failed to calculate screen hash: {e}")
            return str(time.time())  # Fallback to timestamp
    
    def _update_cache(self, hash_key: str, screenshot_b64: str):
        """
        Update the screenshot cache
        
        Args:
            hash_key: Hash key for the screenshot
            screenshot_b64: Base64 encoded screenshot
        """
        # Add to cache
        self.cache[hash_key] = screenshot_b64
        
        # Update order
        if hash_key in self.cache_order:
            self.cache_order.remove(hash_key)
        self.cache_order.append(hash_key)
        
        # Remove old entries if cache is full
        while len(self.cache) > self.cache_size:
            oldest_key = self.cache_order.pop(0)
            if oldest_key in self.cache:
                del self.cache[oldest_key]
                logger.debug(f"Removed old screenshot from cache: {oldest_key[:8]}...")
    
    def save_screenshot(self, filename: str = None) -> str:
        """
        Save current screenshot to file
        
        Args:
            filename: Optional filename, auto-generated if not provided
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            raise
    
    def clear_cache(self):
        """Clear the screenshot cache"""
        self.cache.clear()
        self.cache_order.clear()
        self.last_hash = None
        logger.info("Screenshot cache cleared")
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        return {
            'cache_size': len(self.cache),
            'max_cache_size': self.cache_size,
            'screenshot_count': self.screenshot_count,
            'cache_hits': self.cache_hits,
            'cache_hit_rate': self.cache_hits / max(self.screenshot_count, 1),
            'compression_quality': self.compression_quality,
            'resize_factor': self.resize_factor
        }