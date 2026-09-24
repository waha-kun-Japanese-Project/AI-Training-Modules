import json

from vlm.diagnosis import VisualDiagnosis


def parse_diagnosis(response: str) -> VisualDiagnosis:
    data = json.loads(response)

    return VisualDiagnosis.model_validate(data)
