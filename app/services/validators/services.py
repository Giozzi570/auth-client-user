from app.db.users_db import get_connection,role_for_user
from flask import jsonify,request,g
from werkzeug.security import check_password_hash,generate_password_hash
import jwt
from datetime import datetime, timedelta
import os
from functools import wraps

data_base_user = "users.db"


def update_user_by_id(id= None, name=None, age=None, email=None):
    try:
        conn = get_connection(data_base_user)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = ?, age = ?, email = ? WHERE id = ?", (name, age, email, id))
        conn.commit()
        cursor.close()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({"Error": "El usuario no existe.", "Attr": "ID"}), 404
        return jsonify({"message": f"Usuario actualizado correctamente {id}"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
from datetime import datetime, timedelta

def generar_jwt(user_id):
    persmissions = role_for_user(user_id)
    print(persmissions)
    payload = {
        "user_id": user_id,
        "permissions" : persmissions,   
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    SECRET_KEY = os.getenv("SECRET_KEY")

    print("SECRET_KEY GENERAR:", SECRET_KEY)

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return token
def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        SECRET_KEY = os.getenv("SECRET_KEY")

        print("SECRET_KEY VERIFICAR:", SECRET_KEY)
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"error": "Unauthorized"}), 401

        try:
            token = auth.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data.get("user_id")

            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401
            
            g.user_id = user_id

            return fn(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Unauthorized"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Unauthorized"}), 401

