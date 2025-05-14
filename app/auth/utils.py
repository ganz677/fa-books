from datetime import datetime, timedelta

import bcrypt
import jwt
from core.settings import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,
    expire_seconds: int = settings.auth_jwt.access_token_lifetime_seconds,
    expire_timedelta: timedelta | None = None,
):
    time_now = datetime.utcnow()

    if expire_timedelta:
        expire = time_now + expire_timedelta
    else:
        expire = time_now + timedelta(seconds=expire_seconds)


    full_payload = {
        **payload,
        "exp": expire,
        "iat": time_now,
    }

    return jwt.encode(
        payload=full_payload,
        key=private_key,
        algorithm=algorithm
    )


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
