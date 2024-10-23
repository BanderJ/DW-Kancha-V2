from bd import conectarse
import os

# Función para guardar imágenes en la carpeta static/img
def guardar_imagen(archivo, carpeta='static/img'):
    ruta = os.path.join(carpeta, archivo.filename)
    archivo.save(ruta)
    return archivo.filename

# Insertar producto con imágenes, colores y categorías
def insertar_producto(precio, stock, idModelo, idTalla, genero, tipo_producto, imagenPrincipal, imagenSecundarias, colores, categorias,descripcion,estado):
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
                "INSERT INTO Producto (precio, stock, idModelo, idTalla, idImagen, idGenero, idTipo, descripcion,estado) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (precio, stock, idModelo, idTalla, idImagen, genero, tipo_producto, descripcion,estado)
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

def obtener_3_producto():
    conexion = conectarse()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.idProducto, p.precio, p.stock, m.nombre AS modelo_nombre, 
                   c.nombre AS color, 
                   ge.nombre as genero, t.nombre AS talla_nombre, 
                   tp.nombre as tipo_producto, img.imagenPrincipal, img.imagenSec01, img.imagenSec02, img.imagenSec03, p.descripcion, p.estado, ma.nombre
            FROM Producto p 
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Marca ma ON m.idMarca = ma.idMarca
            JOIN Talla t ON p.idTalla = t.id
            JOIN Producto_Color pc ON pc.idProducto = p.idProducto
            JOIN Color c ON pc.idColor = c.idColor
            JOIN Imagen img ON p.idImagen = img.idImagen
            JOIN Genero ge ON ge.idGenero = p.idGenero
            JOIN tipo_producto tp ON tp.idTipo = p.idTipo
            GROUP BY m.idModelo, c.idColor, tp.nombre
            LIMIT 3
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_productos_diferentes(genero, deporte, precio, color, marca):
    conexion = conectarse()
    productos = []
    with conexion.cursor() as cursor:

        query = """
            SELECT p.idProducto, p.precio, p.stock, m.nombre AS modelo_nombre, 
                   c.nombre AS color,  -- Cambié esto para obtener cada color individualmente
                   ge.nombre AS genero, t.nombre AS talla_nombre, 
                   tp.nombre AS tipo_producto, img.imagenPrincipal, img.imagenSec01, img.imagenSec02, img.imagenSec03, p.descripcion, p.estado, ma.nombre
            FROM Producto p 
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Marca ma ON m.idMarca = ma.idMarca
            JOIN Talla t ON p.idTalla = t.id
            JOIN Producto_Color pc ON pc.idProducto = p.idProducto
            JOIN Color c ON pc.idColor = c.idColor
            JOIN Imagen img ON p.idImagen = img.idImagen
            JOIN Genero ge ON ge.idGenero = p.idGenero
            JOIN tipo_producto tp ON tp.idTipo = p.idTipo

        """
        filtros = []
        if genero:
            query += " AND ge.nombre = %s"
            filtros.append(genero)
        if deporte:
            query += " AND tp.nombre = %s"
            filtros.append(deporte)
        if precio:
            query += " AND p.precio <= %s"
            filtros.append(precio)
        if color:
            query += " AND c.nombre = %s"
            filtros.append(color)
        if marca:
            query += " AND ma.nombre = %s"
            filtros.append(marca)
        
        # Agrupamos también por colores
        query += " GROUP BY m.idModelo, c.idColor, tp.nombre"
        
        cursor.execute(query, filtros)
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
                   tp.nombre as tipo_producto, img.imagenPrincipal, img.imagenSec01, img.imagenSec02, img.imagenSec03, p.descripcion, p.estado, ma.nombre, ma.imagen
            FROM Producto p
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Marca ma ON m.idMarca = ma.idMarca
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

def obtener_productos():
    conexion = conectarse()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.idProducto, p.precio, p.stock, m.nombre AS modelo_nombre, 
                   GROUP_CONCAT(DISTINCT c.nombre SEPARATOR ', ') AS colores, 
                   ge.nombre as genero, t.nombre AS talla_nombre, 
                   tp.nombre as tipo_producto, img.imagenPrincipal, img.imagenSec01, img.imagenSec02, img.imagenSec03, p.descripcion, p.estado, ma.nombre
            FROM Producto p 
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Marca ma ON m.idMarca = ma.idMarca
            JOIN Talla t ON p.idTalla = t.id
            JOIN Producto_Color pc ON pc.idProducto = p.idProducto
            JOIN Color c ON pc.idColor = c.idColor
            JOIN Imagen img ON p.idImagen = img.idImagen
            JOIN Genero ge ON ge.idGenero = p.idGenero
            JOIN tipo_producto tp ON tp.idTipo = p.idTipo
            GROUP BY p.idProducto
            
        """)
        producto = cursor.fetchall()
    conexion.close()
    return producto


def obtenerConColorDiferentePorID(id):
    conexion = conectarse()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.idProducto, p.descripcion, p.precio, i.imagenPrincipal, pc.idColor
            FROM producto p
            JOIN producto_color pc ON p.idProducto = pc.idProducto
            JOIN imagen i ON p.idImagen = i.idImagen
            WHERE p.idModelo = (SELECT idModelo FROM producto WHERE idProducto = %s)
            AND p.idGenero = (SELECT idGenero FROM producto WHERE idProducto = %s)
            AND p.idTalla = (SELECT idTalla FROM producto WHERE idProducto = %s)
            AND p.idTipo = (SELECT idTipo FROM producto WHERE idProducto = %s)
            AND p.idProducto != %s -- Excluye el producto actual
            LIMIT 3;
        """, (id, id, id, id, id))
        producto = cursor.fetchall()
    conexion.close()
    return producto

def obtenerTallasPorProducto(id):
    conexion = conectarse()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.idProducto, t.nombre, p.stock
            FROM Producto p 
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Talla t ON p.idTalla = t.id
            JOIN Producto_Color pc ON pc.idProducto = p.idProducto
            JOIN Color c ON pc.idColor = c.idColor
            JOIN Imagen img ON p.idImagen = img.idImagen
            JOIN Genero ge ON ge.idGenero = p.idGenero
            JOIN tipo_producto tp ON tp.idTipo = p.idTipo
            WHERE m.idModelo = (SELECT idModelo FROM producto WHERE idProducto=%s)
            AND c.idColor IN (SELECT idColor FROM producto_color WHERE idProducto = %s)
            AND tp.idTipo = (SELECT idTipo FROM producto WHERE idProducto=%s)
            AND p.idGenero = (SELECT idTipo FROM producto WHERE idProducto = %s)
            GROUP BY t.nombre, p.stock;
        """, (id, id, id, id))
        producto = cursor.fetchall()
    conexion.close()
    return producto

    

# Actualizar producto
def actualizar_producto(id, precio, stock, idModelo, idTalla, genero, tipo_producto, imagenPrincipal, imagenSecundarias, colores, categorias,descripcion,estado):
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
                UPDATE Producto set precio = %s, stock = %s, idModelo = %s, idTalla = %s, idGenero = %s, idTipo = %s, descripcion =%s, estado =%s
                WHERE idProducto = %s
            """, ( precio, stock, idModelo, idTalla, genero, tipo_producto, descripcion,estado,id))

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

