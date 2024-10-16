from bd import conectarse as obtener_conexion

def obtener_categorias():
    conexion = obtener_conexion()
    categoria = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idCategoria, nombre FROM categoria")
        categoria = cursor.fetchall()
    conexion.close()
    return categoria

def insertar_Categoria(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO categoria(nombre) VALUES (%s)",
                       (nombre))
    conexion.commit()
    conexion.close()
    
def eliminar_categoria(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM categoria WHERE idCategoria = %s", (id,))
    conexion.commit()
    conexion.close()
    

def obtener_categoria_por_id(id):
    conexion = obtener_conexion()
    categoria = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idCategoria, nombre from categoria WHERE idCategoria = %s", (id,))
        categoria = cursor.fetchone()
    conexion.close()
    return categoria


def actualizar_categoria(nombre, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE categoria SET nombre = %s WHERE idCategoria = %s",
                       (nombre, id))
    conexion.commit()
    conexion.close()