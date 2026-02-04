from app import app
from flask import jsonify,g
from flask import request
from app.services.validators.role import permission_required
from app.db.users_db import dar_datos_usuario,get_all_users,validar_datos_usuario,get_user_by_ID,get_user_by_EMAIL,get_user_by_NAME,delete_user_by_id,hashear_contraseña_user,pedir_contraseña_hash_by_email
from app.services.validators.services import update_user_by_id,generar_jwt
from app.services.make_admin import hacer_admin_function
from app.services.validators.services_password import hash_password,renovar_contrasena_email,login_contrasena_email
import sqlite3
from app.services.validators.auth import jwt_required

@app.route("/users", methods = ["GET"])
@jwt_required
@permission_required("view_admin_panel")
def get_users():
    print(request.method)
    try:
        users_all = get_all_users()
        return jsonify(users_all)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route("/register", methods = ["POST"])
def create_user_url():
    if not request.is_json:
        return jsonify({"error": "JSON requerido"}), 400
    try:
        data = request.json
        data_user  = validar_datos_usuario(data)
        return jsonify(data_user), 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 400

@app.route("/users/<int:id>")
@jwt_required
@permission_required("read_profile")
def user_only_id(id):
    try:
        user = get_user_by_ID(id)
        return jsonify(user)
    except TypeError:
        return jsonify({"Error": "El usuario no fue encontrado o no existe.", "Attr": "ID"}), 404

@app.route("/users/<int:id>", methods = ["PUT"])
@jwt_required
@permission_required("update_user")
def user_update_id(id):
    try:
        data = request.json
        name = data.get("name")
        age = data.get("age")
        email = data.get("email")
        update_user_by_id(id,name,age,email)
        return jsonify(f"Se actualizo correctamente{f' ,el Nombre se cambio a {name}' if name else ''}{f' ,la Edad se cambio a {age}' if age else ''}{f' ,el Email se cambio a {email}' if email else ''} del usuario {id}"), 200
    except TypeError:
        return jsonify({"Error": "El usuario no fue encontrado o no existe.", "Attr": "ID"}), 404

@app.route("/users/email/<string:email>")
@jwt_required
@permission_required("read_profile")
def user_only_email(email):
    try:    
        user = get_user_by_EMAIL(email)
        return jsonify(user)
    except TypeError:
        return jsonify({"Error": "El usuario no fue encontrado o no existe.", "Attr": "Email"}), 404


@app.route("/users/name/<string:name>")
@jwt_required
@permission_required("read_profile")
def user_only_name(name):
    try:
        user = get_user_by_NAME(name)
        return jsonify(user)
    except TypeError:
        return jsonify({"Error": "El usuario no fue encontrado o no existe.", "Attr": "Name"}), 404
    
@app.route("/users/<int:id>", methods = ["DELETE"])
@jwt_required
@permission_required("delete_user")
def delete_id(id):
    try:
        data = request.json
        password = data.get("password")
        return jsonify(delete_user_by_id(id,password))
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    

# @app.route("/users/<int:id>/password", methods = ["PUT"])
# def update_password(id):
#     try:
#         data = request.json
#         password = data.get("password")
#         new_password = data.get("new_password")
#         print(password,new_password)
#         verificar_contraseña(password,new_password, id)
#         return jsonify({"message": "La contraseña fue actualizada correctamente"}), 200
#     except Exception as ve:
#         return jsonify({"Error": str(ve)}), 400
    
@app.route("/login", methods = ["POST"])
def login_user():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        user = get_user_by_EMAIL(email)
        if "Error" in user:
            return jsonify({"Error": "El usuario no fue encontrado o no existe.", "Attr": "Email"}), 404
        login_contrasena_email(password, email)
        token = generar_jwt(user["id"])
        return jsonify({"message": "Inicio de sesión exitoso", "token": token}), 200
    except Exception as ve:
        return jsonify({"Error": str(ve)}), 500
     
@app.route("/mis-datos", methods = ["GET"])
@jwt_required 
@permission_required("read_profile")
def my_data():      
    return jsonify(dar_datos_usuario(g.user_id)), 200


@app.route("/renew-password", methods = ["PUT"])
@jwt_required
@permission_required("update_user")
def renew_password():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        new_password = data.get("new_password")
        user = get_user_by_EMAIL(email)
        if "Error" in user:
            return jsonify({"Error": "El usuario no fue encontrado o no existe.", "Attr": "Email"}), 404
        renovar_contrasena_email(password, new_password, email)
        return jsonify({"message": "La contraseña fue actualizada correctamente"}), 200
    except Exception as ve:
        return jsonify({"Error": str(ve)}), 400


@app.route("/admin", methods = ["POST"])
@jwt_required
@permission_required("view_admin_panel")
def admin_route():
    return jsonify({"message": "Ruta de administración accesible"}), 200

@app.route("/make-admin/<int:id>", methods = ["POST"])
@jwt_required
@permission_required("view_admin_panel")
def make_admin(id):
    try:
        return jsonify(hacer_admin_function(id))
    except Exception as e:
        return jsonify({"Error": str(e)}), 500