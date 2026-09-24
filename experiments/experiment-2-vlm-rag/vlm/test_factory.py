from vlm.factory import create_vlm


vlm = create_vlm(
    config_path="configs/vlm_config.json",
    prompt_path="prompts/visual_diagnosis.txt",
)

print(type(vlm).__name__)
print(vlm.model_name)
print(vlm.temperature)
