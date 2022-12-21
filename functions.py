# all functions imported
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import threading
import pandas as pd
from mysql_cc import *

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('ultimo.json', scope)
client = gspread.authorize(credentials)
reservas = client.open('[AUT]PedidosReservas').worksheet('PedidosReservas')  # Open the spreadsheet
reservado=client.open('[EnProceso]EnConexionReservado').worksheet('EnProcesoEnConexionReservado')
SolicitudInforme=client.open('[EnProceso-Semi]PedidosInformes&InfARevisar').worksheet('EnProcesoSemiPedidosInformesyInfARevisar')
busquedasAbiertas=client.open('Maestro').worksheet('Busquedas')
UsersList=client.open('[Gestion]Accesos').worksheet('UsersList').get_all_values()
DirectosList=client.open('[Gestion]Accesos').worksheet('DirectosList').get_all_values()
contratados=client.open('[FueraDeProceso]Contratados').worksheet('FueraDeProcesoContratados').get_all_values()
contratadossheet=client.open('[FueraDeProceso]Contratados').worksheet('FueraDeProcesoContratados')
rechazados=client.open('[FueraDeProceso]ProcesoRechazado').worksheet('FueraDeProcesoProcesoRechazado')
#cambios=client.open('[AUT]PedidosCambios').worksheet('AUTPedidosCambios')


def jsonsheet():
    client = gspread.authorize(credentials)
    sheet4 = client.open('[EnProceso]EnCliente').worksheet('EnProcesoEnCliente')  # Open the spreadsheet
    data=sheet4.get_all_records()
    nuevo=[]
    for i in data:
        i['url']='<button>clau</button>'
        nuevo.append(i)
    return json.loads(json.dumps(nuevo).encode('utf-8').decode('ascii'))


def busquedas():
    busquedas = client.open('Maestro').worksheet('Busquedas')
    data=busquedas.get_all_values()
    return json.loads(json.dumps(data).encode('utf-8').decode('ascii'))

def permitidof(email):
    retorno=list(filter(None,map(lambda x:True if x[0].lower()==email.lower() else None,UsersList)))
    data=dict()
    if len(retorno)>0:
        if retorno[0]:
            data['permitido']=True
    retorno = list(filter(None,map(lambda x: True if str(x[0]).lower() == email.lower() else None, DirectosList)))
    if len(retorno)>0:
        if retorno[0]:
            data['permitido'] = True
    if len(data)==0:
        data['permitido']=False
    return data

def addReserva(values):
 data=reservado.get_all_records()#obtenemos los registros del excel
 try:
    email=values['emailCandidato']
    newDict = list(filter(lambda elem: elem['Email Candidato'] if str(elem['Email Candidato']).lower().strip()==str(email).lower().strip() else None, data))[0]
    contratado=list(filter(
        lambda elem: elem[2] if str(elem[2]).lower().strip() == str(email).lower().strip() else None,
        contratados))
    if len(contratado)>0:
        print(contratado)
        if contratado != '' or contratado is not None:
            return '403'
    print("asd")
    modificarReservar(values)
 except Exception as e:
    print(e)
    if '_' in values['idReserva']:
        for i in values['idReserva'].split('_'):
            newDict = {"datos": "vacio"}
            curDT = datetime.datetime.now()
            date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
            email = values['email']
            emailCandidato = str(values['emailCandidato']).lower()
            naCandi = values['naCandi']
            lkCandi = values['lkCandi']
            tecnologias = ",".join(values['tcandi'])
            tcandi = tecnologias
            tipoPerfil = ",".join(values['tperfil'])
            tperfil = tipoPerfil
            idReserva = i
            comment = values['comment']
            nuevo=values
            nuevo['idReserva']=i
            insertreserva(nuevo)
            reservas.append_row([date_time, email, emailCandidato, naCandi, lkCandi, tcandi, tperfil, idReserva, comment])
    else:
        newDict={"datos":"vacio"}
        curDT = datetime.datetime.now()
        date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
        email=values['email']
        emailCandidato=str(values['emailCandidato']).lower()
        naCandi=values['naCandi']
        lkCandi=values['lkCandi']
        tecnologias=",".join(values['tcandi'])
        tcandi=tecnologias
        tipoPerfil=",".join(values['tperfil'])
        tperfil=tipoPerfil
        idReserva=values['idReserva']
        comment=values['comment']
        insertreserva(values)
        reservas.append_row([date_time,email,emailCandidato,naCandi,lkCandi,tcandi,tperfil,idReserva,comment])

def addInforme(values):
      if 'conexion-hr.com' in values['EmailInf']:
          print(values)
          EsSource = values['EsSourceInf']
          Email = values['EmailInf']
          EMailCandidato = values['EMailCandidatoInf']
          NombreyApellidodelCandidato = values['NombreyApellidodelCandidatoInf']
          IdsaEnviar = values['IdsaEnviarInf']
          RemuneracionPretendidaMensual = values['RemuneracionPretendidaMensualInf']
          NiveldeIngles = "".join(values["NiveldeInglesInf"])
          Locacion = values["LocacionInf"]
          LKCandi = values['LKCandiInf']
          tecnologias=''
          if len(values['TecnoCandiInf']) > 1:
              tecnologias = ",".join(values['TecnoCandiInf'])
          else:
              if len(values['TecnoCandiInf']) == 1:
                  tecnologias = values['TecnoCandiInf'][0]
          TecnoCandi=''
          if tecnologias != None:
            TecnoCandi = tecnologias
          TecnoCandi = tecnologias
          tipoPerfil=''
          if values['TpCandiInf']:
              if len(values['TpCandiInf']) > 1:
                  tipoPerfil = ",".join(values['TpCandiInf'])
              else:
                  if len(values['TpCandiInf']) == 1:
                      tipoPerfil = values['TpCandiInf'][0]
          TpCandi = tipoPerfil
          comment = values['CommentInf']
          CvEspañol = ""  # values['CvEspanolInf']
          InfoEntrevista = values['informeEntEsp']
          CvIngles = ""  # values['CvInglesInf']
          InfoEntrevistaIngles = values['informeEntIng']
          curDT = datetime.datetime.now()
          date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
          values['StatusEnBaseInf']=13
          values['MotivvoRechazoInf']=''
          nuevaLista = []
          for x in DirectosList:
            nuevaLista.append(x[0])
          if Email in nuevaLista:
                revisarAprob(values)
          else: 
            insertinforme(IdsaEnviar,Email,EMailCandidato)
            SolicitudInforme.append_row([False,"", "","","",date_time,Email,
            EsSource, EMailCandidato, IdsaEnviar, TecnoCandi, TpCandi, LKCandi, comment,
            CvEspañol, InfoEntrevista, CvIngles, InfoEntrevistaIngles, RemuneracionPretendidaMensual,
            NiveldeIngles,Locacion[0],
            NombreyApellidodelCandidato, ""])
          """SolicitudInforme.append_row([False, "", "", "", "", date_time, Email,
                                       EsSource, EMailCandidato, IdsaEnviar, TecnoCandi, TpCandi, LKCandi, comment,
                                       CvEspañol, InfoEntrevista, CvIngles, InfoEntrevistaIngles,
                                       RemuneracionPretendidaMensual,
                                       NiveldeIngles, Locacion[0].replace("\n","").replace("\n","").replace("\n",""),
                                       NombreyApellidodelCandidato, ""])"""
      else:
        EsSource=values['EsSourceInf']
        Email= values['EmailInf']
        EMailCandidato = values['EMailCandidatoInf']
        NombreyApellidodelCandidato = values['NombreyApellidodelCandidatoInf']
        IdsaEnviar = values['IdsaEnviarInf']
        RemuneracionPretendidaMensual = values['RemuneracionPretendidaMensualInf']
        NiveldeIngles="".join(values["NiveldeInglesInf"])
        Locacion=values["LocacionInf"]
        LKCandi = values['LKCandiInf']
        tipoPerfil = ''
        tecnologias=''
        if len(values['TecnoCandiInf']) > 1:
            tecnologias = ",".join(values['TecnoCandiInf'])
        else:
            if len(values['TecnoCandiInf'])==1:
                tecnologias = values['TecnoCandiInf'][0]
        TecnoCandi = tecnologias
        if len(values['TpCandiInf'])>1:
            tipoPerfil = ",".join(values['TpCandiInf'])
        else:
            if len(values['TpCandiInf']) == 1:
                tipoPerfil=values['TpCandiInf'][0]
        TpCandi = tipoPerfil
        comment = values['CommentInf']
        CvEspañol= ""#values['CvEspanolInf']
        InfoEntrevista= values['informeEntEsp']
        CvIngles= ""#values['CvInglesInf']
        InfoEntrevistaIngles= values['informeEntIng']
        curDT = datetime.datetime.now()
        date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
        insertinforme(IdsaEnviar,Email,EMailCandidato)
        SolicitudInforme.append_row([False,"", "","","",date_time,Email,
         EsSource, EMailCandidato, IdsaEnviar, TecnoCandi, TpCandi, LKCandi, comment,
         CvEspañol, InfoEntrevista, CvIngles, InfoEntrevistaIngles, RemuneracionPretendidaMensual,
         NiveldeIngles,Locacion[0],
         NombreyApellidodelCandidato, ""])

def revisarAprob(values):
    StatusEnBase= values['StatusEnBaseInf']
    EsSource=values['EsSourceInf']
    Email= values['EmailInf']
    EMailCandidato = values['EMailCandidatoInf']
    NombreyApellidodelCandidato = values['NombreyApellidodelCandidatoInf']
    IdsaEnviar = values['IdsaEnviarInf']
    RemuneracionPretendidaMensual = values['RemuneracionPretendidaMensualInf']
    NiveldeIngles="".join(values["NiveldeInglesInf"])
    Locacion=values["LocacionInf"]
    LKCandi = values['LKCandiInf']
    tecnologias=''
    if len(values['TecnoCandiInf']) > 1:
        tecnologias = ",".join(values['TecnoCandiInf'])
    else:
        if len(values['TecnoCandiInf']) == 1:
            tecnologias = values['TecnoCandiInf'][0]
    TecnoCandi = tecnologias
    tipoPerfil=''
    if values['TpCandiInf']:
        if len(values['TpCandiInf']) > 1:
            tipoPerfil = ",".join(values['TpCandiInf'])
        else:
            if len(values['TpCandiInf']) == 1:
                tipoPerfil = values['TpCandiInf'][0]
    TpCandi = tipoPerfil
    comment = values['CommentInf']
    CvEspañol= ""#values['CvEspanolInf']
    InfoEntrevista= values['informeEntEsp']
    CvIngles= ""#values['CvInglesInf']
    InfoEntrevistaIngles= values['informeEntIng']
    MotivoRechazo= values['MotivvoRechazoInf']
    curDT = datetime.datetime.now()
    date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
    eliminar_guiones(EMailCandidato, IdsaEnviar, Email)
    ind = 1
    for i in SolicitudInforme.get_all_values():
        if i[6] == Email and i[8] == EMailCandidato and i[9] == IdsaEnviar:
            indice = ind
            SolicitudInforme.delete_row(ind)
        ind=ind+1
    insertCliente(values)
    if len(Locacion)>0:
        Locacion=Locacion[0]
    print(Locacion)
    SolicitudInforme.append_row([True,"", IdsaEnviar,"",StatusEnBase,date_time,Email,
    EsSource, EMailCandidato, IdsaEnviar, TecnoCandi, TpCandi, LKCandi, comment,
    CvEspañol, InfoEntrevista, CvIngles, InfoEntrevistaIngles, RemuneracionPretendidaMensual,
    NiveldeIngles,Locacion,
    NombreyApellidodelCandidato, MotivoRechazo])


    return  'ok'

