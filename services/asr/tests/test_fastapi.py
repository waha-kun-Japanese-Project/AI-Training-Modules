import sys
from pathlib import Path

ASR_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = ASR_DIR.parent.parent

sys.path.insert(0, str(ASR_DIR))
sys.path.insert(0, str(ROOT_DIR))

import httpx
from datetime import timedelta
from minio import Minio

from config import settings


AUDIO_FILE = "audio2878.wav"
MINIO_BUCKET = "asr-audio"
MINIO_HOST = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"


def generate_presigned_url() -> str:
    minio_client = Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )

    return minio_client.presigned_get_object(
        MINIO_BUCKET,
        AUDIO_FILE,
        expires=timedelta(minutes=15),
    )


def main():
    audio_url = generate_presigned_url()
    request_id = "fastapi-test-001"

    payload = {
        "request_id": request_id,
        "audio_url": audio_url,
        "extension": AUDIO_FILE.rsplit(".", 1)[-1],
    }

    print(f"Sending FastAPI request: {request_id}")
    print(f"Audio file: {AUDIO_FILE}")

    with httpx.Client(
        base_url=f"http://localhost:{settings.API_PORT}",
        timeout=None,
    ) as client:

        response = client.post(
            "/api/v1/transcriptions",
            json=payload,
        )

    print()
    print("=" * 60)
    print("FastAPI Transcription Result")
    print("=" * 60)

    print(f"HTTP status:      {response.status_code}")

    response.raise_for_status()

    result = response.json()

    print(f"Request ID:       {result['request_id']}")
    print(f"Status:            {result['status']}")
    print(f"Text:              {result['text']}")
    print(f"Processing time:   {result['processing_time']:.2f} seconds")
    print(f"Error:             {result['error']}")
    print("=" * 60)


if __name__ == "__main__":
    main()