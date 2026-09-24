import asyncio

from vlm.ollama_vlm import OllamaVLM
from vlm.prompt_loader import PromptLoader


vlm = OllamaVLM(
    base_url="http://localhost:11434",
    model_name="qwen2.5:7b-instruct",
    temperature=0.0,
    max_tokens=100,
    timeout=120,
    prompt_loader=PromptLoader("prompts/visual_diagnosis.txt"),
)


result = asyncio.run(vlm.health_check())

print(f"Ollama available: {result}")