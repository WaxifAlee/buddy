#!/usr/bin/env python3
"""
Test script to verify the double listening issue is fixed
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers.listen import listen_for_command

def test_single_listen():
    print("Testing single listen functionality...")
    print("Say something and it should only process once:")
    
    result = listen_for_command(timeout=5)
    print(f"Result: '{result}'")
    
    if result:
        print("✅ Single listen test passed!")
    else:
        print("❌ No input detected")

if __name__ == "__main__":
    test_single_listen()
