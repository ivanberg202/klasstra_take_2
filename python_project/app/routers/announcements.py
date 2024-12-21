# filename: app/routers/announcements.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.announcement import AnnouncementCreate, AnnouncementOut
from app.models.announcement import Announcement
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.utils.roles import can_create_announcements, is_parent
from app.utils.rate_limit import check_rate_limit
from app.models.child import Child
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/announcements", tags=["announcements"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=AnnouncementOut)
def create_announcement(
    a: AnnouncementCreate, 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user_id = payload.get("user_id")
    role = payload.get("role")
    if not can_create_announcements(role):
        raise HTTPException(status_code=403, detail="Not allowed")
    if not check_rate_limit(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    ann = Announcement(
        title=a.title,
        body=a.body,
        created_by=user_id,
        last_updated_by=user_id,
        recipient_type=a.recipient_type,
        recipient_id=a.recipient_id
    )
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return ann

@router.get("/for_parent", response_model=List[AnnouncementOut])
def get_announcements_for_parent(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Returns announcements targeted to this parent's user_id (recipient_type='parent')
    AND announcements for all classes that any of this parent's children are in.
    """
    # Decode JWT token to extract user details
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user_role = payload.get("role")
    user_id = payload.get("user_id")

    # Only parents (or class_rep acting as parents) can access
    if not is_parent(user_role):
        raise HTTPException(status_code=403, detail="Not allowed")

    # 1) Query classes of this parent's children
    child_classes = db.query(Child.class_id).filter(Child.parent_id == user_id).all()
    class_ids = [row.class_id for row in child_classes]

    # 2) Query class announcements
    class_announcements = db.query(Announcement).options(
        joinedload(Announcement.created_by)  # Ensure creator is eagerly loaded
    ).filter(
        Announcement.recipient_type == "class",
        Announcement.recipient_id.in_(class_ids)
    ).all()

    # 3) Query direct announcements to the parent
    parent_announcements = db.query(Announcement).options(
        joinedload(Announcement.created_by)  # Ensure creator is eagerly loaded
    ).filter(
        Announcement.recipient_type == "parent",
        Announcement.recipient_id == user_id
    ).all()

    # Combine and return the announcements
    combined_announcements = class_announcements + parent_announcements
    return combined_announcements