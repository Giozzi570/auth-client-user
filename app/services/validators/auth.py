from functools import wraps
from flask import jsonify,request,g
import jwt
import os

def jwt_required(fn):
    # Decorator to protect routes with JWT authentication
    @wraps(fn) 
    def wrapper(*args, **kwargs): 
        # Args and kwargs to pass to the decorated function

        SECRET_KEY = os.getenv("SECRET_KEY") 

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

            # Variable of the request context

            return fn(*args, **kwargs)

            # return the original function

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        
        # General exception handling
    return wrapper

