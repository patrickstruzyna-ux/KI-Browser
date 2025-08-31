#!/usr/bin/env python3
"""
Debug-Test für doppelte Ausgaben
"""

import sys
import time

def test_simple_output():
    """Testet einfache Ausgaben"""
    print("Test 1: Einfache Ausgabe")
    print("Test 2: Weitere Ausgabe")
    sys.stdout.flush()

def test_with_loop():
    """Testet Ausgaben in einer Schleife"""
    for i in range(3):
        print(f"Loop {i}: Test")
        time.sleep(0.1)
        sys.stdout.flush()

def test_with_function_calls():
    """Testet Ausgaben mit Funktionsaufrufen"""
    def inner_function():
        print("Inner function output")
        return "result"
    
    result = inner_function()
    print(f"Result: {result}")

if __name__ == "__main__":
    print("=== Debug Test Start ===")
    test_simple_output()
    print("\n--- Loop Test ---")
    test_with_loop()
    print("\n--- Function Test ---")
    test_with_function_calls()
    print("=== Debug Test Ende ===")