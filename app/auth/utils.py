import jwt
import bcrypt

from datetime import datetime, timedelta

from core.settings import settings

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,
    expire_seconds: int = settings.auth_jwt.access_token_lifetime_seconds,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    time_now = datetime.now()
    
    if expire_timedelta:
        expire = time_now + expire_timedelta
    else:
        expire = time_now + timedelta(seconds=expire_seconds) 
        
    to_encode.update(
        exp=expire,
        iat=time_now,
    )
    
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())