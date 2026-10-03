import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
GENERATED_DIR = Path(__file__).resolve().parent / "infrastructure" / "grpc" / "generated"

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(GENERATED_DIR))

import asyncio
import threading

import aio_pika
import uvicorn

from config import settings
from shared.logging.logger import logger

from infrastructure.models.qwen_asr import QwenASR
from infrastructure.messaging.rabbitmq_consumer import RabbitMQConsumer
from infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from infrastructure.storage.http_audio_downloader import HttpAudioDownloader
from infrastructure.grpc.server import create_grpc_server
from application.services.transcription_service import TranscriptionService

from api import dependencies
from api.app import app


def start_api():
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
    )

def start_grpc(
    transcription_service: TranscriptionService,
    audio_downloader: HttpAudioDownloader,
):
    server = create_grpc_server(
        transcription_service=transcription_service,
        audio_downloader=audio_downloader,
        host=settings.GRPC_HOST,
        port=settings.GRPC_PORT,
    )

    server.start()

    logger.info(
        f"gRPC server started on "
        f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
    )

    server.wait_for_termination()


def create_transcription_service() -> TranscriptionService:
    asr_model = QwenASR()
    return TranscriptionService(asr_model)


async def main():
    connection = None

    try:
        transcription_service = create_transcription_service()
        dependencies.transcription_service = transcription_service

        api_thread = threading.Thread(
            target=start_api,
            daemon=True,
        )
        api_thread.start()

        audio_downloader = HttpAudioDownloader()

        grpc_thread = threading.Thread(
            target=start_grpc,
            args=(
                transcription_service,
                audio_downloader,
            ),
            daemon=True,
        )
        grpc_thread.start()

        logger.info("Connecting to RabbitMQ...")

        connection: aio_pika.abc.AbstractRobustConnection = (
            await aio_pika.connect_robust(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                login=settings.RABBITMQ_USER,
                password=settings.RABBITMQ_PASSWORD,
                virtualhost=settings.RABBITMQ_VHOST,
            )
        )

        channel: aio_pika.abc.AbstractChannel = (
            await connection.channel()
        )

        await channel.set_qos(
            prefetch_count=settings.RABBITMQ_PREFETCH_COUNT
        )

        requests_queue: aio_pika.abc.AbstractQueue = (
            await channel.get_queue(
                settings.RABBITMQ_REQUESTS_QUEUE,
                ensure=False,
            )
        )

        await channel.declare_queue(
            settings.RABBITMQ_RESULTS_QUEUE,
            durable=True,
            auto_delete=False,
        )

        logger.info("RabbitMQ connected successfully.")

        publisher = RabbitMQPublisher(channel)

        consumer = RabbitMQConsumer(
            transcription_service=transcription_service,
            publisher=publisher,
            queue=requests_queue,
            audio_downloader=audio_downloader,
        )

        await consumer.start()

    finally:
        if connection is not None:
            logger.info("Closing RabbitMQ connection...")
            await connection.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("ASR Service stopped.")