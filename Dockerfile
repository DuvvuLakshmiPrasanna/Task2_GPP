# =========================
# Stage 1 - Builder
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target /app/packages


# =========================
# Stage 2 - Runtime
# =========================
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY --from=builder /app/packages /usr/local/lib/python3.11/site-packages

COPY . .

RUN mkdir -p /data && \
    mkdir -p /cron && \
    chmod 755 /data /cron

COPY cronjob /etc/cron.d/seed-cron
RUN chmod 0644 /etc/cron.d/seed-cron && \
    crontab /etc/cron.d/seed-cron

EXPOSE 8080

CMD service cron start && uvicorn app:app --host 0.0.0.0 --port 8080
