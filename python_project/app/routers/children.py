# filename: app/routers/children.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.child import ChildBase, ChildOut
from app.models.child import Child
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.utils.roles import is_parent

router = APIRouter(prefix="/children", tags=["children"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=ChildOut)
def add_child(c: ChildBase, token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if not is_parent(payload.get("role")) or payload.get("user_id") != c.parent_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    ch = Child(**c.dict())
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch
