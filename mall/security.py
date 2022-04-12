from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from apps.user.models import User

from .conf import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer = HTTPBearer()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码 vs hash密码
    :param plain_password: 明文密码
    :param hashed_password: hash密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    加密明文
    :param password: 明文密码
    :return:
    """
    return pwd_context.hash(password)


def create_access_token(username: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"sub": username}.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_token(token: str) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return await User.get_or_none(username=username)


async def check_token_http(token: HTTPAuthorizationCredentials = Depends(bearer)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="认证失败",
    )
    try:
        return await check_token(token.credentials)
    except JWTError:
        raise credentials_exception
