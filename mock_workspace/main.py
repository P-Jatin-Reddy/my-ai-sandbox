# Broken Main Controller File
from utils import format_payload

def run_pipeline():
    user_data = "Target User Data"
    # This call will crash due to the bug inside utils.py
    clean_data = format_payload(user_data)
    print(f"Pipeline executed successfully: {clean_data}")

if __name__ == "__main__":
    run_pipeline()
