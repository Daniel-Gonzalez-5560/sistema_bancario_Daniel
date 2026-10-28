FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BANK_DB_PATH=/data/sistema_bancario.db

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data

EXPOSE 8550

CMD ["sh", "-c", "if [ ! -f \"$BANK_DB_PATH\" ]; then cp /app/sistema_bancario.db \"$BANK_DB_PATH\"; fi; exec python main.py"]
