from pathlib import Path


class PromptLoader:

    def __init__(self, prompt_path: str):
        self.prompt_path = Path(prompt_path)

    def load(self) -> str:
        return self.prompt_path.read_text(encoding="utf-8")
