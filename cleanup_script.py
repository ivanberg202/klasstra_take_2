import os
import shutil

# List of all paths created by the setup script
project_structure = [
    "python_project/app/core/config.py",
    "python_project/app/core/database.py",
    "python_project/app/core/security.py",
    "python_project/app/core/auth.py",
    "python_project/app/models/user.py",
    "python_project/app/models/class_.py",
    "python_project/app/models/announcement.py",
    "python_project/app/models/child.py",
    "python_project/app/models/audit_log.py",
    "python_project/app/schemas/common.py",
    "python_project/app/schemas/user.py",
    "python_project/app/schemas/class_.py",
    "python_project/app/schemas/announcement.py",
    "python_project/app/schemas/child.py",
    "python_project/app/schemas/auth.py",
    "python_project/app/utils/roles.py",
    "python_project/app/utils/rate_limit.py",
    "python_project/app/routers/auth.py",
    "python_project/app/routers/users.py",
    "python_project/app/routers/classes.py",
    "python_project/app/routers/announcements.py",
    "python_project/app/routers/children.py",
    "python_project/app/routers/admin.py",
    "python_project/app/main.py",
    "vue_js_project/postcss.config.js",
    "vue_js_project/tailwind.config.js",
    "vue_js_project/src/main.js",
    "vue_js_project/src/assets/tailwind.css",
    "vue_js_project/src/store/index.js",
    "vue_js_project/src/router.js",
    "vue_js_project/src/App.vue",
    "vue_js_project/src/components/Navbar.vue",
    "vue_js_project/src/components/ThemeToggle.vue",
    "vue_js_project/src/components/AnnouncementCard.vue",
    "vue_js_project/src/layouts/DefaultLayout.vue",
    "vue_js_project/src/pages/LoginPage.vue",
    "vue_js_project/src/pages/RegisterPage.vue",
    "vue_js_project/src/pages/DashboardTeacher.vue",
    "vue_js_project/src/pages/DashboardParent.vue",
    "vue_js_project/src/pages/DashboardAdmin.vue",
    "vue_js_project/public/index.html",
]

def cleanup_files():
    for path in project_structure:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted: {path}")
    # Clean up empty directories
    for path in project_structure:
        dir_path = os.path.dirname(path)
        if os.path.exists(dir_path) and not os.listdir(dir_path):
            shutil.rmtree(dir_path)
            print(f"Deleted directory: {dir_path}")
    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup_files()
