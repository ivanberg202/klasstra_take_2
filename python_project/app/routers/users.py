# filename: app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.utils.roles import can_manage_users
from fastapi import Path

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username==user_in.username)|(User.email==user_in.email)).first():
        raise HTTPException(status_code=400, detail="User exists")
    user = User(
        username=user_in.username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserOut)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    username = payload.get("sub")
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int = Path(..., ge=1), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve a user's information by their ID.
    Only accessible by admins.
    """
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    role = payload.get("role")
    if not can_manage_users(role):
        raise HTTPException(status_code=403, detail="Not allowed")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
