import streamlit as st
import requests

API = "http://localhost:8000"

# ---------------------------------------------------------------------------
# Session state initialization (single source of truth)
# ---------------------------------------------------------------------------
if "tutor_state" not in st.session_state:
    st.session_state.tutor_state = None
if "tutor_session_id" not in st.session_state:
    st.session_state.tutor_session_id = None

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("Stateful AI Tutor")

# ---------------------------------------------------------------------------
# Status line (from state only)
# ---------------------------------------------------------------------------
state = st.session_state.tutor_state
if state and isinstance(state, dict):
    difficulty = state.get("difficulty")
    streak = state.get("streak", 0)
    if difficulty is not None or streak is not None:
        parts = []
        if difficulty is not None:
            parts.append(f"Difficulty: {difficulty}")
        if streak is not None:
            parts.append(f"Streak: {streak}")
        if parts:
            st.caption(" | ".join(parts))
st.divider()

# ---------------------------------------------------------------------------
# Start lesson
# ---------------------------------------------------------------------------
topic = st.text_input("What do you want to learn?", key="topic_input")

if st.button("Start", key="btn_start"):
    if not (topic and str(topic).strip()):
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Thinking..."):
            try:
                r = requests.post(f"{API}/tutor/start", params={"topic": topic.strip()})
                r.raise_for_status()
                data = r.json()
            except requests.RequestException as e:
                st.error(f"Could not start session: {e}")
            else:
                session_id = data.get("session_id")
                # API response → update state only; do not render from data
                if session_id is not None:
                    st.session_state.tutor_session_id = session_id
                # Store returned state as our single source of truth (omit session_id from state if present)
                state_from_api = {k: v for k, v in data.items() if k != "session_id"}
                st.session_state.tutor_state = state_from_api if state_from_api else data
                st.rerun()

# ---------------------------------------------------------------------------
# Render UI only from st.session_state.tutor_state
# ---------------------------------------------------------------------------
state = st.session_state.tutor_state

if state is not None and isinstance(state, dict):
    # Lesson section
    lesson = state.get("lesson")
    if lesson is not None and str(lesson).strip():
        st.subheader("📘 Lesson")
        st.write(lesson)
        st.divider()

    # Feedback section (always before next question)
    feedback = state.get("feedback")
    if feedback is not None and str(feedback).strip():
        correct = state.get("correct")
        if correct is True:
            st.success("✅ " + str(feedback))
        else:
            st.error("❌ " + str(feedback))
        st.divider()

    # Question section
    question = state.get("question")
    if question is not None and str(question).strip():
        st.subheader("❓ Question")
        st.write(question)
        st.divider()

# ---------------------------------------------------------------------------
# Answer input and Submit (disabled when no session or no question to answer)
# ---------------------------------------------------------------------------
has_session = st.session_state.tutor_session_id is not None
# Disable submit when no session or when we're about to send (handled by spinner)
submit_disabled = not has_session

answer = st.text_input("Your answer", key="answer_input", disabled=not has_session)

if st.button("Submit answer", key="btn_submit", disabled=submit_disabled):
    if not has_session:
        st.error("Please start a lesson first!")
    else:
        answer_text = answer.strip() if answer else ""
        if not answer_text:
            st.warning("Please enter an answer.")
        else:
            with st.spinner("Thinking..."):
                try:
                    r = requests.post(
                        f"{API}/tutor/answer",
                        json={
                            "session_id": st.session_state.tutor_session_id,
                            "answer": answer_text,
                        },
                    )
                    r.raise_for_status()
                    new_state = r.json()
                except requests.RequestException as e:
                    st.error(f"Could not submit answer: {e}")
                else:
                    # Replace state with API response; do not render from new_state
                    st.session_state.tutor_state = new_state
                    st.rerun()
