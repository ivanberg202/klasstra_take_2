# filename: app/schemas/announcement.py
from pydantic import BaseModel
from app.schemas.common import Timestamped

class AnnouncementBase(BaseModel):
    title: str
    body: str
    recipient_type: str
    recipient_id: int

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementOut(AnnouncementBase, Timestamped):
    id: int
    created_by: int
    last_updated_by: int | None