def revisarRechaz(values):
    StatusEnBase= values['StatusEnBaseInf']
    EsSource=values['EsSourceInf']
    Email= values['EmailInf']
    EMailCandidato = values['EMailCandidatoInf']
    NombreyApellidodelCandidato = values['NombreyApellidodelCandidatoInf']
    IdsaEnviar = values['IdsaEnviarInf']
    RemuneracionPretendidaMensual = values['RemuneracionPretendidaMensualInf']
    NiveldeIngles="".join(values["NiveldeInglesInf"])
    Locacion=values["LocacionInf"]
    LKCandi = values['LKCandiInf']
    tecnologias = "".join(values['TecnoCandiInf'])
    TecnoCandi = tecnologias
    tipoPerfil = "".join(values['TpCandiInf'])
    TpCandi = tipoPerfil
    comment = values['CommentInf']
    CvEspañol= ""#values['CvEspanolInf']
    InfoEntrevista= values['informeEntEsp']
    CvIngles= ""#values['CvInglesInf']
    InfoEntrevistaIngles= values['informeEntIng']
    MotivoRechazo= values['MotivvoRechazoInf']
    curDT = datetime.datetime.now()
    date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
    eliminar_guiones(EMailCandidato, IdsaEnviar, Email)
    ind=1
    for i in SolicitudInforme.get_all_values():
        if i[6] == Email and i[8] == EMailCandidato and i[9] == IdsaEnviar:
            indice = ind
            SolicitudInforme.delete_row(ind)
        ind=ind+1
    insertEstado(EMailCandidato,IdsaEnviar,Email,'12')
    SolicitudInforme.append_row([True,"","" ,IdsaEnviar,StatusEnBase,date_time,Email,
    EsSource, EMailCandidato, IdsaEnviar, TecnoCandi, TpCandi, LKCandi, comment,
    CvEspañol, InfoEntrevista, CvIngles, InfoEntrevistaIngles, RemuneracionPretendidaMensual,
    NiveldeIngles,Locacion,
    NombreyApellidodelCandidato, MotivoRechazo])
    return  'Ok'

def jsonReservas():
    data=reservado.get_all_records()
    nuevo=[]
    for i in data:
        i['url']='<button>edit</button>'
        nuevo.append(i)
    return json.loads(json.dumps(nuevo).encode('utf-8').decode('ascii'))

def InformeRechazados():
    sheet4 = client.open('[FueraDeProceso]InformeRechazado').worksheet('FueraDeProcesoInformeRechazado')  # Open the spreadsheet
    data=sheet4.get_all_values()
    return json.loads(json.dumps(data).encode('utf-8').decode('ascii'))


def getInformesArevisar():
    algo=[]
    data=SolicitudInforme.get_all_values()
    data[0][1]="Fecha"
    data[0][0]="aprobado"
    numero=0
    for i in data:
        if numero == 0:
           # i.append("acciones")
            numero=1
        else:
          if i[4]!="Anclada":
                    i.append("""<button style="border:none; background-color: transparent;" id="aprobar"><img style="border-radius: 20px;" width="30px" src="https://img2.freepng.es/20180403/dtw/kisspng-computer-icons-check-mark-presentation-symbol-check-list-5ac41357e304a0.5127533215227994479299.jpg" alt=""></button>
                        <button style="border:none; background-color: transparent;" id="rechazar"> <img width="30px"  src="https://geoinn.com/wp-content/uploads/2018/08/010_x-3-512.png" alt=""></button>""")
                    algo.append(i)
    export=[]
    nn=0

    for i in algo:
        if '_' in i[9]:
            splitear = i[9].split("_")
            for j in splitear:
                print(j)
                export.append([i[4],i[5],
                i[6],i[7],i[8],j,i[10],
                i[11],i[12],i[13],i[14],
                i[15],i[16],i[17],i[18],
                i[19],i[20],i[21],i[22],
                i[23]])
        else:
            export.append([i[4],i[5],
                i[6],i[7],i[8],i[9],i[10],
                i[11],i[12],i[13],i[14],
                i[15],i[16],i[17],i[18],
                i[19],i[20],i[21],i[22],
                i[23]])
        print(i)
    return json.loads(json.dumps(export).encode('utf-8').decode('ascii'))



