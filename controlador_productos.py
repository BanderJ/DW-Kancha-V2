from bd import conectarse
import os

# Función para guardar imágenes en la carpeta static/img
def guardar_imagen(archivo, carpeta='static/img'):
    ruta = os.path.join(carpeta, archivo.filename)
    archivo.save(ruta)
    return archivo.filename

# Insertar producto con imágenes, colores y categorías
def insertar_producto(precio, stock, idModelo, idTalla, genero, tipo_producto, imagenPrincipal, imagenSecundarias, colores, categorias,descripcion):
    conexion = conectarse()
    try:
        # Guardar las imágenes
        imagen_principal_nombre = guardar_imagen(imagenPrincipal)
        imagen_secundarias_nombres = [guardar_imagen(imagen) for imagen in imagenSecundarias]

        with conexion.cursor() as cursor:
            # Insertar en la tabla Imagen
            cursor.execute(
                "INSERT INTO Imagen (imagenPrincipal, imagenSec01, imagenSec02, imagenSec03) VALUES (%s, %s, %s, %s)",
                (imagen_principal_nombre, imagen_secundarias_nombres[0], imagen_secundarias_nombres[1], imagen_secundarias_nombres[2])
            )
            idImagen = cursor.lastrowid

            # Insertar en la tabla Producto
            cursor.execute(
                "INSERT INTO Producto (precio, stock, idModelo, idTalla, idImagen, idGenero, idTipo, descripcion) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)",
                (precio, stock, idModelo, idTalla, idImagen, genero, tipo_producto, descripcion)
            )
            idProducto = cursor.lastrowid

            # Insertar en Producto_Color
            for color in colores:
                cursor.execute("INSERT INTO Producto_Color (idProducto, idColor) VALUES (%s, %s)", (idProducto, color))

            # Insertar en CategoriaProducto
            for categoria in categorias:
                cursor.execute("INSERT INTO CategoriaProducto (CategoriaidCategoria, ProductoidProducto) VALUES (%s, %s)", (categoria, idProducto))

        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()

# Obtener lista de productos con todas sus relaciones
def obtener_productos():
    conexion = conectarse()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.idProducto, p.precio, p.stock, m.nombre AS modelo_nombre, 
                   GROUP_CONCAT(DISTINCT c.nombre SEPARATOR ', ') AS colores, 
                   ge.nombre as genero, t.nombre AS talla_nombre, 
                   tp.nombre as tipo_producto, img.imagenPrincipal, img.imagenSec01, img.imagenSec02, img.imagenSec03, p.descripcion
            FROM Producto p
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Talla t ON p.idTalla = t.id
            JOIN Producto_Color pc ON pc.idProducto = p.idProducto
            JOIN Color c ON pc.idColor = c.idColor
            JOIN Imagen img ON p.idImagen = img.idImagen
            JOIN Genero ge ON ge.idGenero = p.idGenero
            JOIN tipo_producto tp ON tp.idTipo = p.idTipo
            GROUP BY p.idProducto
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos

# Obtener producto por ID para editar
def obtener_producto_por_id(id):
    conexion = conectarse()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.idProducto, p.precio, p.stock, m.nombre AS modelo_nombre, 
                   GROUP_CONCAT(DISTINCT c.nombre SEPARATOR ', ') AS colores, 
                   ge.nombre as genero, t.nombre AS talla_nombre, 
                   tp.nombre as tipo_producto, img.imagenPrincipal, img.imagenSec01, img.imagenSec02, img.imagenSec03, p.descripcion
            FROM Producto p
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Talla t ON p.idTalla = t.id
            JOIN Producto_Color pc ON pc.idProducto = p.idProducto
            JOIN Color c ON pc.idColor = c.idColor
            JOIN Imagen img ON p.idImagen = img.idImagen
            JOIN Genero ge ON ge.idGenero = p.idGenero
            JOIN tipo_producto tp ON tp.idTipo = p.idTipo
            WHERE p.idProducto = %s
            GROUP BY p.idProducto
            
        """, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

# Actualizar producto
def actualizar_producto(id, precio, stock, idModelo, idTalla, genero, tipo_producto, imagenPrincipal, imagenSecundarias, colores, categorias,descripcion):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Actualizar imágenes si se han subido nuevas
            if imagenPrincipal:
                imagen_principal_nombre = guardar_imagen(imagenPrincipal)
                imagen_secundarias_nombres = [guardar_imagen(imagen) for imagen in imagenSecundarias]
                cursor.execute("""
                    UPDATE Imagen SET imagenPrincipal = %s, imagenSec01 = %s, imagenSec02 = %s, imagenSec03 = %s 
                    WHERE idImagen = (SELECT idImagen FROM Producto WHERE idProducto = %s)
                """, (imagen_principal_nombre, imagen_secundarias_nombres[0], imagen_secundarias_nombres[1], imagen_secundarias_nombres[2], id))

            # Actualizar producto
            cursor.execute("""
                UPDATE Producto set precio = %s, stock = %s, idModelo = %s, idTalla = %s, idGenero = %s, idTipo = %s, descripcion =%s
                WHERE idProducto = %s
            """, ( precio, stock, idModelo, idTalla, genero, tipo_producto, descripcion,id))

            # Actualizar colores y categorías
            cursor.execute("DELETE FROM Producto_Color WHERE idProducto = %s", (id,))
            for color in colores:
                cursor.execute("INSERT INTO Producto_Color (idProducto, idColor) VALUES (%s, %s)", (id, color))

            cursor.execute("DELETE FROM CategoriaProducto WHERE ProductoidProducto = %s", (id,))
            for categoria in categorias:
                cursor.execute("INSERT INTO CategoriaProducto (CategoriaidCategoria, ProductoidProducto) VALUES (%s, %s)", (categoria, id))

        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()

# Eliminar producto y sus relaciones
def eliminar_producto(id):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM Producto_Color WHERE idProducto = %s", (id,))
            cursor.execute("DELETE FROM CategoriaProducto WHERE ProductoidProducto = %s", (id,))
            cursor.execute("DELETE FROM Producto WHERE idProducto = %s", (id,))
            cursor.execute("DELETE FROM Imagen WHERE idImagen = (SELECT idImagen FROM Producto WHERE idProducto = %s)", (id,))
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()

# Obtener modelos y tallas
def obtener_modelos():
    conexion = conectarse()
    modelos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idModelo, nombre FROM Modelo")
        modelos = cursor.fetchall()
    conexion.close()
    return modelos

def obtener_tallas():
    conexion = conectarse()
    tallas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre FROM Talla")
        tallas = cursor.fetchall()
    conexion.close()
    return tallas
def obtener_colores():
    conexion = conectarse()
    colores = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idColor, nombre FROM Color")
        colores = cursor.fetchall()
    conexion.close()
    return colores

def obtener_categorias():
    conexion = conectarse()
    categorias = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idCategoria, nombre FROM Categoria")
        categorias = cursor.fetchall()
    conexion.close()
    return categorias

def obtener_generos():
    conexion = conectarse()
    colores = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idGenero, nombre FROM Genero")
        colores = cursor.fetchall()
    conexion.close()
    return colores

def obtener_tipos():
    conexion = conectarse()
    categorias = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idTipo, nombre FROM Tipo_Producto")
        categorias = cursor.fetchall()
    conexion.close()
    return categorias

