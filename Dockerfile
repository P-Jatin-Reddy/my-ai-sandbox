FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir google-genai

# COPY THE RAW FILES AND THE MOCK WORKSPACE INTO THE SANDBOX
COPY live_agent.py /app/live_agent.py
COPY mock_workspace /app/mock_workspace

CMD ["python", "live_agent.py"]