def devolverReserva(email):
    contratado = list(filter(
        lambda elem: elem[2] if str(elem[2]).lower().strip() == str(email).lower().strip() else None,
        contratados))
    if len(contratado) > 0:
        if contratado != '' or contratado is not None:
            return '502'
    else:
       data=reservado.get_all_records()#obtenemos los registros del excel
       try:
        newDict = list(filter(lambda elem: elem['Email Candidato'] if str(elem['Email Candidato']).lower()==str(email).lower() else None, data))[0]
       except:
           newDict={"datos":"vacio"}
       return json.loads(json.dumps(newDict).encode('utf-8').decode('ascii'))


def modificarReservar(values):
    if '_' in values['idReserva']:
        for i in values['idReserva'].split('_'):
            cell = reservado.find(str(values['emailCandidato']).lower(), case_sensitive=True)
            row = cell.row
            email = values['email']
            emailCandidato = str(values['emailCandidato']).lower()
            naCandi = values['naCandi']
            lkCandi = values['lkCandi']
            if len(values['tcandi']) > 1:
                tecnologias = ",".join(values['tcandi'])
            else:
                tecnologias = values['tcandi'][0]
            tcandi = tecnologias
            if len(values['tperfil']) > 1:
                tipoPerfil = ",".join(values['tperfil'])
            else:
                tipoPerfil = values['tperfil'][0]
            tperfil = tipoPerfil
            idReserva = i
            comment = values['comment']
            curDT = datetime.datetime.now()
            date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
            reservado.delete_row(row)
            reservado.add_rows(1)
            updateReserva(date_time, email, emailCandidato, naCandi, lkCandi, tcandi, tperfil, idReserva, comment)
            reservado.append_row([date_time, email, emailCandidato, naCandi, lkCandi, tcandi, tperfil, idReserva, comment,],
                                 index=row)
    else:
        cell = reservado.find(str(values['emailCandidato']).lower(), case_sensitive=True)
        row = cell.row
        email = values['email']
        emailCandidato = str(values['emailCandidato']).lower()
        naCandi = values['naCandi']
        lkCandi = values['lkCandi']
        if len(values['tcandi']) > 1:
            tecnologias = ",".join(values['tcandi'])
        else:
            tecnologias = values['tcandi'][0]
        tcandi = tecnologias
        if len(values['tperfil']) > 1:
            tipoPerfil = ",".join(values['tperfil'])
        else:
            tipoPerfil = values['tperfil'][0]
        tperfil = tipoPerfil
        idReserva = values['idReserva']
        comment = values['comment']
        curDT = datetime.datetime.now()
        date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
        reservado.delete_row(row)
        reservado.add_rows(1)
        updateReserva(date_time, email, emailCandidato, naCandi, lkCandi, tcandi, tperfil, idReserva, comment)
        reservado.append_row(
            [date_time, email, emailCandidato, naCandi, lkCandi, tcandi, tperfil, idReserva, comment, ],
            index=row)


def busquedasPrioritarias():
    #try:
      data = busquedasAbiertas.get_all_values()
      variable=[]
      for i in data:
          if i[0]=='ALTA':
            variable.append({'nube':i[0]+"-"+i[3]+"-"+i[4] })
      return json.loads(json.dumps(variable).encode('utf-8').decode('ascii'))

def eliminar_guiones(candidato,id,sourcer):
    datos=SolicitudInforme.get_all_records()
    n=2
    splite2=''
    for i in datos:
        if i['Dirección de correo electrónico']==sourcer \
            and str(id) in str(i['IDs a Enviar a Cliente separados con "_" y sin la palabra "ID" y sin espacios']) \
            and i['E-Mail Candidato']==candidato\
            and '_' in str(i['IDs a Enviar a Cliente separados con "_" y sin la palabra "ID" y sin espacios']):
            splite2=i['IDs a Enviar a Cliente separados con "_" y sin la palabra "ID" y sin espacios']
            eliminar=n


        n=n+1
    nuevo=[]
    if '_' in str(splite2):
        for i in splite2.split("_"):
            if i != id:
                print("DDDD")
                print(i)
                nuevo.append(str(i))
    if len(nuevo)>1:
        valores='_'.join(nuevo )
        SolicitudInforme.update('j'+str(eliminar),valores )

