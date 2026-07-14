# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# system deps needed by psycopg2 and scientific packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs instance app/ml/saved_models

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

CMD ["python", "wsgi.py"]