# filename: app/routers/classes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.class_ import Class
from app.schemas.class_ import ClassBase, ClassOut
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.utils.roles import can_manage_users

router = APIRouter(prefix="/classes", tags=["classes"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=ClassOut)
def create_class(c: ClassBase, token: str=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if not can_manage_users(payload.get("role")):
        raise HTTPException(status_code=403, detail="Not allowed")
    cls = Class(name=c.name)
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return cls

@router.get("/", response_model=list[ClassOut])
def list_classes(db: Session = Depends(get_db)):
    # No auth needed, or optionally add auth if required.
    return db.query(Class).all()
