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
    try:
        a = conexion.cursor()
        sql = "INSERT INTO `reserva` ( id, \
EmailAddres,emailcandidato, \
nombreyapellidodelcandidato, \
idreserva,Linkedin, \
tecnologiasquesabeelcandidato,tipodeperfildelcandidato, \
motivo,status,ComentariosAdicionales,FECHA    ) VALUES (%i, %s, %s, %i, %s, %s, %s, %s, %s, %s, %s, %d )"
        a.execute(sql, (None,
                        values['EmailInf'],
                        values['EMailCandidatoInf'],
                        values['NombreyApellidodelCandidatoInf'],
                        values['IdsaEnviarInf'],values['LKCandiInf'],
                        ",".join(values['TecnoCandiInf']),
                        ",".join(values['TpCandiInf']),
                        None,
                        '1',
                         values['CommentInf'],
                        datetime.date.today()
                        ))
        conexion.commit()
        result='ok'
        return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))
    except:
        print("falle")
contratados()