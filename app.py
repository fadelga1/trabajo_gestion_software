from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Usuario, Categoria, Plato, Pedido, ItemPedido, Reserva, CierreCaja
from datetime import datetime, date
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sigr-secret-key-cambiar-en-produccion'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sigr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

# ---------- DECORADORES ----------
def rol_requerido(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ---------- AUTH ----------
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciales inválidas', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return redirect(url_for('register'))
        user = Usuario(nombre=nombre, email=email, rol='cliente')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso, inicia sesión', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', registro=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('base.html', dashboard=True)

# ---------- MENÚ DIGITAL ----------
@app.route('/menu')
@login_required
def menu():
    categorias = Categoria.query.all()
    return render_template('menu.html', categorias=categorias)

@app.route('/admin/menu')
@rol_requerido('admin')
def admin_menu():
    categorias = Categoria.query.all()
    return render_template('admin_menu.html', categorias=categorias)

# CRUD Categorías
@app.route('/admin/categoria', methods=['POST'])
@rol_requerido('admin')
def crear_categoria():
    nombre = request.form['nombre']
    if nombre:
        db.session.add(Categoria(nombre=nombre))
        db.session.commit()
    return redirect(url_for('admin_menu'))

@app.route('/admin/categoria/<int:cid>/delete', methods=['POST'])
@rol_requerido('admin')
def eliminar_categoria(cid):
    c = Categoria.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('admin_menu'))

# CRUD Platos
@app.route('/admin/plato', methods=['POST'])
@rol_requerido('admin')
def crear_plato():
    plato = Plato(
        nombre=request.form['nombre'],
        descripcion=request.form.get('descripcion', ''),
        precio=float(request.form['precio']),
        categoria_id=int(request.form['categoria_id']),
        disponible=True
    )
    db.session.add(plato)
    db.session.commit()
    return redirect(url_for('admin_menu'))

@app.route('/admin/plato/<int:pid>/update', methods=['POST'])
@rol_requerido('admin')
def actualizar_plato(pid):
    p = Plato.query.get_or_404(pid)
    p.nombre = request.form['nombre']
    p.descripcion = request.form.get('descripcion', '')
    p.precio = float(request.form['precio'])
    p.disponible = 'disponible' in request.form
    p.categoria_id = int(request.form['categoria_id'])
    db.session.commit()
    return redirect(url_for('admin_menu'))

@app.route('/admin/plato/<int:pid>/delete', methods=['POST'])
@rol_requerido('admin')
def eliminar_plato(pid):
    p = Plato.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('admin_menu'))

# ---------- PEDIDOS ----------
@app.route('/pedidos')
@login_required
def pedidos():
    if current_user.rol == 'cliente':
        lista = Pedido.query.filter_by(cliente_id=current_user.id).order_by(Pedido.fecha.desc()).all()
    elif current_user.rol == 'mesero':
        lista = Pedido.query.order_by(Pedido.fecha.desc()).limit(50).all()
    else:  # admin
        lista = Pedido.query.order_by(Pedido.fecha.desc()).all()
    return render_template('pedidos.html', pedidos=lista)

@app.route('/pedido/nuevo', methods=['POST'])
@rol_requerido('cliente', 'mesero', 'admin')
def nuevo_pedido():
    plato_ids = request.form.getlist('plato_id')
    cantidades = request.form.getlist('cantidad')
    if not plato_ids:
        flash('Debes agregar al menos un plato', 'error')
        return redirect(url_for('menu'))

    pedido = Pedido(
        cliente_id=current_user.id if current_user.rol == 'cliente' else None,
        mesero_id=current_user.id if current_user.rol in ('mesero', 'admin') else None,
        estado='pendiente'
    )
    db.session.add(pedido)
    db.session.flush()

    total = 0
    for pid, cant in zip(plato_ids, cantidades):
        plato = Plato.query.get(int(pid))
        if plato and plato.disponible:
            c = max(1, int(cant))
            subtotal = plato.precio * c
            total += subtotal
            db.session.add(ItemPedido(
                pedido_id=pedido.id,
                plato_id=plato.id,
                cantidad=c,
                precio_unitario=plato.precio
            ))
    pedido.total = round(total, 2)
    db.session.commit()
    flash(f'Pedido #{pedido.id} creado. Total: ${pedido.total}', 'success')
    return redirect(url_for('pedidos'))

@app.route('/pedido/<int:pid>/estado', methods=['POST'])
@rol_requerido('mesero', 'admin')
def cambiar_estado(pid):
    pedido = Pedido.query.get_or_404(pid)
    nuevo = request.form['estado']
    if nuevo in ('pendiente', 'preparando', 'listo', 'entregado', 'pagado'):
        pedido.estado = nuevo
        db.session.commit()
    return redirect(url_for('pedidos'))

@app.route('/api/pedidos/seguimiento')
@login_required
def api_seguimiento():
    """Endpoint JSON para refresco en tiempo real (polling)."""
    if current_user.rol == 'cliente':
        lista = Pedido.query.filter_by(cliente_id=current_user.id).order_by(Pedido.id.desc()).limit(10).all()
    else:
        lista = Pedido.query.order_by(Pedido.id.desc()).limit(20).all()
    data = [{
        'id': p.id,
        'estado': p.estado,
        'total': p.total,
        'fecha': p.fecha.strftime('%Y-%m-%d %H:%M'),
        'items': [{'plato': i.plato.nombre, 'cantidad': i.cantidad} for i in p.items]
    } for p in lista]
    return jsonify(data)

# ---------- RESERVAS ----------

