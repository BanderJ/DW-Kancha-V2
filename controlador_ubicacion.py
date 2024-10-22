from flask import jsonify
from bd import conectarse

def obtener_departamentos():
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_departamento, nombre FROM departamento")
            departamentos = cursor.fetchall()
    finally:
        conexion.close()
    return departamentos

def obtener_provincia_por_departamento(id_departamento):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT pro.id_provincia, pro.nombre FROM provincia pro WHERE pro.id_departamento = %s", (id_departamento,))
            provincias = cursor.fetchall()
    finally:
        conexion.close()
    return provincias

def obtener_distritos_por_provincia(id_provincia):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_distrito, nombre FROM distrito WHERE id_provincia = %s", (id_provincia,))
            distritos = cursor.fetchall()
    finally:
        conexion.close()
    return distritos
