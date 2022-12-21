from mysql import connector
import socket
myhost = socket.gethostname()
if 'DESKTOP-EKG5FVQ'==myhost:
    print(myhost)
    conexion= connector.connect(
    host="127.0.0.1",
    port='3309',
    user="root",
    password="Oracle50",
    database="conexion"
    )
else:
    conexion= connector.connect(
    host="127.0.0.1",
    user="root",
    password="Oracle50",
    database="conexion"
    )
conexion.ping()
def connectar():
    if 'DESKTOP-EKG5FVQ'==myhost:
        print(myhost)
        conexion= connector.connect(
        host="127.0.0.1",
        port='3309',
        user="root",
        password="Oracle50",
        database="conexion"
        )
    else:
        conexion= connector.connect(
        host="127.0.0.1",
        user="root",
        password="Oracle50",
        database="conexion"
        )
    return conexion