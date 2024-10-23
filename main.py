from flask import Flask,render_template,request,jsonify, redirect, flash, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
import controlador_usuario
import controlador_productos 
import controlador_nivelusuario
import controlador_categoria
import controlador_marca
import controlador_modelo
import controlador_productos
import controlador_carrito
import controlador_ubicacion
from bd import conectarse
#Para generar claves en hash aleatoriassssss
import hashlib
import os
import controlador_favoritos
import datetime
import controlador_carrito
import controlador_ubicacion
from datetime import datetime

def crearHashSecret():
    datos_aleatorios = os.urandom(16) 
    hash_objeto = hashlib.sha256(datos_aleatorios)
    return hash_objeto.hexdigest()

app = Flask(__name__)
app.secret_key = crearHashSecret()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dawa_kancha'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bdsita = SQLAlchemy(app)

# Definir la clase Usuario basada en la tabla de tu base de datos
class Usuario(bdsita.Model):
    __tablename__ = 'usuarios'  # Asegúrate de que este nombre coincida con el de tu tabla en MySQL

    idUsuario = bdsita.Column(bdsita.Integer, primary_key=True)
    idTipoUsuario = bdsita.Column(bdsita.Integer, default=1)
    nombre = bdsita.Column(bdsita.String(100), nullable=False)
    numDoc = bdsita.Column(bdsita.String(20), nullable=False)
    apePat = bdsita.Column(bdsita.String(50), nullable=False)
    apeMat = bdsita.Column(bdsita.String(50), nullable=False)
    correo = bdsita.Column(bdsita.String(100), nullable=False, unique=True)
    password = bdsita.Column(bdsita.String(200), nullable=False)
    telefono = bdsita.Column(bdsita.String(20))
    fechaNacimiento = bdsita.Column(bdsita.Date)
    sexo = bdsita.Column(bdsita.String(1), nullable=False)  # 'F', 'M' o 'N'
    idNivelUsuario = bdsita.Column(bdsita.Integer, default=1)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='TU_CLIENT_ID',
    client_secret='TU_CLIENT_SECRET',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
)

# Ruta para iniciar el proceso de login con Google
@app.route('/loginGoogle')
def loginGoogle():
    redirect_uri = url_for('authorizeGoogle', _external=True)
    return google.authorize_redirect(redirect_uri)

# Ruta de autorización de Google, donde obtenemos el token y la información del usuario
@app.route('/authorizeGoogle')
def authorizeGoogle():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()

    # Extraer la información relevante del usuario autenticado por Google
    nombre = user_info.get('given_name', '')
    apePat = user_info.get('family_name', '')
    correo = user_info.get('email', '')
    
    # Valores predeterminados
    idTipoUsuario = 1
    idNivelUsuario = 1
    password = ''  # No tenemos password de Google, se puede manejar con OAuth tokens
    numDoc = ''
    apeMat = ''
    telefono = ''
    fechaNacimiento = datetime.date(1900, 1, 1)  # Ajusta si obtienes este dato de otra forma
    sexo = 'N'  # Dato no especificado

    # Crear el nuevo usuario en la base de datos
    nuevo_usuario = Usuario(
        idTipoUsuario=idTipoUsuario,
        nombre=nombre,
        numDoc=numDoc,
        apePat=apePat,
        apeMat=apeMat,
        correo=correo,
        password=password,
        telefono=telefono,
        fechaNacimiento=fechaNacimiento,
        sexo=sexo,
        idNivelUsuario=idNivelUsuario
    )

    # Insertar en la base de datos
    bdsita.session.add(nuevo_usuario)
    bdsita.session.commit()

    # Redirigir a la ruta raíz
    return redirect(url_for('inicio'))

# Enlaces html/templates
@app.route("/")
@app.route("/Inicio")
def inicio():
    productos = controlador_productos.obtener_productos()
    # Pasa valores predeterminados para evitar errores en las plantillas que dependen de estas variables
    return render_template(
        "index.html", 
        productos=productos
    )

def listadoProductos():
    try:
        cursor = bdsita().cursor()
        cursor.execute("select nombre,precio from producto")
        registros = cursor.fetchall()
        print(registros)

        return registros
    except Exception as e:
        return []

