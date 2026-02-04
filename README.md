# Stateful AI Tutor

A stateful AI tutor that teaches a topic, asks questions, and adapts difficulty based on your answers. The backend uses **LangGraph** for a teach → ask → evaluate → decide workflow, with session state persisted in SQLite.

## Features

- **Adaptive tutoring**: Teaches a topic, then asks questions to check understanding.
- **Difficulty levels**: Starts at "easy"; increases to "medium" and "hard" after correct-answer streaks; resets to "easy" after repeated mistakes.
- **Persistent sessions**: Each session is stored by `session_id` so you can resume or integrate with other clients.
- **State-driven UI**: Streamlit frontend uses `st.session_state.tutor_state` as the single source of truth—no rendering directly from API responses.
- **LLM-powered**: Lessons, questions, and evaluation use **Ollama** (e.g. `llama3.1`).

## Tech Stack

| Layer      | Technology        |
|-----------|-------------------|
| Backend   | FastAPI, LangGraph |
| LLM       | Ollama (llama3.1)  |
| Database  | SQLite             |
| Frontend  | Streamlit          |

## Project Structure

```
Stateful_AI_tutor/
├── backend/
│   ├── main.py           # FastAPI app, /tutor/start and /tutor/answer
│   ├── schemas.py        # Pydantic models (AnswerRequest, etc.)
│   ├── db/
│   │   ├── sqlite.py     # DB connection, init_db, tutor_sessions table
│   │   └── tutor_state.py # save_state, load_state
│   ├── graph/
│   │   ├── state.py      # TutorState TypedDict
│   │   ├── nodes.py      # teach, ask, wait, evaluate, decide nodes
│   │   └── tutor_graph.py # StateGraph build and compile
│   └── services/
│       ├── llm.py        # Ollama generate_reply (llama3.1)
│       ├── tutor.py      # teach(), ask_question()
│       └── evaluator.py  # evaluate_answer() → {correct, feedback}
├── frontend/
│   └── app.py            # Streamlit UI (state-driven)
├── data/                 # SQLite DB (created at runtime, gitignored)
└── README.md
```

## Prerequisites

- **Python 3.10+**
- **Ollama** installed and running, with the **llama3.1** model pulled:
  ```bash
  ollama pull llama3.1
  ollama serve   # if not already running
  ```

## Installation

1. Clone or download the project and go to its root:
   ```bash
   cd Stateful_AI_tutor
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS/Linux
   pip install fastapi uvicorn langgraph ollama streamlit requests pydantic
   ```

3. Ensure Ollama is running and `llama3.1` is available.

## Running the App

### 1. Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

### 2. Start the frontend

In another terminal:

```bash
streamlit run frontend/app.py
```

- UI: `http://localhost:8501`

### 3. Use the tutor

1. Enter a topic and click **Start**.
2. Read the lesson and question.
3. Type your answer and click **Submit answer**.
4. See feedback (✅/❌) and the next question; difficulty and streak are shown in the status line.

## API Overview

| Method | Endpoint        | Description |
|--------|-----------------|-------------|
| POST   | `/tutor/start`  | Start a session. Query: `topic`. Returns `session_id` and initial state (lesson, question, etc.). |
| POST   | `/tutor/answer` | Submit an answer. Body: `{ "session_id": "...", "answer": "..." }`. Returns updated state (feedback, next question, difficulty, streak). |

Session state is persisted in SQLite (`data/tutor.db`). The graph runs until the **wait** node (after “ask”); when you submit an answer, the backend resumes from **evaluate** → **decide** → either **ask** (next question) or **teach** (re-teach after too many mistakes).

## How the Tutor Flow Works (LangGraph)

1. **teach** – Generate a lesson for the topic at current difficulty.
2. **ask** – Generate a question; may increase difficulty if streak ≥ 2.
3. **wait** – *Interrupt*: wait for user answer (frontend sends it to `/tutor/answer`).
4. **evaluate** – LLM evaluates the answer; update `correct`, `feedback`, `mistakes`, `streak`.
5. **decide** – If `mistakes >= 2` → **teach** (reset difficulty); else → **ask** (next question).

State (topic, lesson, question, answer, correct, feedback, phase, difficulty, mistakes, streak) is stored per `session_id` and passed through the graph.

## Frontend Behavior

- **Single source of truth**: All visible content comes from `st.session_state.tutor_state`.
- **Session IDs**: `st.session_state.tutor_session_id` holds the current session; API responses only update `tutor_state` and (on start) `tutor_session_id`.
- **Order**: Lesson → Feedback (if any) → Question; no raw `None` values.
- **Feedback**: Correct → `st.success("✅ " + feedback)`; wrong → `st.error("❌ " + feedback)`.

## License

Use and modify as needed for your own projects.
