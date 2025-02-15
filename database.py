import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save a new message
def save_message(user, message):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (user, message))
    conn.commit()
    conn.close()

# Get last 5 messages
def get_last_messages(limit=5):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("SELECT user, message FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    messages = c.fetchall()
    conn.close()
    return messages[::-1]  # Reverse order to maintain chat flow
