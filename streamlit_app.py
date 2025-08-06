import streamlit as st
import pandas as pd
import sqlite3

# Hardcoded users - can later move to a secure database or use Streamlit Auth if needed
users = {"prof": "teach123", "student": "learn123"}

# Use session_state to persist login info
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None

# Login form
if not st.session_state["authenticated"]:
    st.title("🔐 Think-Trek AI Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if users.get(user) == pwd:
            st.session_state["authenticated"] = True
            st.session_state["role"] = "prof" if user == "prof" else "student"
            st.success(f"Logged in as {user}")
            st.rerun()
        else:
            st.error("Invalid login")

# After login
if st.session_state["authenticated"]:
    role = st.session_state["role"]

    st.sidebar.title("🔧 Navigation")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.rerun()

    # Instructor view
    if role == "prof":
        st.title("📊 Think-Trek AI - Instructor Dashboard")

        conn = sqlite3.connect("thinktrek_logs.db")
        df = pd.read_sql_query("SELECT * FROM chat_logs", conn)
        conn.close()

        st.subheader("Search Questions")
        search = st.text_input("Enter a topic or keyword")
        filtered = df[df['user_question'].str.contains(search, na=False, case=False)]
        st.dataframe(filtered)

        st.subheader("Daily Usage")
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily = df.groupby('date').size()
        st.bar_chart(daily)

        st.subheader("All Logs")
        st.dataframe(df[['timestamp', 'user_question', 'bot_response', 'source_reference']])

        st.download_button("Download Logs", filtered.to_csv(index=False), file_name="chat_logs.csv")

    # Student view
    elif role == "student":
        st.title("👋 Welcome to ThinkTrek AI!")
        st.markdown("You're logged in as a student. Explore the chatbot and learn biology through inquiry-based conversation!")

