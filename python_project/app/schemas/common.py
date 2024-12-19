# filename: app/schemas/common.py
from pydantic import BaseModel
from datetime import datetime

class Timestamped(BaseModel):
    created_at: datetime
    updated_at: datetime | None
    class Config:
        orm_mode = True