# @app.get('/productos')
# def seccionProductos():
#     idUsuario = session.get("usuario", {}).get("idUsuario", None)
#     productos = controlador_productos.obtener_productos()
#     generos = controlador_productos.obtener_generos()
#     categorias = controlador_productos.obtener_categorias()
#     colores = controlador_productos.obtener_colores()
#     marcas = controlador_marca.obtener_marcas()
#     if idUsuario is None 
#     favoritos = controlador_favoritos.obtener_favoritos(idUsuario)
#     ids_favoritos = {fav[0] for fav in favoritos}
#     return render_template("SeccionProductos.html",productos=productos,generos=generos,categorias=categorias,colores=colores,marcas=marcas, favoritos = ids_favoritos)

@app.get('/productos')
def seccionProductos():
    idUsuario = session.get("usuario", {}).get("idUsuario", None)
    
    productos = controlador_productos.obtener_productos()
    generos = controlador_productos.obtener_generos()
    categorias = controlador_productos.obtener_categorias()
    colores = controlador_productos.obtener_colores()
    marcas = controlador_marca.obtener_marcas()

    if idUsuario is None:
        return render_template("SeccionProductos.html", productos=productos,generos=generos,categorias=categorias,colores=colores,marcas=marcas)
    else:
        favoritos = controlador_favoritos.obtener_favoritos(idUsuario)
        ids_favoritos = {fav[0] for fav in favoritos}
        return render_template("SeccionProductos.html", productos=productos,generos=generos,categorias=categorias,colores=colores,marcas=marcas, favoritos=ids_favoritos)

@app.route('/favoritos')
def mostrarFavoritos():
 
    idUsuario = session.get("usuario", {}).get("idUsuario", None)
    
    if idUsuario is None:
        return redirect('/IniciarSesion')  
    
    favoritos = controlador_favoritos.obtener_favoritos(idUsuario)
    return render_template("MisFavoritos.html", favoritos=favoritos, idUsuario = idUsuario)

@app.route('/agregar_favorito', methods=['POST'])
def agregar_favorito():
    idUsuario = session.get("usuario", {}).get("idUsuario", None)
    data = request.get_json()
    idCliente = idUsuario
    idProducto = data['idProducto']
    controlador_favoritos.insertar_favoritos(idCliente, idProducto)
    return jsonify({'message': 'Producto agregado a favoritos'})

@app.route('/eliminar_favorito', methods=['POST'])
def eliminar_favorito():
    idUsuario = session.get("usuario", {}).get("idUsuario", None)
    data = request.get_json()
    idCliente = idUsuario
    idProducto = data['idProducto']
    controlador_favoritos.eliminar_favoritos(idCliente, idProducto)
    return jsonify({'message': 'Producto eliminado de favoritos'})

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
    datos = session.get("usuario", {"nombre":"Invitado","apellidos":"Invitado"})
    if datos["nombre"] != "Invitado":
        # Solo formatear la fecha si hay sesión del usuario
        fecha_nac = datetime.strptime(datos["fechaNac"], "%a, %d %b %Y %H:%M:%S %Z")
        formato_fecha = fecha_nac.strftime("%d/%m/%Y")
        return render_template("MiPerfil.html", userData=datos,nacimiento=formato_fecha)
    else:
        return redirect("/IniciarSesion")
    
@app.route('/login', methods=["POST"])  
def validarInicioSesion():
    datosUsuario = dict()
    try:
        email = request.form["correo"]
        contraseña = request.form["clave"]
        print(email)
        print(contraseña)
        
        cursor = conectarse().cursor()
        cursor.execute("SELECT idUsuario, nombre, apePat, apeMat, correo, numdoc,fechaNacimiento,sexo,telefono FROM usuario WHERE correo=%s AND password=%s", (email, contraseña,))
        registro = cursor.fetchone()


        if registro:  # Verificar si se encontró un registro
            datosUsuario["idUsuario"] = registro[0]
            datosUsuario["nombre"] = registro[1]
            datosUsuario["apellidos"] = f"{registro[2]} {registro[3]}"
            datosUsuario["correo"] = registro[4]
            datosUsuario["numdoc"] = registro[5]
            datosUsuario["fechaNac"]=registro[6]
            datosUsuario["sexo"]=registro[7]
            datosUsuario["telefono"]=registro[8]
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
    
