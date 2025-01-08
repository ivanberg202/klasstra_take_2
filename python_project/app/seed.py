# filename: app/seed.py
import sys
import os

# Add the project root to sys.path to allow imports from 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from app.core.database import SessionLocal
from app.models.user import User
from app.models.class_ import Class
from app.models.child import Child
from app.models.announcement import Announcement
from app.models.teacher_class import TeacherClass  # Import TeacherClass model
from app.core.security import hash_password

def seed():
    db = SessionLocal()
    try:
        # Create an admin user if not exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                password_hash=hash_password("AdminSecurePass123!"),
                role="admin",
            )
            db.add(admin)
            db.commit()
            print("Admin user created: admin / AdminSecurePass123!")
        else:
            print("Admin user already exists.")

        # Create a teacher user if not exists
        teacher = db.query(User).filter(User.username == "teacher1").first()
        if not teacher:
            teacher = User(
                username="teacher1",
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                password_hash=hash_password("TeacherPass123!"),
                role="teacher",
            )
            db.add(teacher)
            db.commit()
            print("Teacher user created: teacher1 / TeacherPass123!")
        else:
            print("Teacher user already exists.")

        # Create a parent user if not exists
        parent = db.query(User).filter(User.username == "parent1").first()
        if not parent:
            parent = User(
                username="parent1",
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                password_hash=hash_password("ParentPass123!"),
                role="parent",
            )
            db.add(parent)
            db.commit()
            print("Parent user created: parent1 / ParentPass123!")
        else:
            print("Parent user already exists.")

        # Create sample classes if not exists
        sample_classes = ["F1", "F2", "F3", "F4", "F5", "F6"]
        class_objects = []
        for class_name in sample_classes:
            existing_class = db.query(Class).filter(Class.name == class_name).first()
            if not existing_class:
                cls = Class(name=class_name)
                db.add(cls)
                db.commit()
                db.refresh(cls)
                class_objects.append(cls)
                print(f"Class '{class_name}' created.")
            else:
                class_objects.append(existing_class)
                print(f"Class '{class_name}' already exists.")

        # Retrieve parent and teacher users
        parent_user = db.query(User).filter(User.username == "parent1").first()
        teacher_user = db.query(User).filter(User.username == "teacher1").first()

        # Assign teacher to specific classes (e.g., F1 and F2)
        # Define the classes to assign the teacher to
        classes_to_assign = ["F1", "F2"]
        for cls in class_objects:
            if cls.name in classes_to_assign:
                # Check if the assignment already exists
                existing_assignment = db.query(TeacherClass).filter(
                    TeacherClass.teacher_id == teacher_user.id,
                    TeacherClass.class_id == cls.id
                ).first()
                if not existing_assignment:
                    assignment = TeacherClass(
                        teacher_id=teacher_user.id,
                        class_id=cls.id
                    )
                    db.add(assignment)
                    db.commit()
                    print(f"Assigned teacher1 to class '{cls.name}'.")
                else:
                    print(f"Teacher1 is already assigned to class '{cls.name}'.")

        # Create children for the parent
        existing_children = db.query(Child).filter(Child.parent_id == parent_user.id).all()
        if not existing_children:
            child1 = Child(
                parent_id=parent_user.id,
                first_name="Alice",
                last_name="Smith",
                class_id=class_objects[0].id,  # F1
            )
            child2 = Child(
                parent_id=parent_user.id,
                first_name="Bob",
                last_name="Smith",
                class_id=class_objects[1].id,  # F2
            )
            db.add_all([child1, child2])
            db.commit()
            print("Children Alice and Bob added for parent1.")
        else:
            print("Children already exist for parent1.")

        # Create announcements from the teacher
        # Corrected comparison using 'created_by_id'
        existing_announcements = db.query(Announcement).filter(
            Announcement.created_by_id == teacher_user.id
        ).all()
        if not existing_announcements:
            announcement1 = Announcement(
                title="Welcome to F1!",
                body="We will start with basic lessons next week.",
                created_by_id=teacher_user.id,  # Use 'created_by_id' instead of 'created_by'
                recipient_type="class",
                recipient_id=class_objects[0].id,  # F1
            )
            announcement2 = Announcement(
                title="F2 Activity Reminder",
                body="Don't forget to prepare for the upcoming activity.",
                created_by_id=teacher_user.id,  # Use 'created_by_id' instead of 'created_by'
                recipient_type="class",
                recipient_id=class_objects[1].id,  # F2
            )
            db.add_all([announcement1, announcement2])
            db.commit()
            print("Announcements created by teacher1.")
        else:
            print("Announcements already exist for teacher1.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
