# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY . .
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose Flask port
EXPOSE 8083

# Run the Flask app
CMD ["python", "app.py"]
