# ===============================
# Dockerfile for Task2_GPP Project
# ===============================

# Use official Python slim image
FROM python:3.11-slim

# -------------------------------
# Set working directory
WORKDIR /app

# -------------------------------
# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Copy application code
COPY . .

# -------------------------------
# Create required folders for seed and cron logs
RUN mkdir -p /data /cron && chmod 755 /data /cron

# -------------------------------
# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
# Create cron directory
RUN mkdir -p /cron

# -------------------------------
# Copy cron file and register with crontab
COPY cron/2fa-cron /etc/cron.d/seed-cron
RUN chmod 0644 /etc/cron.d/seed-cron && crontab /etc/cron.d/seed-cron

# -------------------------------
# Expose port for FastAPI
EXPOSE 8080

# -------------------------------
# Start cron in foreground and run FastAPI app
CMD cron && uvicorn app:app --host 0.0.0.0 --port 8080
