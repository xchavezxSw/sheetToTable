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

        a = conexion.cursor()
        consulta = "select * from reserva;"
        a.execute(consulta)
        row_headers = [x[0] for x in a.description]  # this will extract row headers
        results = a.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))

        return json_data

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
                                                            "curdate() )"

        a.execute(sql)
        conexion.commit()
        result='ok'
        return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))


