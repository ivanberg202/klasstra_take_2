# filename: app/routers/announcements.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.announcement import AnnouncementCreate, AnnouncementOut
from app.models.announcement import Announcement
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from app.core.config import settings
from app.utils.roles import can_create_announcements, is_parent
from app.utils.rate_limit import check_rate_limit
from app.models.child import Child
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.models.child import Child
from app.models.user import User
from app.models.teacher_class import TeacherClass
from python_project.app.schemas.user import UserOut



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


@router.get("/teacher/parents", response_model=List[UserOut])
def get_teacher_parents(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Fetch parents associated with the teacher's assigned classes.
    Accessible by 'teacher' and 'class_rep' roles.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    role = payload.get("role")
    user_id = payload.get("user_id")

    if role not in ["teacher", "class_rep", "admin"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    if role == "admin":
        # Admins can fetch all parents
        parents = db.query(User).filter(User.role == "parent").all()
        return parents
    else:
        # Teachers and class_reps fetch parents of their classes
        # Step 1: Get all classes assigned to the teacher
        teacher_classes = db.query(TeacherClass.class_id).filter(TeacherClass.teacher_id == user_id).all()
        class_ids = [tc.class_id for tc in teacher_classes]

        if not class_ids:
            return []

        # Step 2: Get all children in those classes
        children = db.query(Child).filter(Child.class_id.in_(class_ids)).all()
        parent_ids = list({child.parent_id for child in children})

        if not parent_ids:
            return []

        # Step 3: Fetch unique parents
        parents = db.query(User).filter(User.id.in_(parent_ids), User.role == "parent").all()
        return parents