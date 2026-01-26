from pydantic import BaseModel, Field
from typing import Literal

TutorPhase = Literal["teach","ask","wait"]

class TutorState(BaseModel):
    topic: str = Field(..., description="The topic of the tutor")
    phase: TutorPhase = Field(..., description="The phase of the tutor")
    lesson: str | None = Field(None, description="The lesson of the tutor")
    question: str | None = Field(None, description="The question of the tutor")

