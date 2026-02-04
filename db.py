import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

permissions = ["read_profile", "edit_profile", "delete_profile", "view_admin_panel"]


cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER,
    password TEXT NOT NULL,
    role_id INTEGER DEFAULT 1
)""")

conn.commit()
conn.close()
