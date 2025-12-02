from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..services.auth_utils import ALGORITHM, verify_password
from ..config import settings
from ..services.db import db
from ..models.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.get_secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Check if user exists in DB
    if not db.pool:
         raise HTTPException(status_code=503, detail="Database unavailable")
         
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, email, full_name FROM users WHERE id = $1",
            user_id
        )
        if not row:
            raise credentials_exception
            
        return UserResponse(
            id=row['id'],
            email=row['email'],
            full_name=row['full_name']
        )
