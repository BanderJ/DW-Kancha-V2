from bd import conectarse

def insertProduct():
    conexion = conectarse()
    try:
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("")
                conexion.commit()
                conexion.close()
    except:
        print("Error al insertar producto")

def listarProductos():
    conexion = conectarse()
    try:
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("select * from producto")
                registros = cursor.fetchall()
                return registros
    except:
        print("Error al insertar producto")

def updateProducto():
    try:
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("")
                conexion.commit()
                conexion.close()
    except:
        print("Error al actualizar datos del producto")

def deleteProducto():
    conexion = conectarse()
    try:
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("")
                conexion.commit()
                conexion.close()
    except:
        print("Error al eliminar producto")