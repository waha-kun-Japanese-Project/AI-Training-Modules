import base64

import httpx

from vlm.interface import VLMInterface
from vlm.prompt_loader import PromptLoader
from vlm.parser import parse_diagnosis


class OllamaVLM(VLMInterface):

    def __init__(
        self,
        base_url: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
        timeout: int,
        prompt_loader: PromptLoader,
    ):
        self.base_url = base_url
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.prompt_loader = prompt_loader

    async def diagnose(self, image_path: str) -> dict:
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": self.prompt_loader.load(),
                    "images": [image_base64],
                }
            ],
            "stream": False,
            "think": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload,
            )

        response.raise_for_status()

        ollama_response = response.json()

        print("RAW VLM RESPONSE:")
        print(ollama_response["message"]["content"])

        return parse_diagnosis(
            ollama_response["message"]["content"]
        )

    async def health_check(self) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/api/tags"
            )

        response.raise_for_status()

        return True
