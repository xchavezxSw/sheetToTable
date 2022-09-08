# all functions imported
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import threading
import pandas as pd
from datetime import date

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('ultimo.json', scope)
client = gspread.authorize(credentials)
reservas = client.open('[AUT]PedidosReservas').worksheet('PedidosReservas')  # Open the spreadsheet
reservado=client.open('[EnProceso]EnConexionReservado').worksheet('EnProcesoEnConexionReservado')
SolicitudInforme=client.open('[EnProceso-Semi]PedidosInformes&InfARevisar').worksheet('EnProcesoSemiPedidosInformesyInfARevisar')
busquedasAbiertas=client.open('Maestro').worksheet('Busquedas')

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


def addReserva(values):
 data=reservado.get_all_records()#obtenemos los registros del excel
 try:
    email=values['emailCandidato']
    newDict = list(filter(lambda elem: elem['Email Candidato'] if str(elem['Email Candidato']).lower()==str(email).lower() else None, data))[0]
    modificarReservar(values)
 except Exception as e:
    print(e)
    newDict={"datos":"vacio"}
    curDT = datetime.now()
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
    reservas.append_row([date_time,email,emailCandidato,naCandi,lkCandi,tcandi,tperfil,idReserva,comment])

def addInforme(values):
        print(values)
        EsSource=values['EsSourceInf']
        Email= values['EmailInf']
        EMailCandidato = values['EMailCandidatoInf']
        NombreyApellidodelCandidato = values['NombreyApellidodelCandidatoInf']
        IdsaEnviar = values['IdsaEnviarInf']
        RemuneracionPretendidaMensual = values['RemuneracionPretendidaMensualInf']
        NiveldeIngles="".join(values["NiveldeInglesInf"])
        Locacion=values["LocacionInf"]
        LKCandi = values['LKCandiInf']
        tecnologias = ",".join(values['TecnoCandiInf'])
        TecnoCandi = tecnologias
        tipoPerfil = ",".join(values['TpCandiInf'])
        TpCandi = tipoPerfil
        comment = values['CommentInf']
        CvEspañol= ""#values['CvEspanolInf']
        InfoEntrevista= values['informeEntEsp']
        CvIngles= ""#values['CvInglesInf']
        InfoEntrevistaIngles= values['informeEntIng']
        curDT = datetime.now()
        date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
        SolicitudInforme.append_row([False,"", "","","",date_time,Email,
         EsSource, EMailCandidato, IdsaEnviar, TecnoCandi, TpCandi, LKCandi, comment,
         CvEspañol, InfoEntrevista, CvIngles, InfoEntrevistaIngles, RemuneracionPretendidaMensual,
         NiveldeIngles,Locacion[0],
         NombreyApellidodelCandidato, ""])

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
    for i in data:
        print(i)
        i.append(",<input type='checkbox'/>")
        algo.append(i)
    dataframe = pd.DataFrame(algo)
    return json.loads(json.dumps(algo).encode('utf-8').decode('ascii'))

def devolverReserva(email):
   data=reservado.get_all_records()#obtenemos los registros del excel
   try:
    newDict = list(filter(lambda elem: elem['Email Candidato'] if str(elem['Email Candidato']).lower()==str(email).lower() else None, data))[0]
   except:
       newDict={"datos":"vacio"}
   return json.loads(json.dumps(newDict).encode('utf-8').decode('ascii'))


def modificarReservar(values):
    cell = reservado.find(str(values['emailCandidato']).lower(), in_column=3)
    row = cell.row
    print(row)
    email = values['email']
    emailCandidato = str(values['emailCandidato']).lower()
    naCandi = values['naCandi']
    lkCandi = values['lkCandi']
    tecnologias = ",".join(values['tcandi'])
    tcandi = tecnologias
    tipoPerfil = ",".join(values['tperfil'])
    tperfil = tipoPerfil
    idReserva = values['idReserva']
    comment = values['comment']
    curDT = datetime.now()
    date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
    reservado.delete_row(row)
    reservado.insert_row([date_time, email, emailCandidato, naCandi, lkCandi, tcandi, tperfil, idReserva, comment],
                         index=row)

def busquedasPrioritarias():
    #try:
      data = busquedasAbiertas.get_all_values()
      variable=[]
      for i in data:
          if i[0]=='ALTA':
            variable.append({'nube':i[0]+"-"+i[3]+"-"+i[4] })
      return json.loads(json.dumps(variable).encode('utf-8').decode('ascii'))


