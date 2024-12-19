# filename: app/schemas/user.py
from pydantic import BaseModel, EmailStr, constr, Field
from app.schemas.common import Timestamped

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$",
                          description="Username must be 3-20 characters long and contain only alphanumeric characters or underscores.")
    first_name: str = Field(..., min_length=1, description="First name is required and must have at least 1 character.")
    last_name: str = Field(..., min_length=1, description="Last name is required and must have at least 1 character.")
    email: EmailStr = Field(..., description="A valid email address.")
    role: str = Field(..., pattern=r"^(teacher|parent|admin|class_rep)$", 
                      description="Role must be one of: teacher, parent, admin, class_rep.")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50, 
                          description="Password must be between 8 and 50 characters.")

class UserOut(UserBase, Timestamped):
    id: int
