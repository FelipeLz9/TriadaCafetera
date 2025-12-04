import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.config import settings

def _truncate_password_to_bytes(password: str) -> bytes:
    """Trunca la contraseña a 72 bytes máximo para bcrypt"""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncar a 72 bytes, asegurándonos de no cortar en medio de un carácter multibyte
        password_bytes = password_bytes[:72]
        # Si el último byte es parte de un carácter multibyte, eliminarlo
        while len(password_bytes) > 0:
            try:
                password_bytes.decode('utf-8')
                break
            except UnicodeDecodeError:
                password_bytes = password_bytes[:-1]
    return password_bytes

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    # bcrypt tiene una limitación de 72 bytes, truncamos si es necesario
    password_bytes = _truncate_password_to_bytes(plain_password)
    # hashed_password viene como string desde la BD, necesitamos convertirlo a bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña"""
    # bcrypt tiene una limitación de 72 bytes, truncamos si es necesario
    password_bytes = _truncate_password_to_bytes(password)
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Retornar como string para almacenar en la BD
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token JWT de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verifica y decodifica un token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
