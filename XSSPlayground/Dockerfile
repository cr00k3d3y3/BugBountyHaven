FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082

CMD ["python", "app.py"]
