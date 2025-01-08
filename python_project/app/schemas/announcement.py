# filename: app/schemas/announcement.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.user import UserOut  # Ensure this is correctly imported

class AnnouncementBase(BaseModel):
    title: str
    body: str

class AnnouncementCreate(AnnouncementBase):
    attachment_url: Optional[str] = None
    classes: List[int] = []
    parents: List[int] = []

class AnnouncementOut(BaseModel):
    id: int
    title: str
    body: str
    created_by: UserOut
    last_updated_by: Optional[UserOut]
    recipient_type: str
    recipient_id: int
    attachment_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    attachment_url: Optional[str] = None