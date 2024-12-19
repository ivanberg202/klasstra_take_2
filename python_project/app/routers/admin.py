# filename: app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.models.user import User
from app.utils.roles import can_manage_users

router = APIRouter(prefix="/admin", tags=["admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.put("/user/{user_id}/class_rep")
def make_class_rep(user_id: int, token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if not can_manage_users(payload.get("role")):
        raise HTTPException(status_code=403, detail="Not allowed")
    user = db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = "class_rep"
    db.commit()
    return {"detail": "User promoted to class_rep"}
