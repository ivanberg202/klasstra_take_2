# filename: app/seed.py
import sys
import os

# Add the project root to sys.path to allow imports from 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def seed():
    db = SessionLocal()
    try:
        # Check if admin user already exists
        if not db.query(User).filter(User.username == "admin").first():
            # Create an admin user
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
    finally:
        db.close()

if __name__ == "__main__":
    seed()
