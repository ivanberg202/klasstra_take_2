# filename: app/schemas/child.py
from pydantic import BaseModel
from app.schemas.common import Timestamped

class ChildBase(BaseModel):
    parent_id: int
    first_name: str
    last_name: str
    class_id: int

class ChildOut(ChildBase, Timestamped):
    id: int

    class Config:
        from_attributes = True
