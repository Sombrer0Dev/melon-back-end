from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from back_end.core.config import settings
from back_end.models.user_model import User
from back_end.schemas.auth_schema import TokenPayload
from back_end.services.user_service import UserService

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)) -> User:
    """ Функция для инъекции зависимости JWT токена

    Args:
        token: JWT токен

    Returns: Модель юзера

    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "Could not validate credentials:",
                    "error": str(e),
                    "token": token},
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
