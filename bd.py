import pymysql

def conectarse():
    return pymysql.connect(user="root",
                           password="",
                           host="localhost",
                           port=3306,
                           db="dawa_kancha")