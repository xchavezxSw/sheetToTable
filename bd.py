import mysql as dd
conexion= dd.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Oracle50",
    database="conexion"
)
conexion.ping()