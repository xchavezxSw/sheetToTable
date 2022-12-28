import datetime

from bd import conexion,connectar
import json
import base64
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
    if id=="13" :
        return  'Informe Cargado'
def miscandidatos(usuario=''):
    db=connectar()
    a = db.cursor()
    consulta = "select EmailAddres,emailcandidato,idbusqueda,idstatus from metricas where 1=1"
    if usuario != '':
        consulta = consulta + " and lower(trim(EmailAddres))=lower(trim('" + usuario + "'))"
    a.execute(consulta)
    results = a.fetchall()
    json_data = []
    for result in results:
        json_data.append([result[0], result[1], result[2], status(str(result[3]))])
    return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))

def encliente(usuario=''):
            db = connectar()
            a = db.cursor()
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
        db = connectar()
        a = db.cursor()
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


def pertenencia(usuario=''):
    db = connectar()
    a = db.cursor()
    consulta = """select str_to_date(informe ,'%Y-%m-%d' ) >= CURRENT_DATE - INTERVAL 30 DAY informe, 
                        str_to_date(reservado ,'%Y-%m-%d' ) >= CURRENT_DATE - INTERVAL 5 DAY reserva ,
                        EmailAddres 
                from metricas m where 
                (str_to_date(informe ,'%Y-%m-%d' ) >= CURRENT_DATE - INTERVAL 30 DAY
                or 
                str_to_date(reservado ,'%Y-%m-%d' ) >= CURRENT_DATE - INTERVAL 5 DAY
                ) """
    if usuario != '':
        consulta = consulta + " and emailcandidato='" + usuario + "'"
    a.execute(consulta)
    # row_headers = [x[0] for x in a.description]  # this will extract row headers
    results = a.fetchall()
    json_data = []
    # json_data.append(row_headers)
    pertenencia=0
    reserva=0
    valor=''
    for result in results:
        if result[0]!=0:
            pertenencia=1
        if result[1]!=0:
            reserva=1
        valor=result[2]
    if pertenencia==1:
        texto='El candidato tiene pertenencia con otro reclutador'
    if reserva==1:
        texto='El candidato esta reservado para otra reclutador'
        if pertenencia==1:
            texto=texto+ ' y ademas esta en pertencia con otro reclutador'
    if pertenencia==0 & reserva==0:
        return 'OK',valor
    return texto,valor
def metrica(usuario='',rol=''):
    db = connectar()
    a = db.cursor()
    consulta = "select * from metricas m  where 1=1  "
    if usuario != '' and rol != 'admin':
        consulta = consulta + " and EmailAddres='" + usuario + "'"
    a.execute(consulta)
    # row_headers = [x[0] for x in a.description]  # this will extract row headers
    results = a.fetchall()
    json_data = []
    # json_data.append(row_headers)
    for result in results:
        if result[11] is None:
            resultado=''
        else:
            resultado=result[11]
        json_data.append([ result[1], result[2], result[3], result[4], result[5],
                          result[6], result[7], result[8], result[9], result[10], str(resultado),
                           result[12], result[13], status(str(result[14])), result[15], result[16]
                           ])
    return json.loads(json.dumps(json_data).encode('utf-8').decode('ascii'))



def contratadosFun(usuario=''):
        db = connectar()
        a = db.cursor()
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
    db = connectar()
    a = db.cursor()
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
        db = connectar()
        a = db.cursor()
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


def insertinforme(idbusqueda,emailAddress,emailCandidato,cvEspInf,InfoEntrevista,CvIngles,InfoEntrevistaIngles):
        db = connectar()
        a = db.cursor()
        print("llegue")
        if cvEspInf is None:
            cvEspInf=''
        if InfoEntrevista is None:
            InfoEntrevista=''
        if CvIngles is None:
            CvIngles=''
        if InfoEntrevistaIngles is None:
            InfoEntrevistaIngles=''

        sql = "INSERT INTO conexion.cargaInforme (" \
              "idbusqueda, emailAddress, emailCandidato,cvespInf,cvingInf,informeesp,informeing)" \
              " VALUES ('"+idbusqueda+"', " \
              "'"+emailAddress+"', " \
              "'" +emailCandidato + "'," \
              "'" +cvEspInf + "'"+ "," \
              "'" +CvIngles + "'"+ "," \
              "'" +InfoEntrevista + "'"+ "," \
              "'" +InfoEntrevistaIngles + "'"\
              ") "

        a.execute(sql)
        conexion.commit()
        result='ok'
        return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))


def base64decomysql(idbusqueda, emailAddress, emailCandidato,campo):
    db = connectar()
    a = db.cursor()
    sql = "select REPLACE("+campo+" ,'data:application/pdf;base64,','') , cast(substr(cvespInf ,instr(cvespInf,'application/'),instr(cvespInf,'base64,')-7) AS CHAR(10000) CHARACTER SET utf8) content  from conexion.cargaInforme where " \
          " idbusqueda='"+idbusqueda+"'" \
         " and emailAddress='" + emailAddress + "'" \
        " and emailCandidato='" + emailCandidato + "'"
    a.execute(sql)
    results = a.fetchall()
    file=''
    for result in results:
        file=result[0]
        content=result[1]
    return file,content
def insertCliente(values):
    db = connectar()
    a = db.cursor()
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

    print(sql)
    a.execute(sql)
    a.commit()
    result = 'ok'
    return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))

def devolvercambiostado(emailCandi,id):
        db = connectar()
        a = db.cursor()
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
    db = connectar()
    a = db.cursor()
    consulta = "select count(*) ,role from users where trim(email)=trim('"+usuario+"') and trim(password)=trim('"+contrasena+"') group by role;"
    print(consulta)
    a.execute(consulta)
    results = a.fetchall()
    if len(results)>=1:
        return results[0][0],results[0][1]
    else:
        return 0,None

def insertEstado(emailCandi,idSt,emailSt,statusSt,comentarios=''):
    db = connectar()
    a = db.cursor()
    sql = "update cliente set idstatus='"+statusSt+"', " \
            "ComentariosInforme = '"+comentarios+"' " \
          "where emailcandidato='"+emailCandi+"' " \
          " and idBusqueda='"+idSt+"' " \
          " and EmailAddres='"+emailSt+"'"

    a.execute(sql)
    conexion.commit()
    result = 'ok'
    return json.loads(json.dumps(result).encode('utf-8').decode('ascii'))
def insertEstado11(emailCandi,idSt,emailSt,statusSt,salarioMensualAcordadoSt,fechaIngresoSt,comentariosSt):
    db = connectar()
    a = db.cursor()
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
    db = connectar()
    a = db.cursor()
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