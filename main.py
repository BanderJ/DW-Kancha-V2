from flask import Flask,render_template,request,jsonify, redirect, flash
import controlador_usuario
import controlador_productos 
import controlador_nivelusuario
import controlador_categoria
import controlador_marca
import controlador_modelo
import controlador_productos
from bd import conectarse
from flask import session
#Para generar claves en hash aleatoriassssss
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
    productos = controlador_productos.obtener_productos()
    return render_template("index.html", productos =productos)

def listadoProductos():
    try:
        cursor = conectarse().cursor()
        cursor.execute("select nombre,precio from producto")
        registros = cursor.fetchall()
        print(registros)

        return registros
    except Exception as e:
        return []

@app.get('/productos')
def seccionProductos():
    productos = controlador_productos.obtener_productos()
    generos = controlador_productos.obtener_generos()
    categorias = controlador_productos.obtener_categorias()
    colores = controlador_productos.obtener_colores()
    marcas = controlador_marca.obtener_marcas()
    return render_template("SeccionProductos.html",productos=productos,generos=generos,categorias=categorias,colores=colores,marcas=marcas)


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

@app.route('/SobreNosotros')
def redirigirSobreNosotros():
    return render_template('SobreNosotros.html')

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

# Marcas
@app.route('/Marca')
def marca():
    lista = controlador_marca.obtener_marcas()
    return render_template('MantMarca.html', lista=lista)

@app.route('/AgregarMarca')
def formulario_agregar_marca():
    return render_template('agregar_marca.html')

@app.route("/guardar_marca", methods=["POST"])
def guardar_marca():
    nombre = request.form["nombre"]
    controlador_marca.insertar_marca(nombre)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/Marca")

@app.route("/eliminar_marca", methods=["POST"])
def eliminar_marca():
    controlador_marca.eliminar_marca(request.form["id"])
    return redirect("/Marca")

@app.route("/formulario_editar_marca/<int:id>")
def formulario_editar_marca(id):
    # Obtener la marca por ID
    marca = controlador_marca.obtener_marca_por_id(id)
    return render_template("editar_marca.html", marca=marca)

@app.route("/actualizar_marca", methods=["POST"])
def actualizar_marca():
    id = request.form["id"]
    nombre = request.form["nombre"]
    controlador_marca.actualizar_marca(nombre, id)
    return redirect("/Marca")

# Modelos
@app.route('/Modelo')
def modelo():
    lista = controlador_modelo.obtener_modelos()
    return render_template('MantModelo.html', lista=lista)

@app.route('/AgregarModelo')
def formulario_agregar_modelo():
    marcas = controlador_marca.obtener_marcas()  # Obtener la lista de marcas para el formulario
    return render_template('agregar_modelo.html', marcas=marcas)

@app.route("/guardar_modelo", methods=["POST"])
def guardar_modelo():
    nombre = request.form["nombre"]
    idMarca = request.form["idMarca"]  # Asegúrate de que este campo está en el formulario
    controlador_modelo.insertar_modelo(nombre, idMarca)
    return redirect("/Modelo")

@app.route("/eliminar_modelo", methods=["POST"])
def eliminar_modelo():
    controlador_modelo.eliminar_modelo(request.form["id"])
    return redirect("/Modelo")

@app.route("/formulario_editar_modelo/<int:id>")
def formulario_editar_modelo(id):
    modelo = controlador_modelo.obtener_modelo_por_id(id)
    marcas = controlador_marca.obtener_marcas()  # Obtener la lista de marcas para el formulario
    return render_template("editar_modelo.html", modelo=modelo, marcas=marcas)

@app.route("/actualizar_modelo", methods=["POST"])
def actualizar_modelo():
    id = request.form["id"]
    nombre = request.form["nombre"]
    idMarca = request.form["idMarca"]  # Asegúrate de que este campo está en el formulario
    controlador_modelo.actualizar_modelo(nombre, idMarca, id)
    return redirect("/Modelo")


@app.route('/Contactanos')
def contactanos():
    return render_template("Contactanos.html")

@app.route('/Usuario')
def usuario():
    lista = controlador_usuario.obtener_usuario()
    return render_template('MantUsuario.html',lista=lista)

@app.route('/AgregarUsuario')
def formulario_agregar_usuario():
    niveles_usuario = controlador_nivelusuario.obtener_nivelusuario()
    return render_template('agregar_usuario.html', niveles_usuario = niveles_usuario)

@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    nombre = request.form["nombre"]
    nroDoc = request.form["numerodocumento"]
    apePat = request.form["apePat"]
    apeMat = request.form["apeMat"]
    correo = request.form["correo"]
    password = request.form["password"]
    tipoUsu = 1
    nivelUsu = request.form["nivel_usuario"]
    controlador_usuario.insertar_usuario(tipoUsu, nombre, nroDoc, apePat, apeMat, correo, password, controlador_nivelusuario.obtener_nivelusuario_por_nombre(nivelUsu)[0])
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/Usuario")

