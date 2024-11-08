from app import ma
from marshmallow import validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


from models import User, Equipo, Fabricante, Marca, Modelo, Caracteristica, Proveedor, Accesorio, EquipoAccesorio, Categoria, Stock

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    username = ma.auto_field()
    password_hash = ma.auto_field()
    is_admin = ma.auto_field()
    activo = ma.auto_field()
    
    #validates es un decorar que se usa para validar la informacion
    @validates('username')
    def validate_username(self, value):
        user = User.query.filter_by(username=value).first()
        if user is not None:
            raise ValidationError('El nombre de usuario ya existe')
        return value

class UserMinimalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
    username = ma.auto_field()

class EquipoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Equipo

    id = ma.auto_field()
    nombre = ma.auto_field()
    costo = ma.auto_field()
    activo = ma.auto_field()
    
    marca = ma.Nested('MarcaSchema', only=["nombre"])  
    modelo = ma.Nested('ModeloSchema', only=["nombre"])  
    categoria = ma.Nested('CategoriaSchema', only=["nombre"])  
    stock = ma.Nested('StockSchema', only=["ubicacion", "cantidad"])  

class EquipoMinimalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Equipo

    nombre = ma.auto_field() 
    costo = ma.auto_field()

class FabricanteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Fabricante
    id = ma.auto_field()
    nombre = ma.auto_field()
    pais_origen = ma.auto_field()

    @validates('nombre')
    def validate_nombre(self, value):
        if Fabricante.query.filter_by(nombre=value).first():
            raise ValidationError('El fabricante ya existe')
        return value

class MarcaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Marca
    id = ma.auto_field()
    nombre = ma.auto_field()

    @validates('nombre')
    def validate_nombre(self, value):
        if Marca.query.filter_by(nombre=value).first():
            raise ValidationError('La marca ya existe')
        return value

class ModeloSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Modelo
    id = ma.auto_field()
    nombre = ma.auto_field()
    fabricante_id = ma.auto_field()

    fabricante_relacionado = ma.Nested(FabricanteSchema)

class CaracteristicaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Caracteristica
    id = ma.auto_field()
    tipo = ma.auto_field()
    descripcion = ma.auto_field()
    equipo_id = ma.auto_field()

class ProveedorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Proveedor
    id = ma.auto_field()
    nombre = ma.auto_field()
    contacto = ma.auto_field()
    
    accesorios = ma.Nested('AccesorioSchema', many=True)

    @validates('nombre')
    def validate_nombre(self, value):
        if Proveedor.query.filter_by(nombre=value).first():
            raise ValidationError('El proveedor ya existe')
        return value

class AccesorioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Accesorio
    id = ma.auto_field()
    tipo = ma.auto_field()
    compatible_con = ma.auto_field()
    proveedor_id = ma.auto_field()

class EquipoAccesorioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EquipoAccesorio
    equipo_id = ma.auto_field()
    accesorio_id = ma.auto_field()

class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
    id = ma.auto_field()
    nombre = ma.auto_field()

    @validates('nombre')
    def validate_nombre(self, value):
        if Categoria.query.filter_by(nombre=value).first():
            raise ValidationError('La categoría ya existe')
        return value

class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stock
    id = ma.auto_field()
    cantidad = ma.auto_field()
    ubicacion = ma.auto_field()