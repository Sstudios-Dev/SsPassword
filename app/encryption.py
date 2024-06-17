import os
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def load_key():
    return open("integrity/secret.key", "rb").read()

def save_key(key):
    os.makedirs("integrity", exist_ok=True)
    with open("integrity/secret.key", "wb") as key_file:
        key_file.write(key)

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def check_or_create_key():
    if not os.path.exists("integrity/secret.key"):
        return False
    return True

def create_key():
    key = generate_key()
    save_key(key)
