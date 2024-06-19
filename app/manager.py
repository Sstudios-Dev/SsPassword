# Import necessary functions from app.database and app.encryption modules
from app.database import connect_db, add_password, get_passwords
from app.encryption import encrypt_message, decrypt_message, load_key

# Function to store an encrypted password for a given website and username
def store_password(website, username, password):
    # Load the encryption key
    key = load_key()
    
    # Encrypt the provided password using the loaded key
    encrypted_password = encrypt_message(password, key)
    
    # Establish a connection to the database
    conn = connect_db()
    
    # Add the encrypted password to the database along with the website and username
    add_password(conn, website, username, encrypted_password)
    
    # Close the database connection
    conn.close()

# Function to retrieve and decrypt all stored passwords
def retrieve_passwords():
    # Load the encryption key
    key = load_key()
    
    # Establish a connection to the database
    conn = connect_db()
    
    # Retrieve all stored passwords from the database
    passwords = get_passwords(conn)
    
    # Decrypt each password using the loaded key and store them in a list of tuples
    decrypted_passwords = [(website, username, decrypt_message(password, key)) for website, username, password in passwords]
    
    # Close the database connection
    conn.close()
    
    # Return the list of decrypted passwords along with their respective websites and usernames
    return decrypted_passwords
