import aio_pika
import json
from domain.entities.transcription import Transcription
from config import settings
from shared.logging import get_logger
logger = get_logger(__name__)

class RabbitMQPublisher:

    def __init__(self, channel: aio_pika.abc.AbstractChannel):
        self.channel = channel

    async def publish(self, transcription: Transcription) -> None:

        logger.info(f"Channel closed: {self.channel.is_closed}")

        message = {
            "request_id": transcription.request_id,
            "status": transcription.status.value,
            "text": transcription.text,
            "processing_time": transcription.processing_time,
            "error": transcription.error
        }

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message, ensure_ascii=False).encode("utf-8"),
                correlation_id = transcription.request_id,
                content_type = "application/json"
            ),
            routing_key = settings.RABBITMQ_RESULTS_QUEUE,
        )

        logger.info(
            f"Transcription result published for request: {transcription.request_id}"
        )