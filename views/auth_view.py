#para tiempo de vencimiento
from datetime import timedelta

from flask import Blueprint, request, jsonify, make_response, render_template

#crear token
from flask_jwt_extended import(
    create_access_token,
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)

#encriptar password
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from app import db
from models import User, Equipo

#importar schemas
from schemas import UserSchema

#autorizaciones de rutas
auth_bp = Blueprint('auth', __name__)

#crear token de login con post
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.authorization        #para saber la informacion del usuario
    username = data.username
    password = data.password

    usuario = User.query.filter_by(username=username).first()        #para saber si el usuario existe

    # si el usuario existe y coincide las contraseñas
    if usuario and check_password_hash(    #recibe contraseña hasheada y la contraseña del usuario
        pwhash = usuario.password_hash,
        password = password
    ):
        access_token = create_access_token(                     #para crear el token
            identity = username,                                #identidad del usuario
            expires_delta = timedelta(minutes=30),              #tiempo de expiración
            additional_claims=dict(                             #para saber si el usuario es admin
                administrador = usuario.is_admin
            )
        )
        #una ves ya creado el token, lo devolvemos
        return jsonify({'Token':f'Bearer {access_token}'})

    return jsonify(Mensaje ="El nombre de usuario o la contraseña son incorrectos")

#listar todos los usuarios
@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()  # Solo los usuarios autenticados pueden acceder
def users():
    additional_data = get_jwt()  # Obtener los datos del JWT para validar el rol
    administrador = additional_data.get('administrador', False)

    # Acción POST: Crear nuevo usuario solo si es administrador
    if request.method == 'POST':
        if administrador:
            data = request.get_json()  # Obtiene la información del usuario
            username = data.get('usuario')
            password = data.get('contrasenia')

            # Validar los datos antes de crear el usuario
            data_a_validar = dict(
                username=username,
                password_hash=password,
                is_admin=False
            )
            errors = UserSchema().validate(data_a_validar)
            if errors:
                return make_response(jsonify(errors))

            try:
                # Crear nuevo usuario
                nuevo_usuario = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=False,
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return jsonify(
                    {
                        "Mensaje": "Usuario creado",
                        "Usuario": nuevo_usuario.to_dict()
                    }
                )
            except Exception as e:
                return jsonify(
                    {
                        "Mensaje": "Fallo al crear el usuario",
                        "Error": str(e)
                    }
                )
        else:
            return jsonify(Mensaje="Solo el admin puede crear nuevos usuarios"), 403

    # Acción GET: Trae todos los usuarios
    if administrador:
        usuarios = User.query.all()  # Solo los administradores pueden ver todos los usuarios
        return UserSchema().dump(obj=usuarios, many=True)  # Devuelve todos los usuarios con más detalles
    else:
        return jsonify(Mensaje="No tiene permisos para ver los usuarios."), 403  # Si no es admin, denegar acceso

# Actualizar usuario
@auth_bp.route('/user/actualizar', methods=['PUT'])
@jwt_required()
def update_user():
    additional_data = get_jwt()
    administrador = additional_data['administrador']

    if not administrador:
        return jsonify({"Mensaje": "Solo un administrador puede actualizar usuarios."}), 403

    data = request.get_json()
    user_id = data.get("id")
    usuario = User.query.get_or_404(user_id)

    # Validamos y actualizamos los datos del usuario
    username = data.get('usuario', usuario.username)  # Si no se pasa un nuevo username, se mantiene el actual
    password = data.get('contrasenia')
    activo = data.get('activo', usuario.activo)  # Si no se pasa un nuevo valor, se queda con el actual

    if password:
        usuario.password_hash = generate_password_hash(password)
    usuario.username = username
    usuario.activo = activo  # Actualizamos el estado activo del usuario

    # Guardar cambios
    db.session.commit()

    return make_response(usuario.to_dict(), 200)

# Eliminar usuario
@auth_bp.route('/user/eliminar', methods=['DELETE'])
@jwt_required()
def delete_user():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)

    if not administrador:
        return jsonify(Mensaje="Solo un administrador puede eliminar usuarios"), 403

    # Leer el 'id' del cuerpo de la solicitud (JSON)
    data = request.get_json()
    usuario_id = data.get('id')

    if not usuario_id:
        return jsonify({"Mensaje": "Falta el parámetro 'id' en la solicitud."}), 400

    usuario = User.query.get_or_404(usuario_id)  # Buscar el usuario por el ID

    # Desactivar al usuario (marcar como inactivo)
    usuario.activo = 0  # Usamos 0 para marcar como inactivo
    db.session.commit()

    return jsonify(Mensaje="Usuario desactivado exitosamente"), 200


# Inicio
@auth_bp.route('/')
def index():
    equipos = Equipo.query.all()
    return render_template('index.html', equipos=equipos)