@app.route('/reservas', methods=['GET', 'POST'])
@login_required
def reservas():
    if request.method == 'POST':
        fecha_str = request.form['fecha']
        hora_str = request.form['hora']
        personas = int(request.form['personas'])
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()

        # validar duplicado (mismo cliente, fecha, hora)
        dup = Reserva.query.filter_by(
            cliente_id=current_user.id, fecha=fecha, hora=hora, estado='activa'
        ).first()
        if dup:
            flash('Ya tienes una reserva en ese horario', 'error')
        else:
            db.session.add(Reserva(
                cliente_id=current_user.id,
                fecha=fecha, hora=hora,
                personas=personas
            ))
            db.session.commit()
            flash('Reserva creada correctamente', 'success')
        return redirect(url_for('reservas'))

    if current_user.rol == 'cliente':
        lista = Reserva.query.filter_by(cliente_id=current_user.id).order_by(Reserva.fecha).all()
    else:
        lista = Reserva.query.order_by(Reserva.fecha, Reserva.hora).all()
    return render_template('reservas.html', reservas=lista, hoy=date.today())

@app.route('/reserva/<int:rid>/cancelar', methods=['POST'])
@login_required
def cancelar_reserva(rid):
    r = Reserva.query.get_or_404(rid)
    if current_user.rol == 'cliente' and r.cliente_id != current_user.id:
        abort(403)
    r.estado = 'cancelada'
    db.session.commit()
    return redirect(url_for('reservas'))

# ---------- CAJA Y REPORTES ----------
@app.route('/caja', methods=['GET', 'POST'])
@rol_requerido('admin')
def caja():
    if request.method == 'POST':
        hoy = date.today()
        if CierreCaja.query.filter_by(fecha=hoy).first():
            flash('La caja ya fue cerrada hoy', 'error')
            return redirect(url_for('caja'))
        pagados = Pedido.query.filter(
            db.func.date(Pedido.fecha) == hoy,
            Pedido.estado == 'pagado'
        ).all()
        total = sum(p.total for p in pagados)
        db.session.add(CierreCaja(
            fecha=hoy,
            total_ventas=round(total, 2),
            num_pedidos=len(pagados)
        ))
        db.session.commit()
        flash(f'Caja cerrada. Total: ${total:.2f} en {len(pagados)} pedidos', 'success')
        return redirect(url_for('caja'))

    hoy = date.today()
    pagados_hoy = Pedido.query.filter(
        db.func.date(Pedido.fecha) == hoy,
        Pedido.estado == 'pagado'
    ).all()
    total_hoy = sum(p.total for p in pagados_hoy)
    cierre_hoy = CierreCaja.query.filter_by(fecha=hoy).first()
    historial = CierreCaja.query.order_by(CierreCaja.fecha.desc()).limit(15).all()
    return render_template('caja.html',
                          total_hoy=total_hoy,
                          num_hoy=len(pagados_hoy),
                          cierre_hoy=cierre_hoy,
                          historial=historial,
                          hoy=hoy)

@app.route('/reportes')
@rol_requerido('admin')
def reportes():
    # Ventas por día (últimos 7 días)
    from sqlalchemy import func
    ventas = db.session.query(
        func.date(Pedido.fecha).label('dia'),
        func.sum(Pedido.total).label('total'),
        func.count(Pedido.id).label('num')
    ).filter(Pedido.estado == 'pagado').group_by(func.date(Pedido.fecha))\
     .order_by(func.date(Pedido.fecha).desc()).limit(7).all()

    # Top platos
    top = db.session.query(
        Plato.nombre,
        func.sum(ItemPedido.cantidad).label('cantidad'),
        func.sum(ItemPedido.cantidad * ItemPedido.precio_unitario).label('monto')
    ).join(ItemPedido).join(Pedido)\
     .filter(Pedido.estado == 'pagado')\
     .group_by(Plato.id).order_by(func.sum(ItemPedido.cantidad).desc()).limit(10).all()

    return render_template('reportes.html', ventas=ventas, top=top)

# ---------- INICIALIZAR BD ----------
def init_db():
    with app.app_context():
        db.create_all()
        if not Usuario.query.first():
            admin = Usuario(nombre='Administrador', email='admin@sigr.com', rol='admin')
            admin.set_password('admin123')
            mesero = Usuario(nombre='Mesero Demo', email='mesero@sigr.com', rol='mesero')
            mesero.set_password('mesero123')
            cliente = Usuario(nombre='Cliente Demo', email='cliente@sigr.com', rol='cliente')
            cliente.set_password('cliente123')
            db.session.add_all([admin, mesero, cliente])

            c1 = Categoria(nombre='Entradas')
            c2 = Categoria(nombre='Platos Fuertes')
            c3 = Categoria(nombre='Bebidas')
            c4 = Categoria(nombre='Postres')
            db.session.add_all([c1, c2, c3, c4])
            db.session.flush()

            db.session.add_all([
                Plato(nombre='Ensalada César', descripcion='Lechuga, pollo, crutones', precio=8.5, categoria_id=c1.id),
                Plato(nombre='Sopa del día', descripcion='Sopa casera', precio=6.0, categoria_id=c1.id),
                Plato(nombre='Pasta Alfredo', descripcion='Fettuccine con salsa cremosa', precio=14.0, categoria_id=c2.id),
                Plato(nombre='Parrilla Mixta', descripcion='Res, pollo y cerdo', precio=22.0, categoria_id=c2.id),
                Plato(nombre='Limonada', descripcion='Natural', precio=3.5, categoria_id=c3.id),
                Plato(nombre='Café americano', descripcion='100% colombiano', precio=2.5, categoria_id=c3.id),
                Plato(nombre='Tiramisú', descripcion='Receta italiana', precio=7.0, categoria_id=c4.id),
            ])
            db.session.commit()
            print("✅ BD inicializada con usuarios y menú demo.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)