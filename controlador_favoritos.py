from bd import conectarse

cliente = 1

def obtener_favoritos(cliente):
    conexion = conectarse()
    favoritos = []
    with conexion.cursor() as cursor:
        cursor.execute("""select p.idProducto, m.nombre as modelo_nombre, p.precio, img.imagenPrincipal, tp.nombre, idCliente
                        from favoritos fv inner join producto p on fv.idProducto = p.idProducto
                        inner join usuario us on fv.idCliente = us.idUsuario
                        inner join modelo m on p.idModelo = m.idModelo
                        inner join imagen img on p.idImagen = img.idImagen 
                        inner join tipo_producto tp on p.idTipo = tp.idTipo
                        where idCliente = %s
                    """, (cliente))
        favoritos = cursor.fetchall()
    conexion.close()
    print(favoritos)
    return favoritos

def insertar_favoritos (idCliente, idProducto):
    conexion = conectarse()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO favoritos (idCliente, idProducto) values (%s, %s)", (idCliente, idProducto))
        conexion.commit()
    conexion.close()
    
    
def eliminar_favoritos (idCliente, idProducto):
    conexion = conectarse()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM favoritos where idCliente = %s and idProducto = %s", (idCliente, idProducto))
        conexion.commit()
    conexion.close()