@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    controlador_usuario.eliminar_usuario(request.form["id"])
    return redirect("/Usuario")

@app.route("/formulario_editar_Usuario/<int:id>")
def formulario_editar_usuario(id):
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    niveles_usuario = controlador_nivelusuario.obtener_nivelusuario()
    return render_template("editar_Usuario.html", usuario=usuario, niveles_usuario = niveles_usuario)

@app.route("/actualizar_usuario", methods=["POST"])
def actualizar_usuario():
    id = request.form["id"]
    nombre = request.form["nombre"]
    nroDoc = request.form["numerodocumento"]
    apePat = request.form["apePat"]
    apeMat = request.form["apeMat"]
    correo = request.form["correo"]
    password = request.form["password"]
    tipoUsu = 1
    nivelUsu = request.form["nivel_usuario"]
    controlador_usuario.actualizar_usuario(tipoUsu, nombre, nroDoc, apePat, apeMat, correo, password, controlador_nivelusuario.obtener_nivelusuario_por_nombre(nivelUsu)[0], id)
    return redirect("/Usuario")

# PARTE RELACIONADA AL PRODUCTO:

app.secret_key = "super_secret_key"

# Mostrar productos
@app.route("/formulario_productos")
def formulario_producto():
    productos = controlador_productos.obtener_productos()
    return render_template("MantProducto.html", productos=productos)

# Formulario para agregar productos
@app.route("/agregar_producto")
def formulario_agregar_producto():
    generos = controlador_productos.obtener_generos()
    tipos = controlador_productos.obtener_tipos()
    modelos = controlador_productos.obtener_modelos()
    tallas = controlador_productos.obtener_tallas()
    colores = controlador_productos.obtener_colores()
    categorias = controlador_productos.obtener_categorias()
    
    generos = controlador_productos.obtener_generos()
    tipos = controlador_productos.obtener_tipos()
    return render_template("agregar_producto.html", modelos=modelos, tallas=tallas, colores=colores, categorias=categorias,generos=generos,tipos=tipos)

# Guardar producto nuevo
@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    precio = request.form["precio"]
    stock = request.form["stock"]
    idModelo = request.form["idModelo"]
    idTalla = request.form["idTalla"]
    genero = request.form["idGenero"]
    tipo_producto = request.form["idTipo"]
    descripcion = request.form["descripcion"]
    imagenPrincipal = request.files["imagenPrincipal"]
    imagenesSecundarias = request.files.getlist("imagenesSecundarias")
    colores = request.form.getlist("colores")
    categorias = request.form.getlist("categorias")

    controlador_productos.insertar_producto(precio, stock, idModelo, idTalla, genero, tipo_producto, imagenPrincipal, imagenesSecundarias, colores, categorias,descripcion)
    flash("Producto agregado exitosamente.")
    return redirect("/formulario_productos")

# Eliminar producto
@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    controlador_productos.eliminar_producto(request.form["id"])
    flash("Producto eliminado.")
    return redirect("/formulario_productos")

# Editar producto
@app.route("/editar_producto/<int:id>")
def editar_producto(id):
    producto = controlador_productos.obtener_producto_por_id(id)
    modelos = controlador_productos.obtener_modelos()
    tallas = controlador_productos.obtener_tallas()
    colores = controlador_productos.obtener_colores()
    categorias = controlador_productos.obtener_categorias()
    generos = controlador_productos.obtener_generos()
    tipos = controlador_productos.obtener_tipos()
    return render_template("editar_producto.html", producto=producto, modelos=modelos, tallas=tallas,colores=colores, categorias=categorias,generos=generos,tipos=tipos)

# Actualizar producto
@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():
    id = request.form["id"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    idModelo = request.form["idModelo"]
    idTalla = request.form["idTalla"]
    genero = request.form["idGenero"]
    tipo_producto = request.form["idTipo"]

    descripcion = request.form["descripcion"]
    imagenPrincipal = request.files["imagenPrincipal"]
    imagenesSecundarias = request.files.getlist("imagenesSecundarias")
    colores = request.form.getlist("colores")
    categorias = request.form.getlist("categorias")

    controlador_productos.actualizar_producto(id, precio, stock, idModelo, idTalla, genero, tipo_producto, imagenPrincipal, imagenesSecundarias, colores, categorias, descripcion)
    flash("Producto actualizado.")
    return redirect("/formulario_productos")

@app.route("/producto/<int:id>")
def detalle_producto(id):
    # Obtener el disco por ID
    producto = controlador_productos.obtener_producto_por_id(id)
    return render_template("detalle_producto.html", producto=producto)

if __name__ == "__main__":
    app.run(debug=True)
