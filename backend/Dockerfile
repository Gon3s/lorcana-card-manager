# Backend Dockerfile for FastAPI application

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for uploads and database
RUN mkdir -p /app/uploads /app/data

# Expose port
EXPOSE 8000

# Start the application (migrations can be run manually with docker-compose exec)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
