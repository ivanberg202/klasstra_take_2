# filename: app/routers/teacher.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.class_ import Class
from app.models.teacher_class import TeacherClass
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementOut
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.utils.roles import can_create_announcements
from app.schemas.class_ import ClassOut  # Import the correct schema

router = APIRouter(prefix="/teacher", tags=["teacher"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get("/my-classes", response_model=List[ClassOut])  # Use ClassOut instead of Class
def get_my_classes(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Return a list of classes assigned to the logged-in teacher."""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Not allowed")
    teacher_id = payload.get("user_id")

    class_ids = db.query(TeacherClass.class_id)\
                  .filter(TeacherClass.teacher_id == teacher_id).all()
    if not class_ids:
        return []
    # Extract just the IDs
    c_ids = [r.class_id for r in class_ids]
    classes = db.query(Class).filter(Class.id.in_(c_ids)).all()
    return [ClassOut.from_orm(cls) for cls in classes]  # Convert to Pydantic models



@router.get("/my-announcements", response_model=List[AnnouncementOut])
def get_my_announcements(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Return announcements for all classes that the teacher is assigned to.
    Also includes any announcements created_by this teacher (if relevant).
    """
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Not allowed")
    teacher_id = payload.get("user_id")

    # 1) Get the classes this teacher belongs to
    class_ids = db.query(TeacherClass.class_id)\
                  .filter(TeacherClass.teacher_id == teacher_id).all()
    c_ids = [r.class_id for r in class_ids]

    # 2) Announcements for those classes
    ann_class = db.query(Announcement)\
        .options(joinedload(Announcement.created_by))\
        .filter(Announcement.recipient_type=="class", Announcement.recipient_id.in_(c_ids))

    # 3) Also announcements the teacher created (if you want to unify them)
    ann_created_by_me = db.query(Announcement)\
        .options(joinedload(Announcement.created_by))\
        .filter(Announcement.created_by_id==teacher_id)

    # Combine sets (SQL Alchemy queries as sets):
    announcements = ann_class.union(ann_created_by_me).all()
    return announcements


@router.post("/announcements", response_model=List[AnnouncementOut])
def create_teacher_announcements(
    title: str,
    body: str,
    attachment_url: str | None = None,
    classes: List[int] = [],
    parents: List[int] = [],
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Create announcements for one or more class IDs or parent IDs.
    We'll insert multiple Announcement rows, one per recipient.
    """
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user_id = payload.get("user_id")
    role = payload.get("role")
    if not can_create_announcements(role) or role != "teacher":
        raise HTTPException(status_code=403, detail="Not allowed")

    new_announcements = []
    # For each class
    for cid in classes:
        ann = Announcement(
            title=title,
            body=body,
            attachment_url=attachment_url,
            created_by_id=user_id,
            last_updated_by_id=user_id,
            recipient_type="class",
            recipient_id=cid
        )
        db.add(ann)
        new_announcements.append(ann)

    # For each parent
    for pid in parents:
        ann = Announcement(
            title=title,
            body=body,
            attachment_url=attachment_url,
            created_by_id=user_id,
            last_updated_by_id=user_id,
            recipient_type="parent",
            recipient_id=pid
        )
        db.add(ann)
        new_announcements.append(ann)

    db.commit()
    for a in new_announcements:
        db.refresh(a)
    return new_announcements


@router.patch("/announcements/{announcement_id}", response_model=AnnouncementOut)
def edit_teacher_announcement(
    announcement_id: int,
    title: str | None = None,
    body: str | None = None,
    attachment_url: str | None = None,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Edit an announcement if you are the creator."""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    teacher_id = payload.get("user_id")
    role = payload.get("role")
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Not allowed")

    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    if ann.created_by_id != teacher_id:
        raise HTTPException(status_code=403, detail="You can only edit your own announcement")

    if title: ann.title = title
    if body: ann.body = body
    if attachment_url is not None:
        ann.attachment_url = attachment_url
    ann.last_updated_by_id = teacher_id
    db.commit()
    db.refresh(ann)
    return ann


@router.delete("/announcements/{announcement_id}")
def delete_teacher_announcement(
    announcement_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Delete an announcement if you are the creator."""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    teacher_id = payload.get("user_id")
    role = payload.get("role")
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Not allowed")

    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    if ann.created_by_id != teacher_id:
        raise HTTPException(status_code=403, detail="You can only delete your own announcement")

    db.delete(ann)
    db.commit()
    return {"detail": "Announcement deleted"}
