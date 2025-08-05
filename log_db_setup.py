import sqlite3

conn = sqlite3.connect("thinktrek_logs.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    timestamp TEXT,
    user_question TEXT,
    bot_response TEXT,
    source_reference TEXT,
    session_id TEXT
)
''')

conn.commit()
conn.close()
print("Database setup complete.")