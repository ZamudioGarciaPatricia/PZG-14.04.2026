from flask import Flask, render_template, request, redirect, url_for, flash
import gestor
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = 'gatitolula'

gestor_obj = gestor.GestorTareas("mongodb://127.0.0.1:27017/")

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/creacuenta', methods=['GET', 'POST'])
def creacuenta():
    if request.method == 'POST':
        u = request.form.get('user')
        e = request.form.get('email')
        s = request.form.get('secreto')
        
        password_encriptada = pbkdf2_sha256.hash(s)

        if gestor_obj.crear_usuario(u, e, password_encriptada):
            flash('¡Cuenta creada con éxito! Ahora puedes iniciar sesión.')
            return redirect(url_for('iniciasesion'))
        else:
            flash('Este correo ya esta registrado.')
            
    return render_template('crearcuenta.html')

@app.route('/iniciasesion', methods=['GET', 'POST'])
def iniciasesion():
    if request.method == 'POST':
        e = request.form.get('email')
        s = request.form.get('secreto') 
        
        user = gestor_obj.obtener_usuario_por_email(e)

        if user and pbkdf2_sha256.verify(s, user['secreto']):
            return redirect(url_for('tareas'))
        else:
            flash('datos incorrectos.')
            
    return render_template('iniciarsesion.html')

@app.route('/tareas')
def tareas():
    return render_template('tareas.html')

if __name__ == '__main__':
    app.run(debug=True)