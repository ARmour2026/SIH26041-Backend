import os

import jwt
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.database import get_db
from app.models import Worker
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    ChangePasswordRequest,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])

password_hash = PasswordHash.recommended()

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "sih-development-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================
# JWT
# =========================

def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(Worker).filter(
        Worker.mobile_number == user.mobile_number
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Mobile number already registered"
        )

    new_user = Worker(
        name=user.name,
        mobile_number=user.mobile_number,
        password_hash=password_hash.hash(user.password),
        sector=user.sector,
        language_pref=user.language_pref
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration successful",
        "user_id": new_user.id
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(Worker).filter(
        Worker.mobile_number == user.mobile_number
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid mobile number or password"
        )

    if not password_hash.verify(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid mobile number or password"
        )

    access_token = create_access_token(existing_user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": existing_user.id,
        "name": existing_user.name
    }


# =========================
# AUTHENTICATED USER
# =========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload.get("sub"))

    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(Worker).filter(
        Worker.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


# =========================
# MY PROFILE
# =========================

@router.get("/me")
def get_my_profile(
    current_user: Worker = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "mobile_number": current_user.mobile_number,
        "sector": current_user.sector,
        "language_pref": current_user.language_pref
    }


# =========================
# CHANGE PASSWORD
# =========================

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: Worker = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not password_hash.verify(
        data.old_password,
        current_user.password_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect"
        )

    current_user.password_hash = password_hash.hash(
        data.new_password
    )

    db.commit()

    return {
        "message": "Password changed successfully"
    }
