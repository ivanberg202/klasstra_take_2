# filename: app/schemas/child.py

from pydantic import BaseModel
from app.schemas.common import Timestamped
from app.schemas.class_ import ClassOut  # Import ClassOut

class ChildBase(BaseModel):
    parent_id: int
    first_name: str
    last_name: str
    class_id: int

class ChildOut(ChildBase, Timestamped):
    id: int
    class_: ClassOut  # Nested ClassOut

    class Config:
        from_attributes = True
