import pyautogui
import time
import webbrowser
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class ActionExecutor:
    """
    Executes GUI actions with validation and safety checks
    """
    
    def __init__(self, config):
        self.config = config
        self.screen_size = pyautogui.size()
        self.safe_zones = getattr(config, 'SAFE_CLICK_ZONES', [])
        self.confirmation_required = getattr(config, 'CONFIRMATION_REQUIRED_ACTIONS', [])
        self.action_count = 0
        self.successful_actions = 0
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = getattr(config, 'FAILSAFE_ENABLED', True)
        pyautogui.PAUSE = getattr(config, 'PAUSE_BETWEEN_ACTIONS', 0.5)
    
    def execute_action(self, action_data: Dict[str, Any]) -> Optional[str]:
        """
        Execute a GUI action based on action data
        
        Args:
            action_data: Dictionary containing action type and parameters
            
        Returns:
            Optional prompt for next iteration or None to continue
        """
        if not self._validate_action_data(action_data):
            logger.error(f"Invalid action data: {action_data}")
            return None
        
        action = action_data['action']
        self.action_count += 1
        
        try:
            logger.info(f"Executing action: {action}")
            
            # Execute the appropriate action
            if action == 'click':
                return self._execute_click(action_data)
            elif action == 'double_click':
                return self._execute_double_click(action_data)
            elif action == 'right_click':
                return self._execute_right_click(action_data)
            elif action == 'type':
                return self._execute_type(action_data)
            elif action == 'key':
                return self._execute_key(action_data)
            elif action == 'scroll':
                return self._execute_scroll(action_data)
            elif action == 'move_mouse':
                return self._execute_move_mouse(action_data)
            elif action == 'navigate':
                return self._execute_navigate(action_data)
            elif action == 'wait':
                return self._execute_wait(action_data)
            elif action == 'next_prompt':
                return self._execute_next_prompt(action_data)
            elif action == 'complete':
                return self._execute_complete(action_data)
            elif action == 'error':
                return self._execute_error(action_data)
            else:
                logger.error(f"Unknown action: {action}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to execute action {action}: {e}")
            return None
    
    def _validate_action_data(self, action_data: Dict[str, Any]) -> bool:
        """
        Validate action data before execution
        """
        if not isinstance(action_data, dict) or 'action' not in action_data:
            return False
        
        action = action_data['action']
        
        # Validate coordinates for click actions
        if action in ['click', 'double_click', 'right_click', 'move_mouse']:
            if not self._validate_coordinates(action_data.get('x'), action_data.get('y')):
                return False
        
        # Validate scroll parameters
        if action == 'scroll':
            if not self._validate_coordinates(action_data.get('x'), action_data.get('y')):
                return False
            if 'clicks' not in action_data or not isinstance(action_data['clicks'], (int, float)):
                return False
        
        # Validate text input
        if action == 'type':
            if 'text' not in action_data or not isinstance(action_data['text'], str):
                return False
        
        # Validate key input
        if action == 'key':
            if 'key' not in action_data or not isinstance(action_data['key'], str):
                return False
        
        # Validate URL
        if action == 'navigate':
            if 'url' not in action_data or not isinstance(action_data['url'], str):
                return False
        
        # Validate wait time
        if action == 'wait':
            if 'seconds' not in action_data or not isinstance(action_data['seconds'], (int, float)):
                return False
            if action_data['seconds'] < 0 or action_data['seconds'] > 30:
                logger.warning(f"Wait time {action_data['seconds']} is outside safe range (0-30s)")
                return False
        
        return True
    
    def _validate_coordinates(self, x: Any, y: Any) -> bool:
        """
        Validate click coordinates
        """
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(f"Invalid coordinate types: x={type(x)}, y={type(y)}")
            return False
        
        if not (0 <= x <= self.screen_size.width and 0 <= y <= self.screen_size.height):
            logger.error(f"Coordinates ({x}, {y}) outside screen bounds {self.screen_size}")
            return False
        
        # Check safe zones (areas to avoid clicking)
        for zone in self.safe_zones:
            if len(zone) == 4:  # (x1, y1, x2, y2)
                x1, y1, x2, y2 = zone
                if x1 <= x <= x2 and y1 <= y <= y2:
                    logger.warning(f"Coordinates ({x}, {y}) in restricted safe zone")
                    return False
        
        return True
    
    def _execute_click(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute click action"""
        x, y = int(action_data['x']), int(action_data['y'])
        pyautogui.click(x, y)
        logger.info(f"Clicked at ({x}, {y})")
        self.successful_actions += 1
        time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
        return None
    
    def _execute_double_click(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute double click action"""
        x, y = int(action_data['x']), int(action_data['y'])
        pyautogui.doubleClick(x, y)
        logger.info(f"Double-clicked at ({x}, {y})")
        self.successful_actions += 1
        time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
        return None
    
    def _execute_right_click(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute right click action"""
        x, y = int(action_data['x']), int(action_data['y'])
        pyautogui.rightClick(x, y)
        logger.info(f"Right-clicked at ({x}, {y})")
        self.successful_actions += 1
        time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
        return None
    
    def _execute_type(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute type action"""
        text = action_data['text']
        pyautogui.typewrite(text)
        logger.info(f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}")
        self.successful_actions += 1
        time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
        return None
    
    def _execute_key(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute key press action"""
        key = action_data['key']
        
        # Handle key combinations (e.g., "ctrl+c")
        if '+' in key:
            keys = [k.strip() for k in key.split('+')]
            pyautogui.hotkey(*keys)
            logger.info(f"Pressed key combination: {key}")
        else:
            pyautogui.press(key)
            logger.info(f"Pressed key: {key}")
        
        self.successful_actions += 1
        time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
        return None
    
    def _execute_scroll(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute scroll action"""
        x, y = int(action_data['x']), int(action_data['y'])
        clicks = int(action_data['clicks'])
        pyautogui.scroll(clicks, x=x, y=y)
        logger.info(f"Scrolled {clicks} clicks at ({x}, {y})")
        self.successful_actions += 1
        time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
        return None
    
    def _execute_move_mouse(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute mouse move action"""
        x, y = int(action_data['x']), int(action_data['y'])
        pyautogui.moveTo(x, y)
        logger.info(f"Moved mouse to ({x}, {y})")
        self.successful_actions += 1
        time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
        return None
    
    def _execute_navigate(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute navigate action"""
        url = action_data['url']
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            webbrowser.open(url)
            logger.info(f"Opened URL: {url}")
            self.successful_actions += 1
            time.sleep(3)  # Wait for browser to load
            return None
        except Exception as e:
            logger.error(f"Failed to open URL {url}: {e}")
            return None
    
    def _execute_wait(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute wait action"""
        seconds = float(action_data['seconds'])
        logger.info(f"Waiting {seconds} seconds")
        time.sleep(seconds)
        self.successful_actions += 1
        return None
    
    def _execute_next_prompt(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute next prompt action"""
        prompt = action_data.get('prompt', 'Fahre mit dem nächsten Schritt fort.')
        logger.info(f"Next prompt: {prompt}")
        self.successful_actions += 1
        return prompt
    
    def _execute_complete(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute complete action"""
        message = action_data.get('message', 'Aufgabe erfolgreich abgeschlossen')
        logger.info(f"Task completed: {message}")
        self.successful_actions += 1
        return "COMPLETE"
    
    def _execute_error(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Execute error action"""
        message = action_data.get('message', 'Ein Fehler ist aufgetreten')
        logger.error(f"Task error: {message}")
        return "ERROR"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get action execution statistics"""
        return {
            'total_actions': self.action_count,
            'successful_actions': self.successful_actions,
            'success_rate': self.successful_actions / max(self.action_count, 1),
            'screen_size': {'width': self.screen_size.width, 'height': self.screen_size.height}
        }