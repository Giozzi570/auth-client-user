from app.db.users_db import admin_db

def hacer_admin_function(id):
    # Lógica para asignar el rol de administrador al usuario con el ID proporcionado
    # Aquí se debería interactuar con la base de datos para actualizar el rol del usuario
    # Por simplicidad, asumimos que la operación es exitosa
    result = admin_db(id)
    return result