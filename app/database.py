# Import necessary modules
import os
import sqlite3

# Function to establish a connection to the database
def connect_db():
    # Define the folder to store the database file
    db_folder = "integrity"
    
    # Create the folder if it doesn't exist
    os.makedirs(db_folder, exist_ok=True)
    
    # Define the path to the database file
    db_path = os.path.join(db_folder, "passwords.db")
    
    # Connect to the SQLite database at the specified path
    conn = sqlite3.connect(db_path)
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Create the passwords table if it doesn't already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Commit the changes to the database
    conn.commit()
    
    # Return the database connection object
    return conn

# Function to add a password entry to the database
def add_password(conn, website, username, password):
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Insert the website, username, and encrypted password into the passwords table
    cursor.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)', (website, username, password))
    
    # Commit the changes to the database
    conn.commit()

# Function to retrieve all password entries from the database
def get_passwords(conn):
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Select all entries from the passwords table
    cursor.execute('SELECT website, username, password FROM passwords')
    
    # Fetch all results from the executed query
    return cursor.fetchall()
