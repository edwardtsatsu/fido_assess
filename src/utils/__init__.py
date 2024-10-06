from cryptography.fernet import Fernet
from passlib import pwd
from passlib.context import CryptContext

from configs import settings
from src.exceptions.decryption_failed_excpetion import DecryptionFailedException
from src.exceptions.encryption_failed_exception import EncryptionFailedException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ENCRYPTION_KEY = settings.encryption_key

cipher = Fernet(ENCRYPTION_KEY)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def generate_password() -> str:
    return "password" if settings.app_env == "local" else pwd.genword(length=8)


def convert_to_cedis(amount: int) -> float:
    if amount is None:
        return 0
    value = amount / 100
    return round(value, 2)


def convert_to_pesewas(amount: float) -> int:
    if amount is None:
        return 0
    return amount * 100


def encrypt_text(plain_text: str) -> bytes:
    encrypted_username = cipher.encrypt(plain_text.encode())
    return encrypted_username


def decrypt_text(encrypted_text: bytes) -> str:
    decrypted_username = cipher.decrypt(encrypted_text).decode()
    return decrypted_username
