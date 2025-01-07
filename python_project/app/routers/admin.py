# filename: app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.models.user import User
from app.models.teacher_class import TeacherClass
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

@router.post("/assign-teacher-class")
def assign_teacher_class(
    teacher_id: int,
    class_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Assign a teacher (teacher_id) to a class (class_id).
    Only admins can do this.
    """
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if not can_manage_users(payload.get("role")):
        raise HTTPException(status_code=403, detail="Not allowed")

    teacher = db.query(User).filter(User.id == teacher_id, User.role=="teacher").first()
    if not teacher:
        raise HTTPException(status_code=400, detail="Invalid teacher_id or user is not a teacher.")

    # Ensure we don't duplicate
    existing = db.query(TeacherClass).filter_by(teacher_id=teacher_id, class_id=class_id).first()
    if existing:
        return {"detail": "Teacher is already assigned to this class."}

    teacher_class = TeacherClass(teacher_id=teacher_id, class_id=class_id)
    db.add(teacher_class)
    db.commit()
    return {"detail": f"Assigned teacher_id={teacher_id} to class_id={class_id}."}
