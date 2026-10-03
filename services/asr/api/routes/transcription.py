from fastapi import APIRouter, HTTPException
from api import dependencies
from api.schemas.transcription import TranscriptionRequestSchema
from infrastructure.storage.http_audio_downloader import HttpAudioDownloader
from infrastructure.storage.file_storage import get_audio_path, delete_audio
from config import settings

router = APIRouter(
    prefix = "/api/v1/transcriptions",
    tags = ["Transcription"],
)

audio_downloader = HttpAudioDownloader()


@router.post("")
async def transcribe(request: TranscriptionRequestSchema):
    if dependencies.transcription_service is None:
        raise HTTPException(
            status_code = 503,
            detail = "Transcription service is not initialized",
        )

    audio_path = get_audio_path(
        request.request_id,
        request.extension
    )

    try:
        await audio_downloader.download(
            audio_url=request.audio_url,
            destination_path=audio_path,
            max_size_bytes=settings.ASR_MAX_UPLOAD_SIZE_MB * 1024 * 1024,

        )

        transcription = dependencies.transcription_service.transcribe(
            request_id=request.request_id,
            audio_path=audio_path,
        )

        return transcription
    
    finally:
        delete_audio(audio_path)