from config import settings


def validate_extension(extension: str) -> str:
    extension = extension.lower().lstrip(".")

    if extension not in settings.ASR_SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {extension}"
        )

    return extension