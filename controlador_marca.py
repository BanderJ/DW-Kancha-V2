from bd import conectarse as obtener_conexion

def obtener_marcas():
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMarca, nombre FROM marca")
        marcas = cursor.fetchall()
    conexion.close()
    return marcas

def insertar_marca(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO marca(nombre) VALUES (%s)", (nombre,))
    conexion.commit()
    conexion.close()

def eliminar_marca(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM marca WHERE idMarca = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_marca_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMarca, nombre FROM marca WHERE idMarca = %s", (id,))
        marca = cursor.fetchone()
    conexion.close()
    return marca

def actualizar_marca(nombre, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE marca SET nombre = %s WHERE idMarca = %s", (nombre, id))
    conexion.commit()
    conexion.close()
    
def buscar_marca_por_nombre(nombre):
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMarca, nombre FROM marca WHERE nombre LIKE %s", ('%' + nombre + '%',))
        marcas = cursor.fetchall()
    conexion.close()
    return marcas
