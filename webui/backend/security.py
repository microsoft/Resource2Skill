import os
from pathlib import Path
from cryptography.fernet import Fernet

_KEY_FILE = Path(__file__).resolve().parent / ".key"
_FERNET = None


def _fernet() -> Fernet:
    global _FERNET
    if _FERNET is not None:
        return _FERNET
    if _KEY_FILE.exists():
        key = _KEY_FILE.read_bytes().strip()
    else:
        key = Fernet.generate_key()
        _KEY_FILE.write_bytes(key)
        try:
            os.chmod(_KEY_FILE, 0o600)
        except Exception:
            pass
    _FERNET = Fernet(key)
    return _FERNET


def encrypt(plain: str) -> str:
    if not plain:
        return ""
    return _fernet().encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt(token: str) -> str:
    if not token:
        return ""
    try:
        return _fernet().decrypt(token.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""
