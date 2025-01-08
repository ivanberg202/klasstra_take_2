# filename: app/routers/teacher.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.class_ import Class
from app.models.teacher_class import TeacherClass
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementOut, AnnouncementCreate, AnnouncementUpdate
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
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
    announcement: AnnouncementCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Decode JWT token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
    user_id = payload.get("user_id")
    role = payload.get("role")
    
    if not can_create_announcements(role):
        raise HTTPException(status_code=403, detail="Not allowed")
    
    # Fetch the teacher user
    teacher_user = db.query(User).filter(User.id == user_id, User.role == "teacher").first()
    if not teacher_user:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    new_announcements = []
    
    # Create announcements for classes
    for class_id in announcement.classes:
        cls = db.query(Class).filter(Class.id == class_id).first()
        if not cls:
            raise HTTPException(status_code=400, detail=f"Class with id {class_id} does not exist")
        
        ann = Announcement(
            title=announcement.title,
            body=announcement.body,
            attachment_url=announcement.attachment_url,
            created_by_id=teacher_user.id,
            recipient_type="class",
            recipient_id=class_id
        )
        db.add(ann)
        new_announcements.append(ann)
    
    # Create announcements for parents
    for parent_id in announcement.parents:
        parent_user = db.query(User).filter(User.id == parent_id, User.role == "parent").first()
        if not parent_user:
            raise HTTPException(status_code=400, detail=f"Parent with id {parent_id} does not exist")
        
        ann = Announcement(
            title=announcement.title,
            body=announcement.body,
            attachment_url=announcement.attachment_url,
            created_by_id=teacher_user.id,
            recipient_type="parent",
            recipient_id=parent_id
        )
        db.add(ann)
        new_announcements.append(ann)
    
    db.commit()
    
    # Refresh and collect the announcements to return
    for ann in new_announcements:
        db.refresh(ann)
    
    return new_announcements


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


@router.patch("/announcements/{announcement_id}", response_model=AnnouncementOut)
def update_teacher_announcement(
    announcement_id: int,
    announcement_data: AnnouncementUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Update an existing announcement (title, body, attachment_url).
    Only the teacher who created the announcement can update it.
    """
    # Decode token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    user_id = payload.get("user_id")
    role = payload.get("role")

    # Check if user can create/edit announcements
    if not can_create_announcements(role):
        raise HTTPException(status_code=403, detail="Not allowed")

    # Retrieve the announcement
    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")

    # Ensure the logged-in teacher is the creator
    if ann.created_by_id != user_id:
        raise HTTPException(status_code=403, detail="You can only update your own announcement")

    # Apply updates
    if announcement_data.title is not None:
        ann.title = announcement_data.title
    if announcement_data.body is not None:
        ann.body = announcement_data.body
    if announcement_data.attachment_url is not None:
        ann.attachment_url = announcement_data.attachment_url

    # Record who last updated it
    ann.last_updated_by_id = user_id

    db.commit()
    db.refresh(ann)
    return ann