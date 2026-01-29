from pydantic import BaseModel, Field
from typing import Literal, Optional

TutorPhase = Literal["teach", "ask", "wait", "evaluate", "decide"]

class TutorState(BaseModel):
    """Pydantic model for TutorState (used for API validation)."""
    topic: str = Field(..., description="The topic of the tutor")
    phase: TutorPhase = Field(..., description="The phase of the tutor")
    lesson: Optional[str] = Field(None, description="The lesson of the tutor")
    question: Optional[str] = Field(None, description="The question of the tutor")
    answer: Optional[str] = Field(None, description="The student's answer")
    correct: Optional[bool] = Field(None, description="Whether the answer was correct")
    feedback: Optional[str] = Field(None, description="Feedback on the answer")
    difficulty: Literal["easy", "medium", "hard"] = Field("easy", description="Difficulty level")
    mistakes: int = Field(0, description="Number of mistakes made")
    streak: int = Field(0, description="Current streak of correct answers")

class AnswerRequest(BaseModel):
    session_id: str = Field(..., description="The ID of the session")
    answer: str = Field(..., description="The answer to the question")
