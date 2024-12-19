# filename: app/routers/announcements.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.announcement import AnnouncementCreate, AnnouncementOut
from app.models.announcement import Announcement
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.utils.roles import can_create_announcements
from app.utils.rate_limit import check_rate_limit

router = APIRouter(prefix="/announcements", tags=["announcements"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=AnnouncementOut)
def create_announcement(a: AnnouncementCreate, token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user_id = payload.get("user_id")
    role = payload.get("role")
    if not can_create_announcements(role):
        raise HTTPException(status_code=403, detail="Not allowed")
    if not check_rate_limit(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    ann = Announcement(
        title=a.title, body=a.body, created_by=user_id, last_updated_by=user_id,
        recipient_type=a.recipient_type, recipient_id=a.recipient_id)
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return ann
