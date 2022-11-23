from mysql import connector
conexion= connector.connect(
    host="127.0.0.1",
    user="root",
    password="Oracle50",
    database="conexion"
)
conexion.ping()
def connectar():
    conexion = connector.connect(
        host="127.0.0.1",
        user="root",
        password="Oracle50",
        database="conexion"
    )
    return conexion
