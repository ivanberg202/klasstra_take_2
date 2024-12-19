# filename: app/main.py
from fastapi import FastAPI
from app.routers import auth, users, classes, announcements, children, admin
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Klasstra")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classes.router)
app.include_router(announcements.router)
app.include_router(children.router)
app.include_router(admin.router)
