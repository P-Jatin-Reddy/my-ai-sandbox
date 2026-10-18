import os
import sys
from google import genai
from google.genai import types

def run_live_diagnostic():
    # 1. Check for secure environment variable isolation
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY environment variable not found!")
        print("Please verify your windows setx configuration and restart your terminal.")
        sys.exit(1)
        
    print("🔒 Environment Verification: Secure API Key Found.")
    
    # 2. Initialize the modern GenAI Client
    # The client automatically discovers the GEMINI_API_KEY environment variable
    client = genai.Client()
    
    # 3. Define a broken snippet for the model to analyze live
    broken_code = """
def calculate_metrics(data):
    # Intentional bug: executing undefined variable to test error capturing
    result = raw_values * 2 
    return result
"""
    
    print("📡 Sending live execution payload to gemini-3.8-flash...")
    
    try:
        # 4. Generate content using the fast, engineering-optimized model
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=f"Analyze this broken Python code and provide only the corrected function block:\n{broken_code}",
        )
        
        print("\n🏆 Live API Connection Successful! Response Received:")
        print("-" * 50)
        print(response.text)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ API Call Failed: {e}")

if __name__ == "__main__":
    run_live_diagnostic()
