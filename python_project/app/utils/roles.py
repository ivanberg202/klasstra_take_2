# filename: app/utils/roles.py
def can_create_announcements(role: str) -> bool:
    return role in ["teacher", "class_rep", "admin"]

def can_manage_users(role: str) -> bool:
    return role == "admin"

def is_parent(role: str) -> bool:
    return role in ["parent", "class_rep"]
