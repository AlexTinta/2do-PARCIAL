from flask import Flask, session, request, redirect, url_for, render_template, flash
import datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

# Inicializar sesión para los productos
@app.before_request
def init_session():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    productos = session['productos']
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    nuevo_producto = {
        'id': request.form['id'],
        'nombre': request.form['nombre'],
        'cantidad': request.form['cantidad'],
        'precio': request.form['precio'],
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }

    # Verificar que el ID sea único
    for producto in session['productos']:
        if producto['id'] == nuevo_producto['id']:
            flash('El ID debe ser único. Producto no agregado.', 'error')
            return redirect(url_for('index'))

    # Agregar producto a la sesión
    session['productos'].append(nuevo_producto)
    session.modified = True
    flash('Producto agregado exitosamente.', 'success')
    return redirect(url_for('index'))

@app.route('/eliminar/<string:id>', methods=['POST'])
def eliminar_producto(id):
    session['productos'] = [producto for producto in session['productos'] if producto['id'] != id]
    session.modified = True
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('index'))

@app.route('/editar/<string:id>', methods=['POST'])
def editar_producto(id):
    for producto in session['productos']:
        if producto['id'] == id:
            producto['nombre'] = request.form['nombre']
            producto['cantidad'] = request.form['cantidad']
            producto['precio'] = request.form['precio']
            producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
            producto['categoria'] = request.form['categoria']
            break
    session.modified = True
    flash('Producto editado exitosamente.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
