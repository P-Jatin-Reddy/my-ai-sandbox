import os
import sys
import re
from google import genai

def aggregate_workspace(workspace_path):
    """Dynamically parses a directory and creates a unified code context map."""
    context_payload = "=== MULTI-FILE WORKSPACE ARCHITECTURE ===\n\n"
    
    if not os.path.exists(workspace_path):
        print(f"❌ Error: Workspace path '{workspace_path}' not found.")
        sys.exit(1)
        
    for root, _, files in os.walk(workspace_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, workspace_path)
                
                context_payload += f"--- START FILE: {relative_path} ---\n"
                context_payload += "```python\n"
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        context_payload += f.read()
                except Exception as e:
                    context_payload += f"# Error reading file contents: {e}\n"
                context_payload += "\n```\n"
                context_payload += f"--- END FILE: {relative_path} ---\n\n"
                
    return context_payload

def deploy_resolved_code(ai_response_text, workspace_folder):
    """Parses structural markdown blocks from the AI and writes them back to disk."""
    print("\n🛠 Automated Resolution Engine Triggered. Parsing response text...")
    
    # Advanced Regex: Detect files wrapped cleanly inside structural markers
    # Matches: --- START FILE: path --- \n ```python \n [CODE] \n ``` \n --- END FILE: path ---
    pattern = r"--- START FILE: (.*?) ---\s*```python\s*(.*?)\s*```\s*--- END FILE: \1 ---"
    matches = re.findall(pattern, ai_response_text, re.DOTALL)
    
    if not matches:
        print("⚠️ Warning: Could not parse explicit file boundary markers from AI response.")
        print("Falling back to standard markdown block identification...")
        # Fallback to general python blocks if structural parsing fails
        fallback_pattern = r"```python\s*(.*?)\s*```"
        fallback_matches = re.findall(fallback_pattern, ai_response_text, re.DOTALL)
        if fallback_matches:
            print(f"Found {len(fallback_matches)} generic Python code blocks. Inspect console output.")
        return

    for relative_path, clean_code in matches:
        target_path = os.path.join(workspace_folder, relative_path.strip())
        print(f"✍️ Writing resolution payload directly to target: {target_path}")
        
        # Safely create any subdirectory paths if needed
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(clean_code.strip() + "\n")
            
    print("🏆 Workspace structural code repair completed successfully!")

def run_agentic_loop():
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ CRITICAL ERROR: GEMINI_API_KEY environment variable not found!")
        sys.exit(1)
        
    print("🔒 Environment Verification: Secure API Key Found.")
    
    workspace_folder = "./mock_workspace"
    print(f"📁 Scanning target workspace directory: '{workspace_folder}'...")
    workspace_context = aggregate_workspace(workspace_folder)
    
    client = genai.Client()
    
    # Tight systemic instructions to force the model to output strict parsing tags
    system_instruction = (
        "You are an expert systems automation agent. Analyze the multi-file workspace below and fix bugs.\n"
        "CRITICAL ASSIGNMENT: You must return the updated content wrapped in explicit boundary tags exactly like this:\n"
        "--- START FILE: relative_path.py ---\n"
        "```python\n"
        "YOUR CORRECTED CODE HERE\n"
        "```\n"
        "--- END FILE: relative_path.py ---\n"
        "Do not omit these tags. Output only the tagged code files that require repairs."
    )
    
    print("📡 Transmitting multi-file workspace payload to gemini-3.8-flash...")
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=f"{system_instruction}\n\nHere is the codebase context:\n{workspace_context}",
        )
        
        # Run the deployment logic back onto the computer files
        deploy_resolved_code(response.text, workspace_folder)
        
    except Exception as e:
        print(f"❌ Core Transmission Failure: {e}")

if __name__ == "__main__":
    run_agentic_loop()
