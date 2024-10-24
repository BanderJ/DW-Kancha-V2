import pymysql
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path='.env')

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path='.env')

def conectarse():
    # Imprimir las variables de entorno para verificar su contenido
    # print("DB_HOST:", os.getenv('DB_HOST'))
    # print("DB_PORT:", os.getenv('DB_PORT'))
    # print("DB_USER:", os.getenv('DB_USER'))
    # print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
    # print("DB_NAME:", os.getenv('DB_NAME'))

    # return pymysql.connect(
    #     host=os.getenv('DB_HOST'),         # Leer host desde .env
    #     port=int(os.getenv('DB_PORT', 3306)),  # Establecer un valor por defecto
    #     user=os.getenv('DB_USER'),         # Leer usuario desde .env
    #     password=os.getenv('DB_PASSWORD'), # Leer contraseña desde .env
    #     db=os.getenv('DB_NAME')            # Leer base de datos desde .env
    # )
    
    return pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='',
                                db='kancha')