# filename: app/main.py
from fastapi import FastAPI
from app.routers import auth, users, classes, announcements, children, admin, teacher, upload, parents, ai
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from sqlalchemy import text, inspect
from app.seed import seed  # Import the seed function


app = FastAPI(title="Klasstra")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # explicitly allow the Vue dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reset the database schema on startup
with engine.connect() as connection:
    connection = connection.execution_options(isolation_level="AUTOCOMMIT")  # Enable autocommit mode

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if tables:
        print("Dropping all tables except 'alembic_version'...")
        for table in tables:
            if table != "alembic_version":
                connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                print(f"Dropped table: {table}")
        print("All applicable tables dropped.")
    else:
        print("No tables found. Skipping drop.")

    print("Recreating tables...")
    Base.metadata.create_all(engine)
    print("Database tables created.")

# Seed the database with sample data
print("Seeding the database with sample data...")
seed()
print("Database seeding complete.")


# Include API routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classes.router)
app.include_router(announcements.router)
app.include_router(children.router)
app.include_router(admin.router)
app.include_router(teacher.router)
app.include_router(upload.router)
app.include_router(parents.router)
app.include_router(ai.router)


