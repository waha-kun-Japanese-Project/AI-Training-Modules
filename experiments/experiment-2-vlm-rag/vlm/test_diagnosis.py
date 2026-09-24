from vlm.parser import parse_diagnosis


raw_response = """
{
    "problem_type": "pipe_damage",
    "visual_observations": [
        "visible water leakage",
        "damaged pipe section"
    ],
    "affected_component": "irrigation pipe"
}
"""


diagnosis = parse_diagnosis(raw_response)

print(diagnosis.model_dump())