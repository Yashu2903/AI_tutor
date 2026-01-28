from typing import TypedDict, Literal, Optional

class TutorState(TypedDict):
    topic: str
    lesson: Optional[str]
    question: Optional[str]
    phase: Literal["teach", "ask", "wait"]


    