FROM python:3.11-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY . /app

# Install Python dependencies
RUN pip install flask && pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 80

# Start the Flask app
CMD ["python", "app.py"]
