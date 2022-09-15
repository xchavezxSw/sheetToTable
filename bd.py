import pymysql as dd
print(dir(dd))
conexion= dd.Connect(
    host="127.0.0.1",
    user="root",
    password="Oracle50",
    database="conexion"
)
