from app.db.users_db import get_connection
from flask import jsonify
from werkzeug.security import check_password_hash,generate_password_hash

data_base_user = "users.db"


def renovar_contrasena_email(password, new_password, email):
    conn = get_connection(data_base_user)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if check_password_hash(row[0], password):
        hashed_new_password = generate_password_hash(new_password)
        conn = get_connection(data_base_user)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_new_password, email))
        conn.commit()
        cursor.close()
        conn.close()
    if not check_password_hash(row[0], password) and not (not password or not new_password) :
        raise ValueError("La contraseña no es correcta.")
    if not password or not new_password:
        raise ValueError("La contraseña no puede estar vacía.")


def login_contrasena_email(password, email):
    conn = get_connection(data_base_user)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close() 
    if check_password_hash(row[0], password):
        conn = get_connection(data_base_user)
        cursor = conn.cursor()
        conn.commit()
        cursor.close()
        conn.close()
    if not check_password_hash(row[0], password) and not (not password) :
        raise ValueError("La contraseña no es correcta.")
    if not password:
        raise ValueError("La contraseña no puede estar vacía.")
    
        
def hash_password(password):
    return generate_password_hash(password)


def verificar_user_contraseña(hash_password,password):
    if not check_password_hash(hash_password, password):
        raise ValueError("La contraseña no es correcta.")
    if not password:
        raise ValueError("La contraseña no puede estar vacía.")
    if check_password_hash(hash_password, password):
        return True
    