# 1. Use a lightweight, secure Linux baseline with Python pre-installed
FROM python:3.11-slim

# 2. Establish an isolated working directory inside the container
WORKDIR /app

# 3. Prevent Python from writing buffering outputs to ensure immediate terminal logging
ENV PYTHONUNBUFFERED=1

# 4. Install the official Google Gen AI SDK directly inside the Linux container
RUN pip install --no-cache-dir google-genai

# 5. Copy your local live_agent.py script into the isolated container space
COPY live_agent.py /app/live_agent.py

# 6. Execute the script natively inside the isolated container when it starts
CMD ["python", "live_agent.py"]
