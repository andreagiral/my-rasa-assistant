import streamlit as st
import requests

# Set up page config
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

# Chat display
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# User input field
user_input = st.chat_input("Ask a biology question...")

# Send question to Rasa Webhook
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    try:
        response = requests.post(
            "https://thinktrek-web.onrender.com/webhooks/rest/webhook",
            json={"sender": "student-user", "message": user_input},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        bot_reply = "\n\n".join([d.get("text", "") for d in data]) or "🤖 I didn't understand that."

    except Exception as e:
        bot_reply = f"⚠️ Error contacting ThinkTrek AI: {e}"

    st.session_state.chat_history.append({"role": "assistant", "text": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
