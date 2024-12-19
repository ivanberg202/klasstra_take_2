# filename: app/schemas/user.py
from pydantic import BaseModel, EmailStr, constr
from app.schemas.common import Timestamped

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserOut(UserBase, Timestamped):
    id: int
