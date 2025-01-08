# filename: app/routers/children.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.schemas.child import ChildBase, ChildOut
from app.models.child import Child
from app.models.class_ import Class
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from app.core.config import settings
from app.utils.roles import is_parent

router = APIRouter(prefix="/children", tags=["children"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=ChildOut)
def add_child(c: ChildBase, token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if not is_parent(payload.get("role")) or payload.get("user_id") != c.parent_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Check if the class exists
    cls = db.query(Class).filter(Class.id == c.class_id).first()
    if not cls:
        raise HTTPException(status_code=400, detail="Invalid class_id. Class does not exist.")

    ch = Child(**c.dict())
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch

@router.get("/my", response_model=list[ChildOut])
def get_my_children(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Returns a list of children for the currently logged-in parent/class_rep,
    including the class name for each child.
    """
    # Decode token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    user_role = payload.get("role")
    user_id = payload.get("user_id")
    
    # Ensure only parents (or class_reps) can fetch children
    if not is_parent(user_role):
        raise HTTPException(status_code=403, detail="Not allowed")
    
    # Query all children that belong to this parent’s user_id, joining with Class
    children = db.query(Child).options(joinedload(Child.class_)).filter(Child.parent_id == user_id).all()
    
    return children