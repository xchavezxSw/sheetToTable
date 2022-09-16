import datetime

from bd import conexion
import json
def status(id):
    if id=="2":
        return 'En Cliente'
    if id == "1":
        return 'Reservado'


def encliente():

            a=conexion.cursor()
            consulta = "select * from cliente;"
            a.execute(consulta)
            results = a.fetchall()
            json_data = []
            for result in results:
                json_data.append([result[0], result[1], result[2], status(str(result[3])), result[4], result[5],
                                  result[6], result[7], result[8], result[9], result[10], str(result[11])])
            return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))

def reservados():
        a = conexion.cursor()
        consulta = "select * from reserva;"
        a.execute(consulta)
        #row_headers = [x[0] for x in a.description]  # this will extract row headers
        results = a.fetchall()
        json_data = []
       # json_data.append(row_headers)
        for result in results:
            json_data.append( [result[0],result[1],result[2],result[3],result[4],result[5],
                                                    result[6],result[7],result[8],status(str(result[9])),result[10],str(result[11])])
        return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))

def contratadosFun():
        a = conexion.cursor()
        consulta = "select * from contratados;"
        a.execute(consulta)
        results = a.fetchall()
        json_data = []
        print(results)
        for result in results:
            json_data.append([result[0], result[1], result[2], result[3], result[4], result[5],
                              result[6], result[7], result[8], status(str(result[9])), result[10], str(result[11])])
        return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))


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


def insertCliente(values):
    a = conexion.cursor()
    sql = "INSERT INTO `cliente` ( EmailAddres, \
                                   emailcandidato, \
                                    idBusqueda, \
                                    idstatus, \
                                    Linkedin, \
                                    CV1Español, \
                                    CV2Ingles, \
                                    Inf1Español, \
                                    Inf2Ingles, \
                                    ComentariosInforme, \
                                    FECHA    ) VALUES ( \
                                    '"+values['EmailInf']+"',  \
                                     '"+values['EMailCandidatoInf']+"',  \
                                     '" + values['IdsaEnviarInf'] + "',  \
                                        '2',  \
                                    '" + values['LKCandiInf'] + "',  \
                                        '',  \
                                        '',  \
                                        '',  \
                                        '',  \
                                        '" + values['CommentInf'] + "',  \
                                        curdate()); "

    a.execute(sql)
    conexion.commit()
    result = 'ok'
    return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))

def devolvercambiostado(emailCandi,id):
        a = conexion.cursor()
        where=' 1=1 '
        if emailCandi is None or emailCandi != '':
            where=where+" and emailcandidato='"+emailCandi+"'"
        if id is None or id != '':
           where=where+" and idBusqueda = '"+id+"'"
        consulta = "select * from cliente where "+where +";"
        a.execute(consulta)
        results = a.fetchall()
        json_data = []
        for result in results:
            json_data.append([result[0], result[1], result[2], str(result[3]), result[4], result[5],
                              result[6], result[7], result[8], result[9], result[10], str(result[11])])
        return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))

def insertEstado(emailCandi,idSt,emailSt,statusSt):
    a = conexion.cursor()
    sql = "update cliente set idstatus='"+statusSt+"' " \
          "where emailcandidato='"+emailCandi+"' " \
          " and idBusqueda='"+idSt+"' " \
          " and EmailAddres='"+emailSt+"'"

    a.execute(sql)
    conexion.commit()
    result = 'ok'
    return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))