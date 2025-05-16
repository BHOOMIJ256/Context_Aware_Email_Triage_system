import sqlite3

def init_db():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS triage_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            category TEXT,
            tone TEXT,
            urgency TEXT,
            reply TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database and table created successfully.")
