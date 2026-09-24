import asyncio

from vlm.factory import create_vlm


IMAGE_PATH = (
    "evaluation/test_images/waha_dataset/"
    "imageoverflow/image10overflow.jpg"
)

vlm = create_vlm(
    config_path="configs/vlm_config.json",
    prompt_path="prompts/visual_diagnosis.txt",
)

result = asyncio.run(
    vlm.diagnose(IMAGE_PATH)
)

print(result.model_dump_json(indent=2))