@app.route('/logout')
def cerrarSesion():
    # Eliminar la sesión actual
    session.pop('usuario', None)  # Elimina el usuario de la sesión
    return redirect('/IniciarSesion')

@app.route('/EventosDeportivos')
def redirigirEventosDeportivos():
    return render_template('EventosDeportivos.html')

@app.route('/SobreNosotros')
def redirigirSobreNosotros():
    return render_template('SobreNosotros.html')

@app.route('/Pago')
def redirigirPago():
    id_usuario=session.get("usuario", {}).get("idUsuario", None)
    carritoid= controlador_carrito.obtener_id_carrito(id_usuario)
    lista= controlador_carrito.obtener_detalles_carrito(id_usuario)
    total= controlador_carrito.obtener_total_carrito(id_usuario)
    departamentos=controlador_ubicacion.obtener_departamentos()
    return render_template('Pago(1).html', lista=lista, total=total, id_carrito=carritoid, departamentos=departamentos)

@app.route('/MisPedidos')
def redirigirPedidos():
    idUsuario = session.get("usuario", {}).get("idUsuario", None)
    if idUsuario is None:
        return redirect('/IniciarSesion')
    ventas=controlador_carrito.obtener_ventas_y_detalles(idUsuario)
    return render_template('MisPedidos.html', ventas=ventas)

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
    imagen = request.files.get("imagen")  # Asegúrate de que tu formulario tenga un campo para la imagen

    # Verifica si se subió una imagen
    if imagen:
        controlador_marca.insertar_marca(nombre, imagen)  # Pasa la imagen a la función
        flash(f'Marca "{nombre}" registrada correctamente.', 'success')
    else:
        flash('No se pudo registrar la marca porque no se subió una imagen.', 'error')

    return redirect("/Marca")

@app.route("/eliminar_marca", methods=["POST"])
def eliminar_marca():
    id_marca = request.form["id"]
    marca = controlador_marca.obtener_marca_por_id(id_marca)
    nombre_marca = marca[1] if marca else "Marca desconocida"
    exito = controlador_marca.eliminar_marca(id_marca)
    
    if not exito:
        flash(f'La marca "{nombre_marca}" no se puede ser eliminada. Ya existen productos asociados', 'success')
    else:
        flash(f'Marca "{nombre_marca}" eliminada correctamente.', 'success')

    return redirect("/Marca")

@app.route("/formulario_editar_marca/<int:id>")
def formulario_editar_marca(id):
    marca = controlador_marca.obtener_marca_por_id(id)
    return render_template("editar_marca.html", marca=marca)

@app.route("/actualizar_marca", methods=["POST"])
def actualizar_marca():
    id = request.form["id"]
    nombre = request.form["nombre"]
    imagen = request.files.get("imagen")  # Asegúrate de que tu formulario tenga un campo para la imagen
    controlador_marca.actualizar_marca(nombre, imagen, id)
    flash(f'Marca "{nombre}" actualizada correctamente.', 'success')
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
    usuario = session.get("usuario", None)

    producto = controlador_productos.obtener_producto_por_id(id)

    if usuario is None:
        return render_template("detalle_producto.html", producto=producto)

    idUsuario = usuario.get("idUsuario")
    favoritos = controlador_favoritos.obtener_favoritos(idUsuario)
    ids_favoritos = {fav[0] for fav in favoritos}  

    return render_template(
        "detalle_producto.html", 
        producto=producto, 
        favoritos=ids_favoritos, 
        usuario=usuario
    )



# @app.route('/producto/<int:id>')
# def detalle_producto(id):
#     # Obtener el disco por ID
#     producto = controlador_productos.obtener_producto_por_id(id)
#     return render_template("detalle_producto.html", producto=producto)


@app.route('/anadir_carrito', methods=['POST'])
def anadir_carrito():
    # Obtener los datos del formulario

    id_producto = request.form.get('id_producto')
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    id_usuario = session.get("usuario", {}).get("idUsuario", None)
    controlador_carrito.insertar_detalle_venta(id_usuario, id_producto, cantidad, precio)
    producto = controlador_productos.obtener_producto_por_id(id_producto)
    return redirect(f'/producto/{id_producto}?')


