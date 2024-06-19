# Import necessary modules
import os
from cryptography.fernet import Fernet

# Function to generate a new encryption key
def generate_key():
    return Fernet.generate_key()

# Function to load the encryption key from a file
def load_key():
    return open("integrity/secret.key", "rb").read()

# Function to save the encryption key to a file
def save_key(key):
    # Ensure the directory exists
    os.makedirs("integrity", exist_ok=True)
    
    # Write the key to a file in binary mode
    with open("integrity/secret.key", "wb") as key_file:
        key_file.write(key)

# Function to encrypt a message using the provided key
def encrypt_message(message, key):
    # Create a Fernet object with the provided key
    f = Fernet(key)
    
    # Encrypt the message and return the encrypted bytes
    return f.encrypt(message.encode())

# Function to decrypt an encrypted message using the provided key
def decrypt_message(encrypted_message, key):
    # Create a Fernet object with the provided key
    f = Fernet(key)
    
    # Decrypt the message and return the decoded string
    return f.decrypt(encrypted_message).decode()

# Function to check if the encryption key exists
def check_or_create_key():
    # Check if the key file exists and return the result
    if not os.path.exists("integrity/secret.key"):
        return False
    return True

# Function to create and save a new encryption key
def create_key():
    # Generate a new key
    key = generate_key()
    
    # Save the generated key to a file
    save_key(key)
