from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ---------- USUARIOS ----------
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # cliente, mesero, admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ---------- MENÚ ----------
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    platos = db.relationship('Plato', backref='categoria', cascade='all, delete')

class Plato(db.Model):
    __tablename__ = 'platos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

# ---------- PEDIDOS ----------
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, preparando, listo, entregado, pagado
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    mesero_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    total = db.Column(db.Float, default=0.0)
    items = db.relationship('ItemPedido', backref='pedido', cascade='all, delete')

class ItemPedido(db.Model):
    __tablename__ = 'items_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey('platos.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)
    plato = db.relationship('Plato')

# ---------- RESERVAS ----------
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    personas = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='activa')  # activa, cancelada
    cliente = db.relationship('Usuario')

# ---------- CAJA ----------
class CierreCaja(db.Model):
    __tablename__ = 'cierres_caja'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    total_ventas = db.Column(db.Float, default=0.0)
    num_pedidos = db.Column(db.Integer, default=0)
    hora_cierre = db.Column(db.DateTime, default=datetime.utcnow)