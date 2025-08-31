#!/usr/bin/env python3
"""
Enhanced LLM GUI Automation Application
Modular architecture with improved error handling and performance
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import Config
from core.llm_manager import LLMManager
from core.screenshot_manager import ScreenshotManager
from core.action_executor import ActionExecutor
from core.exceptions import (
    LLMAutomationError, ConfigurationError, ProviderUnavailableError,
    MaxIterationsError, JSONParsingError, ActionValidationError
)
from utils.json_parser import RobustJSONParser

class EnhancedLLMAutomationApp:
    """
    Enhanced LLM GUI Automation Application with modular architecture
    """
    
    def __init__(self, provider: str = None):
        """Initialize the enhanced automation application"""
        self.config = Config()
        self.setup_logging()
        
        # Validate configuration
        validation_status = Config.validate_config()
        if not all(validation_status.values()):
            failed_validations = [k for k, v in validation_status.items() if not v]
            raise ConfigurationError(f"Configuration validation failed: {failed_validations}")
        
        # Initialize components
        self.llm_manager = LLMManager(self.config)
        if provider:
            self.llm_manager.switch_provider(provider)
        self.screenshot_manager = ScreenshotManager(
            cache_size=self.config.SCREENSHOT_CACHE_SIZE,
            compression_quality=85,
            resize_factor=0.8
        )
        self.action_executor = ActionExecutor(self.config)
        self.json_parser = RobustJSONParser()
        
        # Application state
        self.iteration_count = 0
        self.session_stats = {
            'start_time': time.time(),
            'total_actions': 0,
            'successful_actions': 0,
            'llm_requests': 0,
            'screenshots_taken': 0,
            'errors': []
        }
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Enhanced LLM Automation App initialized")
        self.logger.info(f"Available providers: {self.llm_manager.get_available_providers()}")
    
    def setup_logging(self):
        """Setup enhanced logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format=self.config.LOG_FORMAT,
            handlers=[
                logging.FileHandler(self.config.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for the LLM"""
        return """
Du bist ein KI-Assistent für GUI-Automatisierung. Du kannst Screenshots analysieren und Aktionen ausführen.

Verfügbare Aktionen:
1. click - Klicke auf eine Position: {"action": "click", "x": 100, "y": 200}
2. double_click - Doppelklick: {"action": "double_click", "x": 100, "y": 200}
3. right_click - Rechtsklick: {"action": "right_click", "x": 100, "y": 200}
4. type - Text eingeben: {"action": "type", "text": "Hallo Welt"}
5. key - Taste drücken: {"action": "key", "key": "enter"} oder {"action": "key", "key": "ctrl+c"}
6. scroll - Scrollen: {"action": "scroll", "x": 500, "y": 300, "clicks": -3}
7. move_mouse - Maus bewegen: {"action": "move_mouse", "x": 100, "y": 200}
8. navigate - URL öffnen: {"action": "navigate", "url": "https://example.com"}
9. wait - Warten: {"action": "wait", "seconds": 2}
10. next_prompt - Nächste Anweisung anfordern: {"action": "next_prompt", "prompt": "Beschreibung"}
11. complete - Aufgabe abgeschlossen: {"action": "complete", "message": "Erfolgreich"}
12. error - Fehler melden: {"action": "error", "message": "Fehlerbeschreibung"}

WICHTIG:
- Antworte IMMER mit gültigem JSON
- Analysiere den Screenshot sorgfältig
- Verwende präzise Koordinaten
- Bei Unsicherheit verwende 'next_prompt' für weitere Anweisungen
- Bei Problemen verwende 'error' mit Beschreibung
- Bei erfolgreicher Aufgabenerledigung verwende 'complete'
"""
    
    def run_automation(self, user_prompt: str) -> bool:
        """Run the automation process with enhanced error handling"""
        try:
            self.logger.info(f"Starting automation with prompt: {user_prompt[:100]}...")
            current_prompt = user_prompt
            
            while self.iteration_count < self.config.MAX_ITERATIONS:
                self.iteration_count += 1
                self.logger.info(f"Iteration {self.iteration_count}/{self.config.MAX_ITERATIONS}")
                
                try:
                    # Take screenshot
                    screenshot_path = self.screenshot_manager.get_screenshot()
                    if not screenshot_path:
                        raise LLMAutomationError("Failed to capture screenshot")
                    
                    self.session_stats['screenshots_taken'] += 1
                    
                    # Send to LLM
                    system_prompt = self.create_system_prompt()
                    full_prompt = f"{system_prompt}\n\nUser: {current_prompt}"
                    
                    # Convert screenshot to base64
                    import base64
                    with open(screenshot_path, 'rb') as img_file:
                        image_b64 = base64.b64encode(img_file.read()).decode('utf-8')
                    
                    self.logger.debug(f"Sending request to LLM with prompt length: {len(full_prompt)}")
                    self.logger.debug(f"Image base64 length: {len(image_b64)}")
                    
                    response = self.llm_manager.send_request(
                        prompt=full_prompt,
                        image_b64=image_b64
                    )
                    
                    self.logger.debug(f"LLM response received: {response is not None}")
                    if response:
                        self.logger.debug(f"Response length: {len(str(response))}")
                    
                    if not response:
                        raise LLMAutomationError("No response from LLM")
                    
                    self.session_stats['llm_requests'] += 1
                    
                    # Parse JSON response
                    try:
                        action_data = self.json_parser.parse_json(response)
                        if not self.json_parser.validate_action(action_data):
                            raise ActionValidationError("Invalid action data", action_data)
                    except Exception as e:
                        raise JSONParsingError(f"Failed to parse LLM response: {e}", response)
                    
                    # Execute action
                    result = self.action_executor.execute_action(action_data)
                    self.session_stats['total_actions'] += 1
                    
                    if result == "COMPLETE":
                        self.logger.info("Task completed successfully")
                        self.session_stats['successful_actions'] += 1
                        return True
                    elif result == "ERROR":
                        error_msg = action_data.get('message', 'Unknown error')
                        self.logger.error(f"Task failed: {error_msg}")
                        self.session_stats['errors'].append(error_msg)
                        return False
                    elif result:
                        # Next prompt provided
                        current_prompt = result
                        self.logger.info(f"Continuing with new prompt: {current_prompt[:50]}...")
                    
                    self.session_stats['successful_actions'] += 1
                    
                    # Add delay between iterations
                    time.sleep(self.config.DELAY_BETWEEN_ACTIONS)
                    
                except (JSONParsingError, ActionValidationError) as e:
                    self.logger.error(f"Iteration {self.iteration_count} failed: {e}")
                    self.session_stats['errors'].append(str(e))
                    
                    # Try to continue with a recovery prompt
                    current_prompt = f"Es gab einen Fehler: {e}. Bitte analysiere den aktuellen Screenshot und fahre fort."
                    continue
                    
                except Exception as e:
                    self.logger.error(f"Unexpected error in iteration {self.iteration_count}: {e}")
                    self.session_stats['errors'].append(str(e))
                    
                    # Try to recover
                    if self.iteration_count < self.config.MAX_ITERATIONS - 1:
                        current_prompt = "Bitte analysiere den aktuellen Screenshot und fahre mit der Aufgabe fort."
                        continue
                    else:
                        break
            
            # Max iterations reached
            raise MaxIterationsError(
                f"Maximum iterations ({self.config.MAX_ITERATIONS}) reached without completion",
                self.iteration_count
            )
            
        except KeyboardInterrupt:
            self.logger.info("Automation interrupted by user")
            return False
        except Exception as e:
            self.logger.error(f"Automation failed: {e}")
            self.session_stats['errors'].append(str(e))
            return False
        finally:
            self._log_session_summary()
    
    def _log_session_summary(self):
        """Log session statistics and summary"""
        duration = time.time() - self.session_stats['start_time']
        
        self.logger.info("=== Session Summary ===")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Iterations: {self.iteration_count}")
        self.logger.info(f"Screenshots taken: {self.session_stats['screenshots_taken']}")
        self.logger.info(f"LLM requests: {self.session_stats['llm_requests']}")
        self.logger.info(f"Total actions: {self.session_stats['total_actions']}")
        self.logger.info(f"Successful actions: {self.session_stats['successful_actions']}")
        
        if self.session_stats['total_actions'] > 0:
            success_rate = self.session_stats['successful_actions'] / self.session_stats['total_actions']
            self.logger.info(f"Action success rate: {success_rate:.2%}")
        
        if self.session_stats['errors']:
            self.logger.info(f"Errors encountered: {len(self.session_stats['errors'])}")
            for i, error in enumerate(self.session_stats['errors'][-5:], 1):  # Show last 5 errors
                self.logger.info(f"  {i}. {error}")
        
        # Log component statistics
        llm_stats = self.llm_manager.get_all_provider_stats()
        action_stats = self.action_executor.get_stats()
        screenshot_stats = self.screenshot_manager.get_cache_stats()
        
        self.logger.info("=== Component Statistics ===")
        self.logger.info(f"LLM Manager: {llm_stats}")
        self.logger.info(f"Action Executor: {action_stats}")
        self.logger.info(f"Screenshot Manager: {screenshot_stats}")

def select_provider(config: Config) -> str:
    """Select the best available LLM provider"""
    validation_status = config.validate_config()
    
    if validation_status.get('openrouter_available', False):
        return 'openrouter'
    elif validation_status.get('google_available', False):
        return 'google'
    else:
        raise ProviderUnavailableError("No LLM providers available. Please configure API keys.")

def main():
    """Main entry point with enhanced argument parsing and error handling"""
    parser = argparse.ArgumentParser(
        description='Enhanced LLM GUI Automation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Öffne Google und suche nach Python"
  python main.py --provider google "Navigiere zu Wikipedia"
  python main.py --validate-config
        """
    )
    
    parser.add_argument(
        'prompt',
        nargs='?',
        help='The task prompt for the automation'
    )
    
    parser.add_argument(
        '--provider',
        choices=['openrouter', 'google', 'auto'],
        default='auto',
        help='LLM provider to use (default: auto-select)'
    )
    
    parser.add_argument(
        '--validate-config',
        action='store_true',
        help='Validate configuration and exit'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Override log level'
    )
    
    parser.add_argument(
        '--max-iterations',
        type=int,
        help='Override maximum iterations'
    )
    
    args = parser.parse_args()
    
    try:
        # Load and validate configuration
        config = Config()
        
        # Override config with command line arguments
        if args.log_level:
            config.LOG_LEVEL = args.log_level
        if args.max_iterations:
            config.MAX_ITERATIONS = args.max_iterations
        
        # Validate configuration if requested
        if args.validate_config:
            validation_status = config.validate_config()
            print("Configuration Validation Results:")
            for key, value in validation_status.items():
                status = "✓" if value else "✗"
                print(f"  {status} {key}: {value}")
            
            if all(validation_status.values()):
                print("\n✓ Configuration is valid")
                return 0
            else:
                print("\n✗ Configuration has issues")
                return 1
        
        # Require prompt if not validating config
        if not args.prompt:
            parser.error("Prompt is required unless using --validate-config")
        
        # Select provider
        if args.provider == 'auto':
            provider = select_provider(config)
            print(f"Auto-selected provider: {provider}")
        else:
            provider = args.provider
        
        # Initialize and run application
        app = EnhancedLLMAutomationApp(provider=provider)
        
        print(f"Starting automation with provider: {provider}")
        print(f"Task: {args.prompt}")
        print("Press Ctrl+C to stop\n")
        
        success = app.run_automation(args.prompt)
        
        if success:
            print("\n✓ Automation completed successfully")
            return 0
        else:
            print("\n✗ Automation failed or was interrupted")
            return 1
            
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        print("Please check your .env file and API keys")
        return 1
    except ProviderUnavailableError as e:
        print(f"Provider Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nAutomation interrupted by user")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.exception("Unexpected error in main")
        return 1

if __name__ == "__main__":
    sys.exit(main())
