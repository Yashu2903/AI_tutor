from fastapi import FastAPI, HTTPException
from .schemas import TutorState
from .services.tutor import teach, ask_question

app = FastAPI(title="Stateful AI Tutor", description="A simple API for a stateful AI tutor")

@app.post("start_tutor", response_model=TutorState)
async def start_tutor(topic: str) -> TutorState:
    
    lesson = teach(topic)
    question = ask_question(topic)

    return TutorState(topic=topic, phase="wait", lesson=lesson, question=question)




