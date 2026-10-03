import sys
from pathlib import Path

ASR_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = ASR_DIR.parent.parent

sys.path.insert(0, str(ASR_DIR))
sys.path.insert(
    0,
    str(ASR_DIR / "infrastructure" / "grpc" / "generated"),
)
sys.path.insert(0, str(ROOT_DIR))


import grpc
from minio import Minio
from datetime import timedelta

from config import settings
from infrastructure.grpc.generated import asr_pb2, asr_pb2_grpc


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

    request_id = "grpc-test-001"

    request = asr_pb2.TranscriptionRequest(
        request_id=request_id,
        audio_url=audio_url,
        extension=AUDIO_FILE.rsplit(".", 1)[-1],
    )

    print(f"Sending gRPC request: {request_id}")
    print(f"Audio file: {AUDIO_FILE}")

    with grpc.insecure_channel(
        f"localhost:{settings.GRPC_PORT}"
    ) as channel:

        stub = asr_pb2_grpc.ASRServiceStub(channel)

        response = stub.Transcribe(request)

    print()
    print("=" * 60)
    print("gRPC Transcription Result")
    print("=" * 60)
    print(f"Request ID:       {response.request_id}")
    print(f"Status:            {response.status}")
    print(f"Text:              {response.text}")
    print(f"Processing time:   {response.processing_time:.2f} seconds")
    print(f"Error:             {response.error}")
    print("=" * 60)


if __name__ == "__main__":
    main()