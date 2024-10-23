from bd import conectarse as obtener_conexion

def obtener_tipos_usuario():
    conexion = obtener_conexion()
    tipos_usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idTipoUsuario, nombre FROM tipoUsuario")
        tipos_usuario = cursor.fetchall()
    conexion.close()
    return tipos_usuario

def insertar_tipo_usuario(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tipoUsuario (nombre) VALUES (%s)", (nombre,))
    conexion.commit()
    conexion.close()

def eliminar_tipo_usuario(idTipoUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM tipoUsuario WHERE idTipoUsuario = %s", (idTipoUsuario,))
    conexion.commit()
    conexion.close()

def obtener_tipo_usuario_por_id(idTipoUsuario):
    conexion = obtener_conexion()
    tipo_usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idTipoUsuario, nombre FROM tipoUsuario WHERE idTipoUsuario = %s", (idTipoUsuario,))
        tipo_usuario = cursor.fetchone()
    conexion.close()
    return tipo_usuario

def actualizar_tipo_usuario(idTipoUsuario, nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipoUsuario SET nombre = %s WHERE idTipoUsuario = %s", (nombre, idTipoUsuario))
    conexion.commit()
    conexion.close()

def obtener_tipo_usuario_por_nombre(nombre):
    conexion = obtener_conexion()
    tipo_usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM tipoUsuario WHERE nombre = %s", (nombre,))
        tipo_usuario = cursor.fetchone()
    conexion.close()
    return tipo_usuario
