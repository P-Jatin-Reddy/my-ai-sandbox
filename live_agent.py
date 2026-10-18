import os
import sys
from google import genai

def aggregate_workspace(workspace_path):
    """Dynamically parses a directory and creates a unified code context map."""
    context_payload = "=== MULTI-FILE WORKSPACE ARCHITECTURE ===\n\n"
    
    if not os.path.exists(workspace_path):
        print(f"❌ Error: Workspace path '{workspace_path}' not found.")
        sys.exit(1)
        
    # Walk through all directories and files natively
    for root, _, files in os.walk(workspace_path):
        for file in files:
            if file.endswith('.py'): # Track strictly Python files for now
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, workspace_path)
                
                context_payload += f"--- FILE PATH: {relative_path} ---\n"
                context_payload += "```python\n"
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        context_payload += f.read()
                except Exception as e:
                    context_payload += f"# Error reading file contents: {e}\n"
                context_payload += "\n```\n\n"
                
    return context_payload

def run_agentic_loop():
    # 1. Verify secure credential vault isolation
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ CRITICAL ERROR: GEMINI_API_KEY environment variable not found!")
        sys.exit(1)
        
    print("🔒 Environment Verification: Secure API Key Found.")
    
    # 2. Ingest the multi-file project workspace context dynamically
    workspace_folder = "./mock_workspace"
    print(f"📁 Scanning target workspace directory: '{workspace_folder}'...")
    workspace_context = aggregate_workspace(workspace_folder)
    
    # 3. Initialize the Google Gen AI Client
    client = genai.Client()
    
    # 4. Construct the engineering instruction prompt
    system_instruction = (
        "You are an expert static analysis automated agent. You have been provided the full multi-file "
        "contents of a broken project repository. Analyze the entire repository layout, find the core cross-file "
        "dependency flaws causing errors, and output the fully corrected, functional versions of the files. "
        "Clearly indicate which file path each code block belongs to."
    )
    
    print("📡 Transmitting multi-file workspace payload to gemini-3.8-flash...")
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=f"{system_instruction}\n\nHere is the codebase context:\n{workspace_context}",
        )
        
        print("\n🏆 Global Review Successful! Multi-File Corrections Received:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Core Transmission Failure: {e}")

if __name__ == "__main__":
    run_agentic_loop()
