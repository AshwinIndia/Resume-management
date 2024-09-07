
import sqlite3

def create_db():
    """Create database tables if they do not exist."""
    conn = sqlite3.connect('resume_management.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS resumes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        job_title TEXT,
                        file_path TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS job_titles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT UNIQUE)''')

    conn.commit()
    conn.close()

def get_db_connection():
    """Create and return a connection to the database."""
    return sqlite3.connect('resume_management.db')

if __name__ == "__main__":
    create_db()
