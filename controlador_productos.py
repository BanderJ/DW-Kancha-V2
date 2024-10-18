from bd import conectarse

def insertar_producto(nombre, precio, stock, idModelo, idTalla):
    conexion = conectarse()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Producto (nombre, precio, stock, idModelo, idTalla) VALUES (%s, %s, %s, %s, %s)",
            (nombre, precio, stock, idModelo, idTalla)
        )
    conexion.commit()
    conexion.close()

def obtener_productos():
    conexion = conectarse()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.idProducto, p.nombre, p.precio, p.stock, m.nombre AS modelo_nombre, t.nombre AS talla_nombre
            FROM Producto p
            JOIN Modelo m ON p.idModelo = m.idModelo
            JOIN Talla t ON p.idTalla = t.id
        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_producto_por_id(id):
    conexion = conectarse()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idProducto, nombre, precio, stock, idModelo, idTalla FROM Producto WHERE idProducto = %s", (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

def actualizar_producto(nombre, precio, stock, idModelo, idTalla, id):
    conexion = conectarse()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE Producto SET nombre = %s, precio = %s, stock = %s, idModelo = %s, idTalla = %s WHERE idProducto = %s",
            (nombre, precio, stock, idModelo, idTalla, id)
        )
    conexion.commit()
    conexion.close()

def eliminar_producto(id):
    conexion = conectarse()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Producto WHERE idProducto = %s", (id,))
    conexion.commit()
    conexion.close()

from bd import conectarse

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

# Las demás funciones (insertar_producto, obtener_productos, etc.) se mantienen igual

