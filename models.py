from app import db  # Importar la instancia de db desde app.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password_hash
        }

class Equipo(db.Model):
    __tablename__ = 'equipo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    modelo_relacionado = db.relationship('Modelo', backref='equipos')
    categoria_relacionada = db.relationship('Categoria', backref='equipos')
    stock_relacionado = db.relationship('Stock', backref='equipos')
    marca_relacionada = db.relationship('Marca', backref='equipos')

    accesorios = db.relationship('Accesorio', secondary='equipo_accesorio', backref='equipos')
    caracteristicas = db.relationship('Caracteristica', backref='equipo', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo_relacionado.nombre if self.modelo_relacionado else None,
            "categoria": self.categoria_relacionada.nombre if self.categoria_relacionada else None,
            "costo": self.costo,
            "marca": self.marca_relacionada.nombre if self.marca_relacionada else None,
            "stock": self.stock_relacionado.cantidad if self.stock_relacionado else None
        }

class Fabricante(db.Model):
    __tablename__ = 'fabricante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    pais_origen = db.Column(db.String(50))

    modelos = db.relationship('Modelo', backref='fabricante')

class Marca(db.Model):
    __tablename__ = 'marca'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

class Modelo(db.Model):
    __tablename__ = 'modelo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)

class Caracteristica(db.Model):
    __tablename__ = 'caracteristica'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(120), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "equipo_id": self.equipo_id
        }

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    contacto = db.Column(db.String(50))

    accesorios = db.relationship('Accesorio', backref='proveedor')

class Accesorio(db.Model):
    __tablename__ = 'accesorio'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    compatible_con = db.Column(db.String(50))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "compatible_con": self.compatible_con,
            "proveedor": self.proveedor.nombre if self.proveedor else None
        }

class EquipoAccesorio(db.Model):
    __tablename__ = 'equipo_accesorio'
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), primary_key=True)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), primary_key=True)

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(50))

    def actualizar_stock(self, cantidad_nueva):
        self.cantidad = cantidad_nueva
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "cantidad": self.cantidad,
            "ubicacion": self.ubicacion
        }
