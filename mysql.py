import datetime

from bd import conexion
import json
def encliente():
    try:
            a=conexion.cursor()
            consulta = "select * from cliente;"
            a.execute(consulta)
            result = a.fetchall()
            return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))
    except:
        print("falle")


def reservados():
    try:
        a = conexion.cursor()
        consulta = "select * from reserva;"
        a.execute(consulta)
        result = a.fetchall()
        return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))
    except:
        print("falle")
def contratados():
    try:
        a = conexion.cursor()
        consulta = "select * from contratados;"
        a.execute(consulta)
        result = a.fetchall()
        return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))
    except:
        print("falle")
def insertreserva(values):
        a = conexion.cursor()
        sql = "INSERT INTO `reserva` ( id, \
EmailAddres,emailcandidato, \
nombreyapellidodelcandidato, \
idreserva,Linkedin, \
tecnologiasquesabeelcandidato,tipodeperfildelcandidato, \
motivo,status,ComentariosAdicionales,FECHA    ) VALUES (0, '"+values['email']+"', " \
                                                            "'"+values['emailCandidato']+"', " \
                                                            "'"+values['naCandi']+"', " \
                                                            ""+values['idReserva']+", " \
                                                            "'"+values['lkCandi']+"', " \
                                                            "'"+",".join(values['tcandi'])+"', " \
                                                            "'"+ ",".join(values['tperfil'])+"', " \
                                                            "'', " \
                                                            "'1', " \
                                                            "'"+values['comment']+"', " \
                                                            "'"+datetime.date.today().strftime("%m/%d/%Y, %H:%M:%S")+"' )"

        a.execute(sql)
        conexion.commit()
        result='ok'
        return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))


