from bd import conectarse
import os

# Función para guardar imágenes en la carpeta static/img
def guardar_imagen(archivo, carpeta='static/img'):
    ruta = os.path.join(carpeta, archivo.filename)
    archivo.save(ruta)
    return archivo.filename

# Obtener marcas con imagen
def obtener_marcas():
    conexion = conectarse()
    marcas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMarca, nombre, imagen FROM marca")
        marcas = cursor.fetchall()
    conexion.close()
    return marcas

# Insertar marca con imagen
def insertar_marca(nombre, imagen):
    conexion = conectarse()
    try:
        # Guardar la imagen
        nombre_imagen = guardar_imagen(imagen)
        
        # Insertar la nueva marca
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO marca (nombre, imagen) VALUES (%s, %s)", (nombre, nombre_imagen))
        conexion.commit()
        return True, "Marca agregada correctamente."
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally:
        conexion.close()

# Eliminar marca por ID
def eliminar_marca(id):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Primero verifica si hay modelos asociados
            cursor.execute("SELECT COUNT(*) FROM modelo WHERE idMarca = %s", (id,))
            count = cursor.fetchone()[0]
            if count > 0:
                return False
            
            # Si no hay modelos, procede a eliminar
            cursor.execute("DELETE FROM marca WHERE idMarca = %s", (id,))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally:
        conexion.close()

# Obtener marca por ID
def obtener_marca_por_id(id):
    conexion = conectarse()
    marca = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMarca, nombre, imagen FROM marca WHERE idMarca = %s", (id,))
        marca = cursor.fetchone()
    conexion.close()
    return marca

# Actualizar marca con imagen
def actualizar_marca(nombre, imagen, id):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Si se ha subido una nueva imagen
            if imagen:
                nombre_imagen = guardar_imagen(imagen)
                cursor.execute("UPDATE marca SET nombre = %s, imagen = %s WHERE idMarca = %s", (nombre, nombre_imagen, id))
            else:
                # Si no se subió nueva imagen
                cursor.execute("UPDATE marca SET nombre = %s WHERE idMarca = %s", (nombre, id))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally:
        conexion.close()

# Buscar marcas por nombre
def buscar_marca_por_nombre(nombre):
    conexion = conectarse()
    marcas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMarca, nombre, imagen FROM marca WHERE nombre LIKE %s", ('%' + nombre + '%',))
        marcas = cursor.fetchall()
    conexion.close()
    return marcas
