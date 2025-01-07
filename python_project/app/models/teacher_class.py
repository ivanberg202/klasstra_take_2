# filename: app/models/teacher_class.py
from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from app.core.database import Base

class TeacherClass(Base):
    __tablename__ = "teacher_classes"
    
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    # We enforce uniqueness on (teacher_id, class_id) pairs.
    __table_args__ = (
        PrimaryKeyConstraint('teacher_id', 'class_id', name='teacher_class_pk'),
    )
