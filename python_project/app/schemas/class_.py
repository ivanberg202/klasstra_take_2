# filename: app/schemas/class_.py

from pydantic import BaseModel
from app.schemas.common import Timestamped

class ClassBase(BaseModel):
    name: str

class ClassOut(ClassBase, Timestamped):
    id: int

    class Config:
        from_attributes = True
