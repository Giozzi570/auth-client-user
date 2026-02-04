from app.db.users_db import role_for_user
from functools import wraps
from flask import jsonify,request,g
from app import app
from jwt import decode
import os


from functools import wraps
from flask import request, jsonify, g
from jwt import decode
import os

def permission_required(permission_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization")
            if not auth:
                return jsonify({"error": "Unauthorized"}), 401

            SECRET_KEY = os.getenv("SECRET_KEY") 
            try:
                token = auth.split(" ")[1]
                data = decode(token, SECRET_KEY, algorithms=["HS256"])
                permissions_auth = data.get("permissions", [])

                permissions = [perm[0] for perm in permissions_auth]
                print("PERMISSIONS EN DECORADOR:", permissions)
                
                if permission_name not in permissions:
                    return jsonify({"error": "Forbidden"}), 403

                # Llamás a la ruta original
                return fn(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": "Unauthorized"}), 401

        return wrapper
    return decorator
