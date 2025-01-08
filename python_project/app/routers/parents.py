from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserOut
from app.utils.roles import can_manage_users

router = APIRouter(prefix="/parents", tags=["parents"])

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/", response_model=list[UserOut])
def get_parents(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Fetch all users with the role 'parent'.
    """
    # Decode the token and check permissions
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    if not can_manage_users(payload.get("role")):
        raise HTTPException(status_code=403, detail="Not allowed")

    # Query all users with the 'parent' role
    parents = db.query(User).filter(User.role == "parent").all()
    return parents
