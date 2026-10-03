from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ==========================================================
    # Service
    # ==========================================================
    SERVICE_NAME: str
    SERVICE_VERSION: str
    SERVICE_ENVIRONMENT: str

    # ==========================================================
    # Model
    # ==========================================================
    MODEL_NAME: str
    MODEL_DEVICE: str
    MODEL_TRUST_REMOTE_CODE: bool

    # ==========================================================
    # Audio
    # ==========================================================
    ASR_MAX_UPLOAD_SIZE_MB: int
    ASR_SUPPORTED_FORMATS: list[str]

    # ==========================================================
    # Storage
    # ==========================================================
    ASR_UPLOAD_DIR: str

    # ==========================================================
    # RabbitMQ
    # ==========================================================
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str
    RABBITMQ_REQUESTS_QUEUE: str
    RABBITMQ_RESULTS_QUEUE: str
    RABBITMQ_PREFETCH_COUNT: int

    # ==========================================================
    # API
    # ==========================================================
    API_HOST: str
    API_PORT: int

    GRPC_HOST: str
    GRPC_PORT: int

    # ==========================================================
    # Pydantic Config
    # ==========================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()


settings = get_settings()