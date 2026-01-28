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
    st.write(data["lesson"])

    st.subheader("❓ Question")
    st.write(data["question"])

answer = st.text_input("Your answer")

if st.button("Submit answer"):
    if "state" not in st.session_state:
        st.error("Please start a lesson first!")
    else:
        state = st.session_state["state"].copy()
        state["answer"] = answer
        r = requests.post(f"{API}/tutor/answer", json=state)
        new_state = r.json()
        
        # Update stored state
        st.session_state["state"] = new_state

        st.write(new_state.get("feedback"))
        st.write(new_state.get("question"))

