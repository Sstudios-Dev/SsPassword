import os
import sqlite3

def connect_db():
    db_folder = "integrity"
    os.makedirs(db_folder, exist_ok=True)
    db_path = os.path.join(db_folder, "passwords.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    return conn

def add_password(conn, website, username, password):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)', (website, username, password))
    conn.commit()

def get_passwords(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT website, username, password FROM passwords')
    return cursor.fetchall()
