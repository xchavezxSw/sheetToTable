import datetime

from bd import conexion
import json
def status(id):
    if id=="1":
        return 'Reservado'
    if id=="2":
        return 'En Cliente'
    if id=="4" :
        return  'Entrevista Con Cliente (no técnica)'
    if id=="5" :
        return  'Entrevista Técnica'
    if id=="6" :
        return  'Ejercicio Técnico'
    if id=="7" :
        return  'Trámites Ingreso'
    if id=="8" :
        return  'Oferta'
    if id=="9" :
        return  'On Hold '
    if id=="10" :
        return  'Pre-Offer '
    if id=="11" :
        return  'Ingreso'
    if id=="12" :
        return  'Fuera de proceso'
def miscandidatos(usuario=''):
    a = conexion.cursor()
    consulta = "select EmailAddres,emailcandidato,idbusqueda,idstatus from metricas where 1=1"
    if usuario != '':
        consulta = consulta + " and EmailAddres='" + usuario + "'"
    a.execute(consulta)
    results = a.fetchall()
    json_data = []
    for result in results:
        json_data.append([result[0], result[1], result[2], status(str(result[3]))])
    return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))

def encliente(usuario=''):

            a=conexion.cursor()
            consulta = "select * from cliente where idstatus not in ('11','12')"
            if usuario !='':
                consulta=consulta+" and EmailAddres='"+usuario+"'"
            a.execute(consulta)
            results = a.fetchall()
            json_data = []
            for result in results:
                json_data.append([result[0], result[1], result[2], status(str(result[3])), result[4], result[5],
                                  result[6], result[7], result[8], result[9], result[10], str(result[11])])
            return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))

def reservados(usuario=''):
        a = conexion.cursor()
        consulta = "select * from reserva where 1=1 "
        if usuario != '':
            consulta = consulta + " and EmailAddres='" + usuario +"'"
        print(consulta)
        a.execute(consulta)
        #row_headers = [x[0] for x in a.description]  # this will extract row headers
        results = a.fetchall()
        json_data = []
       # json_data.append(row_headers)
        for result in results:
            json_data.append( [result[0],result[1],result[2],result[3],result[4],result[5],
                                                    result[6],result[7],result[8],status(str(result[9])),result[10],str(result[11])])
        return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))
def metrica(usuario='',rol=''):
    a = conexion.cursor()
    consulta = "select * from metricas m  where 1=1  "
    if usuario != '' and rol != 'admin':
        consulta = consulta + " and EmailAddres='" + usuario + "'"
    a.execute(consulta)
    # row_headers = [x[0] for x in a.description]  # this will extract row headers
    results = a.fetchall()
    json_data = []
    # json_data.append(row_headers)
    for result in results:
        json_data.append([ result[1], result[2], result[3], result[4], result[5],
                          result[6], result[7], result[8], result[9], result[10], str(result[11]),
                           result[12], result[13], status(str(result[14])), result[15], result[16]
                           ])
    return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))



def contratadosFun(usuario=''):
        a = conexion.cursor()
        consulta = "select * from contratados  where 1=1 "
        if usuario != '':
            consulta = consulta + " and EmailAddres='" + usuario + "'"
        a.execute(consulta)
        results = a.fetchall()
        json_data = []
        for result in results:
            json_data.append([result[0], result[1], result[2], result[3], str(result[4]), result[5], str(result[6])
                              ])
        return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))


def updateReserva(date_time, email, emailCandidato, naCandi, lkCandi, tcandi, tperfil, idReserva, comment):
    a = conexion.cursor()
    sql="update reserva set " \
        "Linkedin='"+lkCandi+"'" \
        ",tecnologiasquesabeelcandidato='"+tcandi+"'" \
        ",tipodeperfildelcandidato='"+tperfil+"'" \
        ",ComentariosAdicionales='" + comment + "'" \
        ",FECHA=curdate() " \
        "where EmailAddres='"+email+"' and " \
        "emailcandidato='"+emailCandidato+"' and " \
        "idreserva='" + idReserva + "'"
    a.execute(sql)
    conexion.commit()
    result = 'ok'
    return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))
def insertreserva(values):
        print("inserto")
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


def insertinforme(idbusqueda,emailAddress,emailCandidato):
        a = conexion.cursor()
        sql = "INSERT INTO conexion.cargaInforme (" \
              "idbusqueda, emailAddress, emailCandidato)" \
              " VALUES ('"+idbusqueda+"', " \
              "'"+emailAddress+"', " \
              "'" +emailCandidato + "') "
        print(sql)
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
def login(usuario,contrasena):
    from bd import conexion
    a = conexion.cursor()
    consulta = "select count(*) ,role from users where trim(email)=trim('"+usuario+"') and trim(password)=trim('"+contrasena+"') group by role;"
    print(consulta)
    a.execute(consulta)
    results = a.fetchall()
    if len(results)>=1:
        return results[0][0],results[0][1]
    else:
        return 0,None

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
def insertEstado11(emailCandi,idSt,emailSt,statusSt,salarioMensualAcordadoSt,fechaIngresoSt,comentariosSt):
    a = conexion.cursor()
    sql = "INSERT INTO `contratados` ( id,EmailAddres, \
                                       emailcandidato, \
                                        idBusqueda, \
                                        salario, \
                                        Comentarios, \
                                        FECHAcontratado ) VALUES ( \
                                        0,  \
                                         '" +emailSt + "',  \
                                         '" + emailCandi + "',  \
                                        '" + idSt+ "', \
                                        " + str(float(salarioMensualAcordadoSt)) + ",  \
                                        '" + comentariosSt + "',  \
                                        '" + fechaIngresoSt + "');"
    a.execute(sql)
    conexion.commit()
    insertEstado(emailCandi,idSt,emailSt,statusSt)
    result = 'ok'
    return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))

def insertEstado12(emailCandi,idSt,emailSt,statusSt,salarioMensualOfrecidoClienteSt,salarioMensualPretendidoSt,motivoFinCandi,motivoFinCliente):
    a = conexion.cursor()
    if motivoFinCandi != '' or motivoFinCandi.strip() is None:
        sql = "INSERT INTO conexion.rechazados (" \
              "emailCandidato, idbusqueda, emailAddress, " \
              "status, salarioMensualOfrecidoCliente, salarioMensualPretendido, " \
              "motivorechazo, rechazadoPor) " \
              "VALUES('"+emailCandi+"', " \
                     "'"+idSt+"', " \
                     "'"+emailSt+"', " \
                     "'"+statusSt+"', " \
                     "'"+salarioMensualOfrecidoClienteSt+"', " \
                     "'"+salarioMensualPretendidoSt+"', " \
                     "'"+motivoFinCandi+"', " \
                     "'candidato');"
    else:
        sql = "INSERT INTO conexion.rechazados (" \
              "emailCandidato, idbusqueda, emailAddress, " \
              "status, salarioMensualOfrecidoCliente, salarioMensualPretendido, " \
              "motivorechazo, rechazadoPor) " \
              "VALUES('"+emailCandi+"', " \
                     "'"+idSt+"', " \
                     "'"+emailSt+"', " \
                     "'"+statusSt+"', " \
                     "'"+salarioMensualOfrecidoClienteSt+"', " \
                     "'"+salarioMensualPretendidoSt+"', " \
                     "'"+motivoFinCliente+"', " \
                     "'cliente');"

    a.execute(sql)
    conexion.commit()
    result = 'ok'
    return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))