from cryptography.fernet import Fernet



# def generate_and_save_key(env_file_path='../.env'):
#     key = Fernet.generate_key()
#
#     os.makedirs(os.path.dirname(env_file_path), exist_ok=True)
#
#     with open(env_file_path, 'a') as env_file:
#         env_file.write(f"FERNET_KEY={key.decode()}\n")

from dotenv import dotenv_values
from io import StringIO
from datetime import datetime
from requests.auth import HTTPBasicAuth
from  super_app import settings




def load_fernet_key():
    key = settings.dotenv_config.get('FERNET_KEY')
    if key is None:
        raise ValueError(
            "FERNET_KEY not")

    return Fernet(key.encode())


def encrypt_message(message):
    fernet = load_fernet_key()
    encrypted_message = fernet.encrypt(message.encode())

    return encrypted_message


def decrypt_message(encrypted_message):
    fernet = load_fernet_key()
    try:

        if isinstance(encrypted_message, str):
            encrypted_message = eval(encrypted_message)

        decrypted_message = fernet.decrypt(encrypted_message).decode()

        return decrypted_message
    except Exception as e:
        print(f"Error decrypting message: {e}")
        raise
