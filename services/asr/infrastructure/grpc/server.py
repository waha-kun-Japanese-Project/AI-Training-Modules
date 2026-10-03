import asyncio
import grpc

from concurrent import futures

from shared.logging import get_logger

from config import settings

from application.services.transcription_service import (
    TranscriptionService,
)

from domain.entities.transcription import (
    Transcription,
    TranscriptionStatus,
)

from infrastructure.grpc.generated import (
    asr_pb2,
    asr_pb2_grpc,
)

from infrastructure.storage.http_audio_downloader import (
    HttpAudioDownloader,
)

from infrastructure.storage.file_storage import delete_audio


logger = get_logger(__name__)


class ASRServicer(asr_pb2_grpc.ASRServiceServicer):

    def __init__(
        self,
        transcription_service: TranscriptionService,
        audio_downloader: HttpAudioDownloader,
    ):
        self.transcription_service = transcription_service
        self.audio_downloader = audio_downloader

    def Transcribe(
        self,
        request: asr_pb2.TranscriptionRequest,
        context: grpc.ServicerContext,
    ) -> asr_pb2.TranscriptionResponse:

        logger.info(
            f"Received gRPC transcription request: "
            f"{request.request_id}"
        )

        audio_path = None

        try:
            audio_path = self._download_audio(request)

            transcription = self.transcription_service.transcribe(
                request_id=request.request_id,
                audio_path=audio_path,
            )

            return self._build_response(transcription)

        except Exception as exc:

            logger.exception(
                f"gRPC transcription failed: "
                f"{request.request_id}"
            )

            return asr_pb2.TranscriptionResponse(
                request_id=request.request_id,
                status=asr_pb2.FAILED,
                error=str(exc),
            )

        finally:

            if audio_path is not None:
                delete_audio(audio_path)

    def _download_audio(
        self,
        request: asr_pb2.TranscriptionRequest,
    ) -> str:

        destination_path = (
            f"{settings.ASR_UPLOAD_DIR}/"
            f"{request.request_id}.{request.extension}"
        )

        max_size_bytes = (
            settings.ASR_MAX_UPLOAD_SIZE_MB
            * 1024
            * 1024
        )

        return asyncio.run(
            self.audio_downloader.download(
                audio_url=request.audio_url,
                destination_path=destination_path,
                max_size_bytes=max_size_bytes,
            )
        )

    @staticmethod
    def _build_response(
        transcription: Transcription,
    ) -> asr_pb2.TranscriptionResponse:

        status_mapping = {
            TranscriptionStatus.PENDING: asr_pb2.PENDING,
            TranscriptionStatus.PROCESSING: asr_pb2.PROCESSING,
            TranscriptionStatus.COMPLETED: asr_pb2.COMPLETED,
            TranscriptionStatus.FAILED: asr_pb2.FAILED,
        }

        return asr_pb2.TranscriptionResponse(
            request_id=transcription.request_id,
            status=status_mapping[transcription.status],
            text=transcription.text or "",
            processing_time=transcription.processing_time or 0.0,
            error=transcription.error or "",
        )


def create_grpc_server(
    transcription_service: TranscriptionService,
    audio_downloader: HttpAudioDownloader,
    host: str,
    port: int,
) -> grpc.Server:

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    asr_pb2_grpc.add_ASRServiceServicer_to_server(
        ASRServicer(
            transcription_service=transcription_service,
            audio_downloader=audio_downloader,
        ),
        server,
    )

    server.add_insecure_port(
        f"{host}:{port}"
    )

    return server