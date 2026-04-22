from flask import Flask, render_template
import gestor

gestor = gestor.GestorTareas()

app = Flask(__name__)
app.secret_key = 'gatitolula'

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/iniciasesion', methods=['GET', 'POST'])
def iniciasesion():
    return render_template('iniciarsesion.html')


@app.route('/creacuenta', methods=['GET', 'POST'])
def creacuenta():
    return render_template('crearcuenta.html')

@app.route('/tareas')
def tareas():
    return render_template('tareas.html')

if __name__ == '__main__':
    app.run(debug=True)