def modificarStatus(emailCandi,idSt,emailSt,statusSt):
    client = gspread.authorize(credentials)
    sheet4 = client.open('[EnProceso]EnCliente').worksheet('EnProcesoEnCliente')  # Open the spreadsheet
    data=sheet4.get_all_values()
    searchValues=[]
    ar = [{"rowIndex": i, "value": e} for i, e in enumerate(
        data) if e[2] == emailCandi  and e[0]== emailSt and e[3]==idSt]
    ar[0]['value'][19] = status(statusSt)
    if str(statusSt)=='4':
        ar[0]['value'][7]=datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    if str(statusSt)=='5':
        ar[0]['value'][8]=datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    if str(statusSt)=='6':
        ar[0]['value'][9]=datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    if str(statusSt)=='7':
        ar[0]['value'][11]=datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    if str(statusSt)=='8':
        ar[0]['value'][10]=datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    if str(statusSt)=='9':
        ar[0]['value'][12]=datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    if str(statusSt)=='10':
        ar[0]['value'][21]=datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    print(ar[0]['rowIndex'])
    sheet4.delete_row(ar[0]['rowIndex']+1)
    sheet4.append_row(ar[0]['value'])

def modificarStatus11(emailCandi,idSt,emailSt,statusSt,salarioMensualAcordadoSt,fechaIngresoSt,comentariosSt):
    client = gspread.authorize(credentials)
    sheet4 = client.open('[EnProceso]EnCliente').worksheet('EnProcesoEnCliente')  # Open the spreadsheet
    data = sheet4.get_all_values()
    searchValues = []
    ar = [{"rowIndex": i, "value": e} for i, e in enumerate(
        data) if e[2] == emailCandi and e[0] == emailSt and e[3] == idSt]
    if str(statusSt)=='11':
        sheet4.delete_row(ar[0]['rowIndex']+1)
        contratadossheet.add_rows(1)
        contratadossheet.append_row([datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
                               ar[0]['value'][0],
                               ar[0]['value'][2],
                               ar[0]['value'][3],
                               'Ingresó (Solo colocar este estado cuando el candidato entró a trabajar)',
                               comentariosSt,
                                '',
                                '',
                                '',
                                '',
                                '',
                                salarioMensualAcordadoSt,
                                '',
                                'CambioAc'
                               ''
                               ])

def modificarStatus12(emailCandi,idSt,emailSt,statusSt,salarioMensualOfrecidoClienteSt,salarioMensualPretendidoSt,motivoFinCandi,motivoFinCliente):
    client = gspread.authorize(credentials)
    sheet4 = client.open('[EnProceso]EnCliente').worksheet('EnProcesoEnCliente')  # Open the spreadsheet
    data = sheet4.get_all_values()
    searchValues = []
    ar = [{"rowIndex": i, "value": e} for i, e in enumerate(
        data) if e[2] == emailCandi and e[0] == emailSt and e[3] == idSt]
    if str(statusSt)=='11':
        sheet4.delete_row(ar[0]['rowIndex']+1)
        rechazados.add_rows(1)
        if motivoFinCandi != '' or motivoFinCandi.strip() is None:
            cancelado='Candidato'
        else:
            if motivoFinCliente != '' or motivoFinCliente.strip() is None:
                 cancelado='Cliente'
            else:
                cancelado='Conexion'

        rechazados.append_row([datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
                               ar[0]['value'][0],
                               ar[0]['value'][2],
                               ar[0]['value'][3],
                               'FueraDeProceso (Casos donde estamos 100% seguros que no va a haber contratacion). En la siguiente pregunta colocar el Motivo o SubEstado)',
                               '',
                                cancelado,
                                salarioMensualOfrecidoClienteSt,
                                salarioMensualPretendidoSt,
                                motivoFinCandi,
                                motivoFinCliente,
                                '',
                                '',
                                'CambioAc'
                               ])
