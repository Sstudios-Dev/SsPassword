from app.database import connect_db, add_password, get_passwords
from app.encryption import encrypt_message, decrypt_message, load_key

def store_password(website, username, password):
    key = load_key()
    encrypted_password = encrypt_message(password, key)
    conn = connect_db()
    add_password(conn, website, username, encrypted_password)
    conn.close()

def retrieve_passwords():
    key = load_key()
    conn = connect_db()
    passwords = get_passwords(conn)
    decrypted_passwords = [(website, username, decrypt_message(password, key)) for website, username, password in passwords]
    conn.close()
    return decrypted_passwords
