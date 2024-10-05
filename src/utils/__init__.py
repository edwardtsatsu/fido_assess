import base64

from cryptography.fernet import Fernet
from passlib import pwd
from passlib.context import CryptContext

from configs import settings
from src.exceptions.decryption_failed_excpetion import DecryptionFailedException
from src.exceptions.encryption_failed_exception import EncryptionFailedException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ENCRYPTION_KEY = settings.encryption_key
# fernet_cipher = Fernet(ENCRYPTION_KEY.encode("utf-8"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def generate_password() -> str:
    return "password" if settings.app_env == "local" else pwd.genword(length=8)


def convert_to_cedis(amount: int) -> float:
    value = amount / 100
    return round(value, 2)


def convert_to_pesewas(amount: float) -> int:
    return amount * 100


# def encrypt_text(plain_text: str) -> str:
#     if not isinstance(plain_text, str):
#         raise EncryptionFailedException("Only string values can be encrypted.")

#     encrypted_text = fernet_cipher.encrypt(plain_text.encode("utf-8"))
#     return encrypted_text.decode("utf-8")


# def decrypt_text(encrypted_text: str) -> str:
#     if not isinstance(encrypted_text, str):
#         raise DecryptionFailedException("Only string values can be decrypted.")

#     try:
#         decrypted_text = fernet_cipher.decrypt(encrypted_text.encode("utf-8"))
#         return decrypted_text.decode("utf-8")
#     except Exception as e:
#         raise DecryptionFailedException("Decryption failed.") from e
