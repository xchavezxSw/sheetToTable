# all functions imported
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import threading
import pandas as pd
from mysql_cc import *
from bd import conexion,connectar

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('ultimo.json', scope)
client = gspread.authorize(credentials)
sendmails = client.open('sendMailsEstado')

def sendmailstatus(result):

    #sendmails.add_rows(1)
    #sendmails.append_row([datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),emailSt,emailCandi,idSt,status(statusSt),comentarios,"","","","","","","","","","",0],table_range="A1")
    values=[]
    for i in result:
        values.append([datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),str(i[0]),str(i[1]),str(i[2]),"14","","","","","","","","","","","",str(0)])
    sendmails.values_append("mails!A1",{'valueInputOption': 'RAW'}, {'values': values})

def update2(EmailAddres,candi,id,estado,result):
        db = connectar()
        a = db.cursor()
        sql = " update reserva set status = '"+estado+"'  where EmailAddres = '"+EmailAddres+"' and emailcandidato='"+candi+"' and idreserva='"+id+"' "
        a.execute(sql)
        db.commit()
        updatec(EmailAddres, candi, id, estado,result)

def updatec(EmailAddres, candi, id, estado,result):
    db = connectar()
    a = db.cursor()
    sql = " update metricas set idstatus = '" + estado + "'  where EmailAddres = '" + EmailAddres + "' and emailcandidato='" + candi + "' and idbusqueda='" + id + "' "
    a.execute(sql)
    db.commit()




def update(usuario=''):
    db=connectar()
    a = db.cursor()
    consulta = """
            select r.EmailAddres ,r.emailcandidato ,r.idreserva ,r.status from reserva r left join 
            metricas  c on (c.EmailAddres =r.EmailAddres  
                          and c.idBusqueda =r.idreserva  
                          and c.emailcandidato =r.emailcandidato)
            where c.enviadocliente is null
            and c.entrevistanotecnicacliente is NULL 
            and c.entrevistatecnica is NULL 
            and c.onhold is NULL 
            and c.ejerciciotecnico is NULL 
            and c.oferta is NULL 
            and c.preoferta is null
            and c.tramiteingreso is null
            and c.contratado is null
            and c.informe is NULL 
            and c.rechazado is null
            and TIMESTAMPDIFF(HOUR, fecha, now()) >=96
            and r.status not in ('14')
 """
    a.execute(consulta)
    results = a.fetchall()
    for result in results:
         update2(result[0],result[1],str(result[2]),'14',result)
    sendmailstatus(results)

def update_onhold():
    db = connectar()
    cursor = db.cursor()
    consulta = """
            UPDATE cliente c
            SET idstatus = 12
            FROM metricas m 
            WHERE c.idstatus = 9 AND c.idbusqueda = m.idbusqueda AND c.EmailAddres = m.EmailAddres AND c.emailcandidato = m.emailcandidato
            AND m.onhold IS NOT NULL
            AND m.onhold != ""
            AND DATEDIFF(CURDATE(), m.onhold) > 30;
    """
    cursor.execute(consulta)
    cursor.commit()
    cursor.close()

#LLamada a Update
update()

#LLmada update_onhold
update_onhold()