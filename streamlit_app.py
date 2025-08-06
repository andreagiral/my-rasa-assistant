import streamlit as st
import pandas as pd
import sqlite3
import requests

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
        st.set_page_config(page_title="Think-Trek AI", layout="centered")
        st.title("🤖 Think-Trek AI – Your Biology Companion")

        st.markdown("""
        Welcome to **Think-Trek AI**, your intelligent biology tutor. 
        Ask me anything related to biology topics, capstone ideas, or practice exercises.
        I respond in a **definition + Socratic style**, and I cite sources when applicable.
        """)

        # Track chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["text"])

        user_input = st.chat_input("Ask a biology question...")

        if user_input:
            st.session_state.chat_history.append({"role": "user", "text": user_input})

            try:
                response = requests.post(
                    "https://thinktrek-web.onrender.com/webhooks/rest/webhook",
                    json={"sender": "student-user", "message": user_input},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()
                bot_reply = "\n\n".join([d.get("text", "") for d in data]) or "🤖 I didn't understand that."

            except Exception as e:
                bot_reply = f"⚠️ Error contacting ThinkTrek AI: {e}"

            st.session_state.chat_history.append({"role": "assistant", "text": bot_reply})

            with st.chat_message("assistant"):
                st.markdown(bot_reply)


