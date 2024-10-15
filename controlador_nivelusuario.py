from bd import conectarse as obtener_conexion

def obtener_nivelusuario():
    conexion = obtener_conexion()
    nivelusuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idNivelUsuario, nombre, puntosRequeridos FROM nivelusuario")
        nivelusuario = cursor.fetchall()
    conexion.close()
    return nivelusuario

def insertar_nivelUsuario(nombre, puntosRequeridos):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO nivelusuario(nombre, puntosRequeridos) VALUES (%s, %s)",
                       (nombre, puntosRequeridos))
    conexion.commit()
    conexion.close()
    
def eliminar_nivelUsuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM nivelusuario WHERE idNivelUsuario = %s", (id,))
    conexion.commit()
    conexion.close()
    

def obtener_nivelusuario_por_id(id):
    conexion = obtener_conexion()
    nivelusuario = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT idNivelUsuario, nombre, puntosRequeridos FROM nivelusuario WHERE idNivelUsuario = %s", (id,))
        nivelusuario = cursor.fetchone()
    conexion.close()
    return nivelusuario


def actualizar_nivelusuario(nombre, puntos, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE nivelusuario SET nombre = %s, puntosRequeridos = %s WHERE idNivelUsuario = %s",
                       (nombre, puntos, id))
    conexion.commit()
    conexion.close()