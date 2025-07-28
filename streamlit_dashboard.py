import streamlit as st
import pandas as pd
import sqlite3

st.title("📊 ThinkTrek AI - Professor Dashboard")

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

st.download_button("Download Logs", filtered.to_csv(index=False), file_name="chat_logs.csv")
