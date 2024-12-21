# schemas/announcement.py
from datetime import datetime
from pydantic import BaseModel
from app.schemas.user import UserOut  # or a simpler user schema

class AnnouncementBase(BaseModel):
    title: str
    body: str
    recipient_type: str
    recipient_id: int

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementOut(BaseModel):
    id: int
    title: str
    body: str

    # "created_by" is now a full user object, not an int
    created_by: UserOut
    last_updated_by: UserOut | None
    
    recipient_type: str
    recipient_id: int
    created_at: datetime
    updated_at: datetime | None
    
    class Config:
        from_attributes = True
