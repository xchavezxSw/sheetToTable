# all functions imported
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import threading

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
 except:
    newDict={"datos":"vacio"}
    curDT = datetime.now()
    date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
    email=values['email']
    emailCandidato=values['emailCandidato']
    naCandi=values['naCandi']
    lkCandi=values['lkCandi']
    tecnologias=",".join(values['tcandi'])
    tcandi=tecnologias
    tipoPerfil=",".join(values['tperfil'])
    tperfil=tipoPerfil
    idReserva=values['idReserva']
    comment=values['comment']
    #reservas.append_row([date_time,email,emailCandidato,naCandi,lkCandi,tcandi,tperfil,idReserva,comment])

def addInforme(values):
        EsSource=values['EsSource']
        Email= values['Email']
        EMailCandidato = values['EMailCandidato']
        NombreyApellidodelCandidato = values['NombreyApellidodelCandidato']
        IdsaEnviar = values['IdsaEnviar']
        RemuneracionPretendidaMensual = values['RemuneracionPretendidaMensual']
        NiveldeIngles=values["NiveldeIngles"]
        Locacion=values["Locacion"]
        LKCandi = values['LKCandi']
        tecnologias = ",".join(values['TecnoCandi'])
        TecnoCandi = tecnologias
        tipoPerfil = ",".join(values['TpCandi'])
        TpCandi = tipoPerfil
        comment = values['Comment']
        #SolicitudInforme.append_row(["","","","","","", Direccióndecorreoelectrónico,
        # EsSource, EmailCandidato, IdsaEnviar, TecnoCandi, TpCandi, Likedin, Commentario,
        # CvEspañol, InfoEntrevista, CvIngles, InfoEntrevistaIngles, RemuneracionPretendidaMensual,
        # NombreyApellidodelCandidato, MotivoRechazo])

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

def devolverReserva(email):
   data=reservado.get_all_records()#obtenemos los registros del excel
   try:
    newDict = list(filter(lambda elem: elem['Email Candidato'] if str(elem['Email Candidato']).lower()==str(email).lower() else None, data))[0]
   except:
       newDict={"datos":"vacio"}
   return json.loads(json.dumps(newDict).encode('utf-8').decode('ascii'))


def modificarReservar(values):
    cell = reservado.find(values['emailCandidato'], in_column=3)
    row = cell.row
    email = values['email']
    emailCandidato = values['emailCandidato']
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
         #with open('busquedas.txt') as f:
          #      lines = f.readlines()
           # download_thread = threading.Thread(target=busquedasPrioritariasFile, name="Downloader")
            #download_thread.start()
       # except:
          #  download_thread = threading.Thread(target=busquedasPrioritariasFile, name="Downloader")
           # download_thread.start()
      return json.loads(json.dumps(variable).encode('utf-8').decode('ascii'))


#def busquedasPrioritariasFile():
#    data = busquedasAbiertas.get_all_values()
#    newDict = list(filter(lambda elem: elem[3] if str(elem[0]).lower() == str("ALTA").lower() else None, data))
#    with open('busquedas.txt', 'w') as f:
#        for i in newDict:
#            f.write(str(i))
print(busquedasPrioritarias())