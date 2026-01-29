import streamlit as st
import requests

API = "http://localhost:8000"

st.title("Stateful AI Tutor (Feature 1)")

topic = st.text_input("What do you want to learn?")

if st.button("Start"):
    r = requests.post(f"{API}/tutor/start", params={"topic": topic})
    data = r.json()
    
    # Store state in session state
    st.session_state["state"] = data

    st.subheader("📘 Lesson")
    st.write(data.get("lesson"))

    st.subheader("❓ Question")
    st.write(data.get("question"))

answer = st.text_input("Your answer")

if st.button("Submit answer"):
    if "state" not in st.session_state or "session_id" not in st.session_state["state"]:
        st.error("Please start a lesson first!")
    else:
        session_id = st.session_state["state"]["session_id"]
        r = requests.post(
            f"{API}/tutor/answer",
            json={"session_id": session_id, "answer": answer}
        )
        new_state = r.json()
        
        # Update stored state
        st.session_state["state"] = {"session_id": session_id, **new_state}

        st.write(new_state.get("feedback"))
        st.write(new_state.get("question"))

