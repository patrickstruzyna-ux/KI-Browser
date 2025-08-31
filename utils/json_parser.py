import json
import re
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class RobustJSONParser:
    """
    Robust JSON parser for LLM responses with multiple fallback strategies
    """
    
    @staticmethod
    def parse_llm_response(content: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from LLM response with multiple fallback strategies
        
        Args:
            content: Raw content from LLM
            
        Returns:
            Parsed JSON dictionary or None if parsing fails
        """
        if not content or not isinstance(content, str):
            logger.error("Invalid content provided for JSON parsing")
            return None
        
        content = content.strip()
        
        # Strategy 1: Direct JSON parsing
        result = RobustJSONParser._try_direct_parse(content)
        if result:
            return result
        
        # Strategy 2: Extract JSON from code blocks
        result = RobustJSONParser._extract_from_code_blocks(content)
        if result:
            return result
        
        # Strategy 3: Find JSON objects in text
        result = RobustJSONParser._find_json_in_text(content)
        if result:
            return result
        
        # Strategy 4: Brace counting method
        result = RobustJSONParser._extract_with_brace_counting(content)
        if result:
            return result
        
        # Strategy 5: Regex-based extraction
        result = RobustJSONParser._extract_with_regex(content)
        if result:
            return result
        
        logger.error(f"Failed to parse JSON from content: {content[:200]}...")
        return None
    
    @staticmethod
    def _try_direct_parse(content: str) -> Optional[Dict[str, Any]]:
        """
        Try direct JSON parsing
        """
        try:
            result = json.loads(content)
            if isinstance(result, dict):
                logger.debug("Successfully parsed JSON directly")
                return result
        except json.JSONDecodeError:
            pass
        return None
    
    @staticmethod
    def _extract_from_code_blocks(content: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON from markdown code blocks
        """
        # Look for ```json or ``` code blocks
        patterns = [
            r'```json\s*\n([^`]+)\n?```',
            r'```\s*\n([^`]+)\n?```',
            r'`([^`]+)`'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                result = RobustJSONParser._try_direct_parse(match.strip())
                if result:
                    logger.debug("Successfully extracted JSON from code block")
                    return result
        
        return None
    
    @staticmethod
    def _find_json_in_text(content: str) -> Optional[Dict[str, Any]]:
        """
        Find JSON objects within text by looking for lines that start with {
        """
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('{'):
                # Try parsing this line and subsequent lines
                for j in range(i, len(lines)):
                    json_candidate = '\n'.join(lines[i:j+1]).strip()
                    result = RobustJSONParser._try_direct_parse(json_candidate)
                    if result:
                        logger.debug("Successfully found JSON in text")
                        return result
        
        return None
    
    @staticmethod
    def _extract_with_brace_counting(content: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON using brace counting to find complete objects
        """
        start_idx = content.find('{')
        if start_idx == -1:
            return None
        
        brace_count = 0
        in_string = False
        escape_next = False
        
        for i in range(start_idx, len(content)):
            char = content[i]
            
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\' and in_string:
                escape_next = True
                continue
            
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
            
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    
                    if brace_count == 0:
                        # Found complete JSON object
                        json_str = content[start_idx:i+1]
                        result = RobustJSONParser._try_direct_parse(json_str)
                        if result:
                            logger.debug("Successfully extracted JSON with brace counting")
                            return result
                        break
        
        return None
    
    @staticmethod
    def _extract_with_regex(content: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON using regex patterns for common LLM response formats
        """
        patterns = [
            # Action pattern: {"action": "...", ...}
            r'\{\s*["\']action["\']\s*:\s*["\'][^"\'}]+["\'][^}]*\}',
            # General JSON object pattern
            r'\{[^{}]*\}',
            # Nested JSON pattern (simple)
            r'\{[^{}]*\{[^{}]*\}[^{}]*\}'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                result = RobustJSONParser._try_direct_parse(match)
                if result:
                    logger.debug("Successfully extracted JSON with regex")
                    return result
        
        return None
    
    @staticmethod
    def validate_action_data(data: Dict[str, Any]) -> bool:
        """
        Validate that parsed data contains required action fields
        
        Args:
            data: Parsed JSON data
            
        Returns:
            True if data is valid action data
        """
        if not isinstance(data, dict):
            return False
        
        # Must have 'action' field
        if 'action' not in data:
            logger.warning("Missing 'action' field in parsed data")
            return False
        
        action = data['action']
        if not isinstance(action, str):
            logger.warning("'action' field must be a string")
            return False
        
        # Validate action-specific requirements
        valid_actions = {
            'click': ['x', 'y'],
            'double_click': ['x', 'y'],
            'right_click': ['x', 'y'],
            'type': ['text'],
            'key': ['key'],
            'scroll': ['x', 'y', 'clicks'],
            'move_mouse': ['x', 'y'],
            'navigate': ['url'],
            'wait': ['seconds'],
            'next_prompt': ['prompt'],
            'complete': [],
            'error': ['message']
        }
        
        if action not in valid_actions:
            logger.warning(f"Unknown action: {action}")
            return False
        
        # Check required fields for specific actions
        required_fields = valid_actions[action]
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field '{field}' for action '{action}'")
                return False
        
        logger.debug(f"Validated action data: {action}")
        return True
    
    @staticmethod
    def extract_multiple_json_objects(content: str) -> List[Dict[str, Any]]:
        """
        Extract multiple JSON objects from content
        
        Args:
            content: Raw content that may contain multiple JSON objects
            
        Returns:
            List of parsed JSON objects
        """
        objects = []
        
        # Try to find multiple JSON objects
        start_positions = []
        for i, char in enumerate(content):
            if char == '{':
                start_positions.append(i)
        
        for start_pos in start_positions:
            remaining_content = content[start_pos:]
            result = RobustJSONParser._extract_with_brace_counting(remaining_content)
            if result and RobustJSONParser.validate_action_data(result):
                objects.append(result)
        
        return objects