from flask import Flask,render_template,request,jsonify, redirect
import controlador_productos 
import controlador_nivelusuario
import controlador_categoria
import controlador_productos
from bd import conectarse
from flask import session
#Para generar claves en hash aleatorias
import hashlib
import os

def crearHashSecret():
    datos_aleatorios = os.urandom(16)
    hash_objeto = hashlib.sha256(datos_aleatorios)
    return hash_objeto.hexdigest()

app = Flask(__name__)
app.secret_key = crearHashSecret()

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

@app.route('/Registrate')
def registrarUsuario():
    return render_template('RegistroUsuario.html')

@app.route("/perfil")
def mostrarPerfil():
    datos = session.get("usuario", {"nombre":"Invitado","apellidos":"Invitado","correo":"example@email.com","numdoc":"11111111"})
    return render_template("MiPerfil.html", userData=datos)

@app.route("/favoritos")
def mostrarFavoritos():
    return render_template("MisFavoritos.html")
    
@app.route('/login', methods=["POST"])
def validarInicioSesion():
    datosUsuario = dict()
    try:
        email = request.form["correo"]
        contraseña = request.form["clave"]
        print(email)
        print(contraseña)
        
        cursor = conectarse().cursor()
        cursor.execute("SELECT nombre, apePat, apeMat, correo, numdoc FROM usuario WHERE correo=%s AND password=%s", (email, contraseña,))
        registro = cursor.fetchone()

        if registro:  # Verificar si se encontró un registro
            datosUsuario["nombre"] = registro[0]
            datosUsuario["apellidos"] = f"{registro[1]} {registro[2]}"
            datosUsuario["correo"] = registro[3]
            datosUsuario["numdoc"] = registro[4]
            datosUsuario["mensaje"] = "Usuario logueado exitosamente"
            datosUsuario["status"] = 1
            session["usuario"] = datosUsuario
            
            return redirect('/')  # Redirigir a la ruta del perfil
        else:
            datosUsuario["mensaje"] = "Usuario no logueado"
            datosUsuario["error"] = "Credenciales incorrectas"
            datosUsuario["status"] = -1
            return jsonify(datosUsuario)

    except Exception as e:
        datosUsuario["mensaje"] = "Ha ocurrido un error"
        datosUsuario["error"] = f"Ha ocurrido un error => {repr(e)}"
        datosUsuario["status"] = -1
        return jsonify(datosUsuario)

@app.route('/EventosDeportivos')
def redirigirEventosDeportivos():
    return render_template('EventosDeportivos.html')

@app.route('/Pago')
def redirigirPago():
    return render_template('Pago(1).html')

@app.route('/MisPedidos')
def redirigirPedidos():
    return render_template('MisPedidos.html')

@app.route('/NikeMercurial')
def NikeMercurial():
    return render_template('NikeMercurial2.html')

@app.route('/dashboard')
def dash():
    return render_template('maestradashboard.html')
    
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

@app.route("/formulario_productos")
def formulario_producto():
    productos = controlador_productos.obtener_productos()
    return render_template("Mantproducto.html", productos=productos)

@app.route("/agregar_producto")
def formulario_agregar_producto():
    modelos = controlador_productos.obtener_modelos()  # Obtenemos los modelos
    tallas = controlador_productos.obtener_tallas()    # Obtenemos las tallas
    return render_template("agregar_producto.html", modelos=modelos, tallas=tallas)

@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    idModelo = request.form["idModelo"]
    idTalla = request.form["idTalla"]
    controlador_productos.insertar_producto(nombre, precio, stock, idModelo, idTalla)
    return redirect("/formulario_productos")

@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    controlador_productos.eliminar_producto(request.form["id"])
    return redirect("/formulario_productos")

@app.route("/editar_producto/<int:id>")
def editar_producto(id):
    producto = controlador_productos.obtener_producto_por_id(id)
    modelos = controlador_productos.obtener_modelos()  # Obtenemos los modelos
    tallas = controlador_productos.obtener_tallas()    # Obtenemos las tallas
    return render_template("editar_producto.html", producto=producto, modelos=modelos, tallas=tallas)

@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():
    id = request.form["id"]
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    idModelo = request.form["idModelo"]
    idTalla = request.form["idTalla"]
    controlador_productos.actualizar_producto(nombre, precio, stock, idModelo, idTalla, id)
    return redirect("/formulario_productos")


if __name__ == "__main__":
    app.run(debug=True)