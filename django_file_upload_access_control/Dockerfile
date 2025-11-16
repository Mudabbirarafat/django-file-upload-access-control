
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Create media directory
RUN mkdir -p /app/uploaded_media

EXPOSE 8000

CMD ["gunicorn", "file_share.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
