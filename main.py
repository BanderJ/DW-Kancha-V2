from flask import Flask,render_template,request,jsonify, redirect
import controlador_productos 
import controlador_nivelusuario
import controlador_categoria
from bd import conectarse

app = Flask(__name__)

# Enlaces html/templates
@app.route("/")
@app.get('/Inicio')
def inicio():
    return render_template("index.html")

@app.get('/productos')
def seccionProductos():
    return render_template("SeccionProductos.html")

@app.route('/kancha-club')
def kancha_club():
    return render_template('KanchaClub.html')

@app.route('/soporte')
def soporteTecnico():
    return render_template("SoporteTecnico.html")

@app.route("/VentanaPago")
def ventanaPago():
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

@app.route('/Registrate')
def registrarUsuario():
    return render_template('RegistroUsuario.html')

from flask import Flask, request, jsonify
# Asumiendo que ya tienes conexión con la base de datos

@app.route("/validarSesion", methods=["POST"])
def validarInicioSesion():
    correo = request.form["correo"]
    contraseña = request.form["clave"]

    # Imprimir solo si es necesario para depuración
    print(f"Correo: {correo}")
    print(f"Contraseña: {contraseña}")
    
    try:
        cursor = conectarse().cursor()
        cursor.execute("SELECT correo,password FROM usuario WHERE correo=%s and password=%s", (correo,contraseña))
        registro = cursor.fetchone()

        if registro[0]==registro[0] and registro[1] == contraseña:  # Asegúrate de que el índice sea correcto
            return jsonify({"message": "Logeado exitosamente", "status": "success"})
        else:
            return jsonify({"message": "Correo o contraseña incorrectos", "status": "error"})
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"})

        

# ------------------------------------------------------------------------------------------------------------------------------------------
# Controladores
# Nivel de Usuario
@app.route('/NivelUsuario')
def nivelusuario():
    lista = controlador_nivelusuario.obtener_nivelusuario()
    return render_template('nivelusuario.html',lista=lista)

@app.route('/AgregarNivelUsuario')
def formulario_agregar_nivelUsuario():
    return render_template('agregar_nivelusuario.html')

@app.route("/guardar_nivelusuario", methods=["POST"])
def guardar_nivelusuario():
    nombre = request.form["nombre"]
    puntos = request.form["puntos"]
    controlador_nivelusuario.insertar_nivelUsuario(nombre, puntos)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/NivelUsuario")

@app.route("/eliminar_nivelUsuario", methods=["POST"])
def eliminar_nivelUsuario():
    controlador_nivelusuario.eliminar_nivelUsuario(request.form["id"])
    return redirect("/NivelUsuario")

@app.route("/formulario_editar_nivelUsuario/<int:id>")
def formulario_editar_nivelusuario(id):
    # Obtener el disco por ID
    nivel = controlador_nivelusuario.obtener_nivelusuario_por_id(id)
    return render_template("editar_nivelUsuario.html", disco=nivel)


@app.route("/actualizar_nivelUsuario", methods=["POST"])
def actualizar_nivelusuario():
    id = request.form["id"]
    nombre = request.form["nombre"]
    puntos = request.form["puntos"]
    controlador_nivelusuario.actualizar_nivelusuario(nombre, puntos, id)
    return redirect("/NivelUsuario")

# Categorias
@app.route('/Categoria')
def categoria():
    lista = controlador_categoria.obtener_categorias()
    return render_template('categoria.html',lista=lista)


@app.route('/AgregarCategoria')
def formulario_agregar_categoria():
    return render_template('agregar_categoria.html')

@app.route("/guardar_categoria", methods=["POST"])
def guardar_categoria():
    nombre = request.form["nombre"]
    controlador_categoria.insertar_Categoria(nombre)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/Categoria")

@app.route("/eliminar_categoria", methods=["POST"])
def eliminar_categoria():
    controlador_categoria.eliminar_categoria(request.form["id"])
    return redirect("/Categoria")

@app.route("/formulario_editar_categoria/<int:id>")
def formulario_editar_categoria(id):
    # Obtener el disco por ID
    categoria = controlador_categoria.obtener_categoria_por_id(id)
    return render_template("editar_categoria.html", categoria=categoria)


@app.route("/actualizar_categoria", methods=["POST"])
def actualizar_categoria():
    id = request.form["id"]
    nombre = request.form["nombre"]
    controlador_categoria.actualizar_categoria(nombre, id)
    return redirect("/Categoria")

if __name__ == "__main__":
    app.run(debug=True)