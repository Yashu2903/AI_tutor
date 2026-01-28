from fastapi import FastAPI, HTTPException
from .schemas import TutorState
from .services.tutor import teach, ask_question
from .graph.tutor_graph import build_tutor_graph

app = FastAPI(title="Stateful AI Tutor", description="A simple API for a stateful AI tutor")

tutor_graph = build_tutor_graph()

@app.post("/tutor/start")
async def start_tutor(topic: str) -> TutorState:
    state = {"topic": topic, "phase": "teach", "lesson": None, "question": None}
    return tutor_graph.invoke(state)





