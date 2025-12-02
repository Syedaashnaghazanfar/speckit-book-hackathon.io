from fastapi import APIRouter, HTTPException, Depends, status
from ..models.user import UserCreate, UserLogin, Token, UserResponse
from ..services.db import db
from ..services.auth_utils import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import asyncpg

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    if not db.pool:
        raise HTTPException(status_code=503, detail="Database not initialized")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    try:
        async with db.pool.acquire() as conn:
            # Check if user exists
            existing_user = await conn.fetchval(
                "SELECT id FROM users WHERE email = $1", user.email
            )
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

            # Create user
            row = await conn.fetchrow(
                """
                INSERT INTO users (email, password_hash, full_name)
                VALUES ($1, $2, $3)
                RETURNING id, email, full_name
                """,
                user.email, hashed_password, user.full_name
            )

            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email, "id": row['id']},
                expires_delta=access_token_expires
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": row['id'],
                    "email": row['email'],
                    "full_name": row['full_name']
                }
            }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    if not db.pool:
        raise HTTPException(status_code=503, detail="Database not initialized")

    async with db.pool.acquire() as conn:
        # Get user
        row = await conn.fetchrow(
            "SELECT id, email, password_hash, full_name FROM users WHERE email = $1",
            user_credentials.email
        )

        if not row or not verify_password(user_credentials.password, row['password_hash']):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": row['email'], "id": row['id']},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": row['id'],
                "email": row['email'],
                "full_name": row['full_name']
            }
        }
