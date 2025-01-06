# filename: app/models/child.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship


class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    class_ = relationship("Class")  # Define relationship
