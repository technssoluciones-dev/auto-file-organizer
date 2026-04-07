FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY config/ ./config/
RUN useradd --create-home --shell /bin/bash organizer && chown -R organizer:organizer /app
RUN mkdir -p /app/logs && chown organizer:organizer /app/logs   # ← NUEVA LÍNEA
USER organizer
CMD ["python", "-m", "src.organizer", "--config", "config/settings.json"]