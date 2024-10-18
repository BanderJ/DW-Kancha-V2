from bd import conectarse as obtener_conexion

def obtener_usuario():
    conexion = obtener_conexion()
    usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("select usu.idUsuario, usu.nombre, usu.numDoc, usu.apePat, usu.apeMat, usu.correo, tu.nombre as TipoUsuario, nu.nombre as NivelUsuario from usuario usu inner join tipousuario tu on tu.idTipoUsuario = usu.idTipoUsuario inner join nivelusuario nu on nu.idNivelUsuario = usu.idNivelUsuario;")
        usuario = cursor.fetchall()
    conexion.close()
    return usuario

def insertar_usuario(idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, idNivelUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuario(idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, idNivelUsuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, idNivelUsuario))
    conexion.commit()
    conexion.close()
    
def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuario WHERE idusuario = %s", (id,))
    conexion.commit()
    conexion.close()
    

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "select usu.idUsuario, usu.nombre, usu.numDoc, usu.apePat, usu.apeMat, usu.correo, tu.nombre as TipoUsuario, nu.nombre as NivelUsuario from usuario usu inner join tipousuario tu on tu.idTipoUsuario = usu.idTipoUsuario inner join nivelusuario nu on nu.idNivelUsuario = usu.idNivelUsuario WHERE idusuario = %s", (id,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario


def actualizar_usuario(idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, idNivelUsuario, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuario SET idTipoUsuario = %s, nombre = %s, numDoc = %s, apePat = %s, apeMat = %s, correo = %s, password = %s, idNivelUsuario = %s WHERE idusuario = %s",
                       (idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, idNivelUsuario, id))
    conexion.commit()
    conexion.close()