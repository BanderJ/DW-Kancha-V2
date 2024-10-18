from bd import conectarse as obtener_conexion

def obtener_modelos():
    conexion = obtener_conexion()
    modelos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT m.idModelo, m.nombre, b.nombre AS nombreMarca 
            FROM Modelo m
            JOIN Marca b ON m.idMarca = b.idMarca
        """)
        modelos = cursor.fetchall()
    conexion.close()
    return modelos

def insertar_modelo(nombre, idMarca):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Modelo(nombre, idMarca) VALUES (%s, %s)", (nombre, idMarca))
    conexion.commit()
    conexion.close()

def eliminar_modelo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Modelo WHERE idModelo = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_modelo_por_id(id):
    conexion = obtener_conexion()
    modelo = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idModelo, nombre, idMarca FROM Modelo WHERE idModelo = %s", (id,))
        modelo = cursor.fetchone()
    conexion.close()
    return modelo

def actualizar_modelo(nombre, idMarca, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Modelo SET nombre = %s, idMarca = %s WHERE idModelo = %s",
                       (nombre, idMarca, id))
    conexion.commit()
    conexion.close()