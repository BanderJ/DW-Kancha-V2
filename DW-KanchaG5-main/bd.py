import pymysql

def conectarse():
    return pymysql.connect(user="root",password="",host="127.0.0.1",port=3306,db="bd_kancha")