from flask import Blueprint, request, jsonify, make_response

from app import db
from models import Equipo

from schemas import EquipoSchema , EquipoMinimalSchema

from flask_jwt_extended import(
    jwt_required,               #para saber si el usuario esta autenticado
    get_jwt,                    #para saber si el usuario es admin
)

equipo_bp = Blueprint('equipo', __name__)

@equipo_bp.route("/equipos", methods=["GET"])
@jwt_required()  
def equipos():
    additional_data = get_jwt() 
    administrador = additional_data.get("administrador", False)  

    equipos = Equipo.query.all()  
    if administrador: 
        return EquipoSchema().dump(equipos, many=True) 
    else:  
        return EquipoMinimalSchema().dump(equipos, many=True)  

@equipo_bp.route("/equipos/crear", methods=["POST"])
@jwt_required()
def crear_equipo():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    if request.method == "POST":
        if administrador:
            data = request.get_json()  # Obtener los datos enviados en formato JSON
            
            # Validar el valor de 'activo' (0 o 1)
            activo = data.get("activo", 1)
            if activo not in [0, 1]:
                return jsonify({"Mensaje": "El valor de 'activo' debe ser 0 o 1."}), 400

            # Crear una nueva instancia del equipo usando los datos proporcionados
            nuevo_equipo = Equipo(
                nombre=data.get("nombre"),
                modelo_id=data.get("modelo_id"),
                categoria_id=data.get("categoria_id"),
                costo=data.get("costo"),
                stock_id=data.get("stock_id"),
                activo=activo,  # Establecer 'activo' como 1 o 0 según la validación
                marca_id=data.get("marca_id"),
            )  

            # Agregar el nuevo equipo a la sesión de la base de datos
            db.session.add(nuevo_equipo)
            db.session.commit()  # Confirmar los cambios en la base de datos

            # Retornar el equipo creado en formato JSON con código 201
            return make_response(EquipoSchema().dump(nuevo_equipo), 201)

        return jsonify({"Mensaje": "Debes ser admin para crear un equipo"}), 403

@equipo_bp.route("/equipos/actualizar", methods=["PUT"])
@jwt_required()
def actualizar_equipo():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    if not administrador:
        return jsonify({"Mensaje": "No tiene permisos para actualizar un equipo."}), 403

    data = request.get_json()
    equipo_id = data.get("id")
    equipo = Equipo.query.get_or_404(equipo_id)

    # Validar el valor de 'activo' (0 o 1)
    if 'activo' in data and data['activo'] not in [0, 1]:
        return jsonify({"Mensaje": "El valor de 'activo' debe ser 0 o 1."}), 400

    equipo.nombre = data.get("nombre", equipo.nombre)
    equipo.modelo_id = data.get("modelo_id", equipo.modelo_id)
    equipo.categoria_id = data.get("categoria_id", equipo.categoria_id)
    equipo.costo = data.get("costo", equipo.costo)
    equipo.stock_id = data.get("stock_id", equipo.stock_id)
    equipo.marca_id = data.get("marca_id", equipo.marca_id)
    equipo.activo = data.get("activo", equipo.activo)  # Actualizar solo si se pasa un valor válido
    
    db.session.commit()
    return make_response(EquipoSchema().dump(equipo), 200)

@equipo_bp.route("/equipos/eliminar", methods=["DELETE"])
@jwt_required()
def eliminar_equipo():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    if not administrador:
        return jsonify({"Mensaje": "No tiene permisos para eliminar un equipo."}), 403

    equipo_id = request.json.get("id")
    if not equipo_id:
        return jsonify({"Mensaje": "Falta el parámetro 'id' en la solicitud."}), 400

    equipo = Equipo.query.get_or_404(equipo_id)
    equipo.activo = False  # Marcar el equipo como inactivo
    db.session.commit()
    return jsonify({"Mensaje": "Equipo marcado como inactivo correctamente."}), 200
