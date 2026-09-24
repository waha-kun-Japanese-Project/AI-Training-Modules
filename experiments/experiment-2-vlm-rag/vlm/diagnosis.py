from typing import Literal

from pydantic import BaseModel


class VisualDiagnosis(BaseModel):
    problem_type: Literal[
	"normal",
        "blockage",
        "overflow",
        "pipe_damage",
    ]
    visual_observations: list[str]
    affected_component: str
