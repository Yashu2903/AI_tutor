from typing import TypedDict, Literal, Optional

class TutorState(TypedDict):
    topic: str
    lesson: Optional[str]
    question: Optional[str]
    answer: Optional[str]
    correct: Optional[bool]
    feedback: Optional[str]
    phase: Literal["teach", "ask", "wait", "evaluate", "decide"]




    