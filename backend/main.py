from fastapi import FastAPI, HTTPException
from .schemas import AnswerRequest
from .graph.tutor_graph import build_tutor_graph
from .db.tutor_state import save_state, load_state
from .db.sqlite import init_db
import uuid

app = FastAPI(title="Stateful AI Tutor", description="A simple API for a stateful AI tutor")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

tutor_graph = build_tutor_graph()

@app.post("/tutor/start")
async def start_tutor(topic: str):
    session_id = str(uuid.uuid4())
    initial_state = {
        "topic": topic,
        "lesson": None,
        "question": None,
        "answer": None,
        "correct": None,
        "feedback": None,
        "phase": "teach",
        "difficulty": "easy",
        "mistakes": 0,
        "streak": 0
    }
    state = tutor_graph.invoke(initial_state)
    save_state(session_id, state)
    return {"session_id": session_id, **state}

@app.post("/tutor/answer")
async def submit_answer(request: AnswerRequest):
    state = load_state(request.session_id)

    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state["answer"] = request.answer
    state["phase"] = "evaluate"
    
    new_state = tutor_graph.invoke(state, config={"resume": True})

    save_state(request.session_id, new_state)
    return new_state






