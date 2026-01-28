import streamlit as st
import requests

API = "http://localhost:8000"

st.title("Stateful AI Tutor (Feature 1)")

topic = st.text_input("What do you want to learn?")

if st.button("Start"):
    r = requests.post(f"{API}/tutor/start", params={"topic": topic})
    data = r.json()

    st.subheader("📘 Lesson")
    st.write(data["lesson"])

    st.subheader("❓ Question")
    st.write(data["question"])


