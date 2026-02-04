import email
import sqlite3
from flask import jsonify
from app.db.connection import get_connection
from werkzeug.security import generate_password_hash
from app.services.validators.services_password import hash_password,verificar_user_contraseña
import re
data_base_user = "users.db"
 


def get_all_users():
    try:
        conn = get_connection(data_base_user)
        cursor = conn.cursor()

        cursor.execute("SELECT id, email, name, age FROM users")
        rows = cursor.fetchall()

        users = []

        for row in rows:
            users.append(
                {
                    "id" : row[0],
                    "name" : row[2],
                    "age" : row[3],
                    "email" : row[1]
                }
            )
        cursor.close()
        conn.close()
    except Exception as e:
        return {"Error": str(e)}

    return users

def validar_datos_usuario(data):
    name = data.get("name")
    age = data.get("age")
    email = data.get("email")
    passwords = data.get("password")


    hash = hash_password(passwords)

    EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"

    if name is None or age is None or email is None or passwords is None:
        raise ValueError("Los campos seleccionados son obligatorios.")
    elif age < 12 or age > 120:
        raise ValueError("La edad no puede ser un valor negativo ni mayor a 120 años.")
    elif not re.match(EMAIL_REGEX, email):
        raise ValueError("El email proporcionado no es válido.")
    elif len(passwords) < 6 or passwords.isalpha() or passwords.isdigit():
            raise ValueError("La contraseña debe tener al menos 6 caracteres, incluyendo letras y números.")
    else:
        return create_user(name,age,email,hash)
def create_user(name,age,email,passwords):

    conn = get_connection(data_base_user)

    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (email,name,password,age) VALUES (?,?,?,?)", (email, name, passwords, age))

    conn.commit()

    cursor.close()
    
    return {"name": name, "age": age, "email": email, "id": cursor.lastrowid}


def get_user_by_ID(id):
    try:
        conn = get_connection(data_base_user)
        cursor = conn.cursor()

        cursor.execute("SELECT id, email, name, age, role_id FROM users WHERE id = ?", (id,))
        
    except Exception as e:
        return {"Error": str(e)}
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "name": row[2],
        "age": row[3],
        "email": row[1]
    }
def get_user_by_EMAIL(email):
    try:
        conn = get_connection(data_base_user)
        cursor = conn.cursor()

        cursor.execute("SELECT id, email, name, age FROM users WHERE email = ?", (email,))
        
    except Exception as e:
        return {"Error": str(e)}
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "name": row[1],
        "age": row[2],
        "email": row[3]
    }

def get_user_by_NAME(name):
    try:
        conn = get_connection(data_base_user)
        cursor = conn.cursor()

        cursor.execute("SELECT id, email, name, age FROM users WHERE name = ?", (name,))
    except Exception as e:
        return {"Error": str(e)}
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "name": row[1],
        "age": row[2],
        "email": row[3]
    }
def delete_user_by_id(id,password):
    try:
        conn = get_connection(data_base_user)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        verificar_user_contraseña(row[0],password)
        cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        if cursor.rowcount == 0:
            return ({"Error": "El usuario no existe.", "Attr": "ID"}), 404
        return ({"message": f"Usuario {id} eliminado correctamente"}), 200
    except Exception as e:
        return ({"Error": str(e)}), 500
    

def hashear_contraseña_user(user,password):
    conn = get_connection(data_base_user)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user))
    conn.commit()
    cursor.close()
    conn.close()


def pedir_contraseña_hash_by_email(email):
    conn = get_connection(data_base_user)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0]

def dar_datos_usuario(user_id):
    try:   
        conn = get_connection(data_base_user)
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, name, age FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        return {
            "id": row[0],
            "name": row[2],
            "age": row[3],
            "email": row[1]
        }
    except Exception as e:
        return {"Error": str(e)}
    
def role_for_user(user_id):
    try:   
        conn = get_connection(data_base_user)
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        role_id = row[0]
        cursor.execute("SELECT permission_id FROM role_permissions WHERE role_id = ?", (role_id,))
        permissions_id = cursor.fetchall()
        cursor.execute("SELECT name FROM permissions WHERE id IN (?,?,?,?)" , (permissions_id[0][0],permissions_id[1][0] if len(permissions_id) > 1 else 0,permissions_id[2][0] if len(permissions_id) > 2 else 0,permissions_id[3][0] if len(permissions_id) > 3 else 0,))
        permissions = cursor.fetchall()
        cursor.close()
        conn.close()

        return permissions
    except Exception as e:
        return {"Error": str(e)}
    
def admin_db(user_id):
    try:   
        conn = get_connection(data_base_user)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role_id = 2 WHERE id = ?", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"El usuario con ID {user_id} ha sido promovido a administrador."}
    except Exception as e:
        return {"Error": str(e)}