from configs.loader import load_vlm_config
from vlm.ollama_vlm import OllamaVLM
from vlm.prompt_loader import PromptLoader
from configs.settings import settings


def create_vlm(
    config_path: str,
    prompt_path: str,
) -> OllamaVLM:
    config = load_vlm_config(config_path)

    prompt_loader = PromptLoader(prompt_path)

    return OllamaVLM(
        base_url=settings.VLM_BASE_URL,
        model_name=config["model_name"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        timeout=config["timeout"],
        prompt_loader=prompt_loader,
    )
