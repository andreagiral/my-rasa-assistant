import streamlit as st

users = {"prof": "teach123", "student": "learn123"}
user = st.text_input("Username")
pwd = st.text_input("Password", type="password")

if st.button("Login"):
    if users.get(user) == pwd:
        st.session_state["role"] = "prof" if user == "prof" else "student"
        st.success(f"Logged in as {user}")
    else:
        st.error("Invalid login")
