import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    VLM_BASE_URL: str = os.getenv(
        "VLM_BASE_URL",
        "http://localhost:11434",
    )


settings = Settings()
