from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash, session

pymysql.install_as_MySQLdb()
app = Flask(__name__, static_folder='static')
app.secret_key = 'ANGIESECRETA'

#app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/seminario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la tabla de usuarios
class Usuarios(db.Model):
    _tablename_ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['contrasena']

        user = Usuarios.query.filter_by(usuario=username).first()

        if user and user.contrasena == password:
            session['user_id'] = user.id_usuario
            session['username'] = user.usuario
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos')

    return render_template('Login.html')

@app.route('/')
def home():
    return render_template('layout.html', tab='informacion')

@app.route('/pedidos')
@app.route('/informacion')
def tab1(tab=None):
    if tab is None:
        tab = 'pedidos'
    if tab == 'informacion':
        return render_template('layout.html', tab=tab)
    elif tab == 'pedidos' and 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('layout.html', tab=tab)

@app.route('/logout')
def logout():
    # Clear the user's session
    session.clear()
    # Redirect to the login page
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)