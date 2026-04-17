from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/iniciasesion')
def iniciasesion():
    return render_template('iniciarsesion.html') 

@app.route('/creacuenta')
def creacuenta():
    return render_template('crearcuenta.html')

@app.route('/tareas')
def tareas():
    return render_template('tareas.html')

if __name__ == '__main__':
    app.run(debug=True)