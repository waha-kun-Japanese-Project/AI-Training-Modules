from abc import ABC, abstractmethod


class VLMInterface(ABC):

    @abstractmethod
    async def diagnose(self, image_path: str) -> dict:
        pass
