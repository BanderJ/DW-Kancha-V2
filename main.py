from flask import Flask,render_template,request,jsonify
from controlador_productos import insertProduct,listarProductos,updateProducto,deleteProducto

app = Flask(__name__)

@app.get('/')
def inicio():
    return render_template("index.html")

@app.get('/productos')
def seccionProductos():
    return render_template("SeccionProductos.html")

@app.route('/kancha-club')
def kancha_club():
    return render_template('KanchaClub.html')

@app.route('/index')
def redirigir_index():
    return render_template('index.html')

@app.route('/soporte')
def soporteTecnico():
    return render_template("SoporteTecnico.html")

@app.route("/VentanaPago")
def ventatnaPago():
    return render_template("VentanaPago(SinIniciarSesion).html")

@app.route("/IniciarSesion")
def iniciarSesion():
    return render_template("IniciarSesion.html")

@app.route('/EventosDeportivos')
def redirigirEventosDeportivos():
    return render_template('EventosDeportivos.html')

@app.route('/Pago')
def redirigirPago():
    return render_template('Pago(1).html')

@app.route('/MisPedidos')
def redirigirPedidos():
    return render_template('MisPedidos.html')


if __name__ == "__main__":
    app.run(debug=True)