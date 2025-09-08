from cryptography.fernet import Fernet

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