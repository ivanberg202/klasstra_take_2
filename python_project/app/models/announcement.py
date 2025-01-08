# filename: app/models/announcement.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    recipient_type = Column(String, nullable=False)   # "class" or "parent"
    recipient_id = Column(Integer, nullable=False)    # class_id or user_id

    # Optional: store a file path or URL if there’s an attachment
    attachment_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    created_by = relationship(
        "User",
        foreign_keys=[created_by_id],
        backref="announcements_created"
    )
    last_updated_by = relationship(
        "User",
        foreign_keys=[last_updated_by_id],
        backref="announcements_updated"
    )
