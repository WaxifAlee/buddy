#!/usr/bin/env python3
"""
Test script to verify the double listening issue is fixed
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers.listen import listen_for_command

def test_single_listen():
    print("Testing single listen functionality...", flush=True)
    print("Say something and it should only process once:", flush=True)
    
    result = listen_for_command(timeout=5)
    print(f"Result: '{result}'", flush=True)
    
    if result:
        print("✅ Single listen test passed!", flush=True)
    else:
        print("❌ No input detected", flush=True)

if __name__ == "__main__":
    test_single_listen()