@app.route('/carrito')
def mostrar_carrito():
    idUsuario = session.get("usuario", {}).get("idUsuario", None)
    
    if idUsuario is None:
        return redirect('/IniciarSesion')  
    detalles_carrito= controlador_carrito.obtener_detalles_carrito(idUsuario);
    return render_template("carro.html", lista=detalles_carrito)

@app.route('/eliminar_detalle_venta', methods=['POST'])
def eliminar_detalle_venta():
    id_det_vta = request.form.get('id_det_vta')
    id_producto = request.form.get('id_producto')
    id_carrito = request.form.get('id_carrito')
    id_usuario = session.get("usuario", {}).get("idUsuario", None)

    # Llamar a la función para eliminar el detalle de venta
    controlador_carrito.eliminar_detalle_venta_bd(id_det_vta, id_producto, id_carrito, id_usuario)

    # Redirigir nuevamente a la página del carrito
    return redirect(url_for('mostrar_carrito'))

@app.route('/actualizar_cantidad_mas', methods=['POST'])
def actualizar_cantidad_mas():
    id_det_vta = request.form.get('id_det_vta')
    id_producto = request.form.get('id_producto')
    id_carrito = request.form.get('id_carrito')
    id_usuario = session.get("usuario", {}).get("idUsuario", None)

    resultado = controlador_carrito.incrementarcantidad(id_det_vta, id_producto, id_carrito, id_usuario)

    if "error" in resultado:
        return jsonify({"error": resultado["error"]}), 400
    else:
        return jsonify({
            "nueva_cantidad": resultado["nueva_cantidad"],
            "nuevo_subtotal": resultado["nuevo_subtotal"]
        }), 200

@app.route('/actualizar_cantidad_menos', methods=['POST'])
def actualizar_cantidad_menos():
    id_det_vta = request.form.get('id_det_vta')
    id_producto = request.form.get('id_producto')
    id_carrito = request.form.get('id_carrito')
    id_usuario = session.get("usuario", {}).get("idUsuario", None)

    resultado = controlador_carrito.disminuircantidad(id_det_vta, id_producto, id_carrito, id_usuario)

    if "error" in resultado:
        return jsonify({"error": resultado["error"]}), 400
    else:
        return jsonify({
            "nueva_cantidad": resultado["nueva_cantidad"],
            "nuevo_subtotal": resultado["nuevo_subtotal"]
        }), 200

@app.route('/actualizar_cantidad', methods=['POST'])
def actualizar_cantidad():
    id_producto = request.form.get('id_producto')
    id_carrito = request.form.get('id_carrito')
    accion = request.form.get('accion')  # 'mas' o 'menos'

    # Lógica para obtener la cantidad actual y stock disponible
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Obtener la cantidad actual del detalle de venta
            cursor.execute("SELECT cantidad FROM detalle_venta WHERE idProducto = %s AND idCarrito = %s", (id_producto, id_carrito))
            cantidad_actual = cursor.fetchone()[0]

            # Obtener el stock disponible del producto
            cursor.execute("SELECT stock FROM producto WHERE idProducto = %s", (id_producto,))
            stock_disponible = cursor.fetchone()[0]

            # Verificar la acción
            if accion == 'mas':
                if cantidad_actual < stock_disponible:
                    nueva_cantidad = cantidad_actual + 1
                else:
                    return jsonify({'error': 'No se puede agregar más. Stock insuficiente.'}), 400
            elif accion == 'menos':
                if cantidad_actual > 1:
                    nueva_cantidad = cantidad_actual - 1
                else:
                    return jsonify({'error': 'La cantidad mínima es 1.'}), 400
            else:
                return jsonify({'error': 'Acción no válida.'}), 400

            # Actualizar la cantidad en la base de datos
            cursor.execute("""
                UPDATE detalle_venta 
                SET cantidad = %s 
                WHERE idProducto = %s AND idCarrito = %s
            """, (nueva_cantidad, id_producto, id_carrito))

            # Recalcular el subtotal del carrito
            cursor.execute("CALL actualizar_subtotal_carrito(%s)", (id_carrito,))
            conexion.commit()

            # Devolver la nueva cantidad y el precio del producto para actualizar el frontend
            cursor.execute("SELECT precio FROM producto WHERE idProducto = %s", (id_producto,))
            precio_unitario = cursor.fetchone()[0]

            return jsonify({
                'nueva_cantidad': nueva_cantidad,
                'precio_unitario': precio_unitario
            })

    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        conexion.close()


