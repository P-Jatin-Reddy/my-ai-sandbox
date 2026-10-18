# Broken Utility File
def format_payload(raw_input):
    # Intentional Bug: string concatenation error with integer
    processed = raw_input + 500
    return processed
