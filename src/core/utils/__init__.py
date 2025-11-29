from hashlib import pbkdf2_hmac
from os import urandom


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = urandom(16)
    else:
        salt = bytes.fromhex(salt)
    hashed_password = pbkdf2_hmac('sha256', password.encode(), salt, 10 ** 6).hex()
    return hashed_password, salt.hex()


def check_password(password: str, salt: str, hashed_password: str) -> bool:
    return hash_password(password, salt)[0] == hashed_password