@app.route('/finalizarcompra', methods=['POST'])
def finalizarCompra():
    # Obtener los datos enviados desde el frontend
    id_carrito = request.form['id_carrito']
    id_ciudad = request.form['id_distrito']
    direccion = request.form['direcc']
    id_usuario = session.get("usuario", {}).get("idUsuario", None)
    # Llamar a la función incrementarcantidad para actualizar en la base de datos
    try:
        controlador_carrito.finalizarCompra_bd(id_carrito, id_ciudad, direccion, id_usuario)
        return redirect(url_for('resumenCompra'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/resumen_compra')
def resumenCompra():
    # Verificar si el usuario está autenticado
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for('login'))  # Redirigir al login si no hay sesión activa

    id_usuario = usuario.get("idUsuario")

    try:
        # Conectar con la base de datos y ejecutar la consulta
        db = conectarse()
        cursor = db.cursor()

        query = """
        SELECT cr.idCarrito, usu.idUsuario, pr.idProducto, usu.nombre, usu.numDoc, 
               vt.direccion, vt.fecha, cr.descuento, cr.subtotal
        FROM carrito cr
        INNER JOIN usuario usu ON cr.idUsuario = usu.idUsuario
        INNER JOIN detalle_venta dv ON cr.idCarrito = dv.idCarrito
        INNER JOIN producto pr ON dv.idProducto = pr.idProducto
        INNER JOIN venta vt ON cr.idCarrito = vt.idCarrito
        WHERE cr.idUsuario = %s;
        """

        cursor.execute(query, (id_usuario,))
        productos = cursor.fetchall()

        # Calcular el total de la compra con el subtotal y descuento
        total_compra = sum(producto[8] for producto in productos)  # Índice 8 es el subtotal

        # Formatear los productos para pasarlos a la plantilla
        productos_format = [
            {
                'idCarrito': producto[0],
                'idUsuario': producto[1],
                'idProducto': producto[2],
                'nombre_usuario': producto[3],
                'numDoc': producto[4],
                'direccion': producto[5],
                'fecha': producto[6],
                'descuento': producto[7],
                'subtotal': producto[8],
            }
            for producto in productos
        ]

        return render_template(
            'resumen_compra.html',
            usuario=usuario,
            productos=productos_format,
            total_compra=total_compra
        )

    except Exception as e:
        return jsonify({
            "mensaje": "Error al cargar el resumen de compra",
            "error": f"Detalles del error: {repr(e)}",
            "status": -1
        })

@app.route('/get_provincias/<int:departamento_id>')
def get_provincias(departamento_id):
    provincias = controlador_ubicacion.obtener_provincia_por_departamento(departamento_id)
    return jsonify(provincias)

@app.route('/get_distritos/<int:provincia_id>')
def get_distritos(provincia_id):
    distritos = controlador_ubicacion.obtener_distritos_por_provincia(provincia_id)
    return jsonify(distritos)


if __name__ == "__main__":
    app.run(debug=True)
    
    
#     @app.get('/productos')
# def seccionProductos():
#     idUsuario = session.get("usuario", {}).get("idUsuario", None)
    
#     productos = controlador_productos.obtener_productos()
#     generos = controlador_productos.obtener_generos()
#     categorias = controlador_productos.obtener_categorias()
#     colores = controlador_productos.obtener_colores()
#     marcas = controlador_marca.obtener_marcas()

#     if idUsuario is None:
#         return render_template("SeccionProductos.html", productos=productos,generos=generos,categorias=categorias,colores=colores,marcas=marcas)
#     else:
#         favoritos = controlador_favoritos.obtener_favoritos(idUsuario)
#         ids_favoritos = {fav[0] for fav in favoritos}
#         return render_template("SeccionProductos.html", productos=productos,generos=generos,categorias=categorias,colores=colores,marcas=marcas, favoritos=ids_favoritos)
