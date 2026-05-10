FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir fastapi uvicorn requests beautifulsoup4 apscheduler openai scikit-learn pydantic python-dotenv feedparser pandas numpy markdown PyYAML loguru supabase pydantic-settings

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

RUN pip install --no-cache-dir jieba dashscope

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]