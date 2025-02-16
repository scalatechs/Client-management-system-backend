from cryptography.fernet import Fernet

new_key = Fernet.generate_key()
print("this is the key",new_key.decode())