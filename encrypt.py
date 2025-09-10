from cryptography.fernet import Fernet
import bcrypt

def generate_key():
    key = Fernet.generate_key()
    with open("master.key", "wb") as f:
        f.write(key)

def load_key():
    with open("master.key", "rb") as f:
        return f.read()
    
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

def generate_password_hash(password: str):
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return salt, hashed_password

def verify_password_hash(password: str, hash: bytes):
    password_bytes = password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hash)