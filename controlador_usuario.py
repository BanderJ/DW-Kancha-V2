from bd import conectarse as obtener_conexion

def obtener_usuario():
    conexion = obtener_conexion()
    usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT usu.idUsuario, usu.nombre, usu.numDoc, usu.apePat, usu.apeMat, usu.correo, usu.telefono, 
                   usu.fechaNacimiento, usu.sexo, tu.nombre as TipoUsuario, nu.nombre as NivelUsuario
            FROM usuario usu
            INNER JOIN tipousuario tu ON tu.idTipoUsuario = usu.idTipoUsuario
            INNER JOIN nivelusuario nu ON nu.idNivelUsuario = usu.idNivelUsuario;
        """)
        usuario = cursor.fetchall()
    conexion.close()
    return usuario

def insertar_usuario(idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, telefono, fechaNacimiento, sexo, idNivelUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO usuario (idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, telefono, fechaNacimiento, sexo, idNivelUsuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, password, telefono, fechaNacimiento, sexo, idNivelUsuario))
    conexion.commit()
    conexion.close()

def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuario WHERE idUsuario = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT usu.idUsuario, usu.nombre, usu.numDoc, usu.apePat, usu.apeMat, usu.correo, usu.telefono,
                   usu.fechaNacimiento, usu.sexo, tu.nombre as TipoUsuario, nu.nombre as NivelUsuario
            FROM usuario usu
            INNER JOIN tipousuario tu ON tu.idTipoUsuario = usu.idTipoUsuario
            INNER JOIN nivelusuario nu ON nu.idNivelUsuario = usu.idNivelUsuario
            WHERE idUsuario = %s
        """, (id,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario

def actualizar_usuario(idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, telefono, fechaNacimiento, sexo, idNivelUsuario, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE usuario
            SET idTipoUsuario = %s, nombre = %s, numDoc = %s, apePat = %s, apeMat = %s, correo = %s, 
                telefono = %s, fechaNacimiento = %s, sexo = %s, idNivelUsuario = %s
            WHERE idUsuario = %s
        """, (idTipoUsuario, nombre, numDoc, apePat, apeMat, correo, telefono, fechaNacimiento, sexo, idNivelUsuario, id))
    conexion.commit()
    conexion.close()

def actualizarPerfilUsuario(nombre, numDoc, apePat, apeMat, correo,fechaNac,telefono,sexo, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuario SET nombre = %s, numDoc = %s, apePat = %s, apeMat = %s, correo = %s, fechaNacimiento=%s, telefono=%s,sexo=%s WHERE idusuario = %s",
                       (nombre, numDoc, apePat, apeMat, correo,fechaNac,telefono,sexo, id))
    conexion.commit()
    conexion.close()
