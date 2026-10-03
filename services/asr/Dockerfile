FROM python:3.11-slim

WORKDIR /app

COPY services/asr/requirements.txt .

RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY services/asr ./services/asr
COPY shared ./shared

ENV PYTHONUNBUFFERED=1

CMD ["python", "services/asr/main.py"]