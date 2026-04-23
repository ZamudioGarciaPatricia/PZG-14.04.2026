from flask import Flask, render_template, request, redirect, url_for, flash
import gestor

# Inicializamos el gestor
gestor_obj = gestor.GestorTareas()

app = Flask(__name__)
app.secret_key = 'gatitolula'

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/iniciasesion', methods=['GET', 'POST'])
def iniciasesion():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')
        
        if gestor_obj.validar_usuario(usuario, contraseña):
            return redirect(url_for('tareas'))
        else:
            flash('Usuario o contraseña incorrectos')
            
    return render_template('iniciarsesion.html')

@app.route('/creacuenta', methods=['GET', 'POST'])
def creacuenta():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        gestor_obj.crear_usuario(usuario, email, contraseña)
        flash('Cuenta creada con éxito. ¡Inicia sesión!')
        return redirect(url_for('iniciasesion'))
        
    return render_template('crearcuenta.html')


@app.route('/tareas')
def tareas():
    return render_template('tareas.html')

if __name__ == '__main__':
    app.run(debug=True)