# all functions imported
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('ultimo.json', scope)
client = gspread.authorize(credentials)
reservas = client.open('[AUT]PedidosReservas').worksheet('PedidosReservas')  # Open the spreadsheet
reservado=client.open('[EnProceso]EnConexionReservado').worksheet('EnProcesoEnConexionReservado')
def jsonsheet():
    client = gspread.authorize(credentials)
    sheet4 = client.open('[EnProceso]EnCliente').worksheet('EnProcesoEnCliente')  # Open the spreadsheet
    data=sheet4.get_all_records()
    nuevo=[]
    for i in data:
        i['url']='<button>clau</button>'
        nuevo.append(i)
    return json.loads(json.dumps(nuevo).encode('utf-8').decode('ascii'))

def addReserva(values):
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
    reservas.append_row([date_time,email,emailCandidato,naCandi,lkCandi,tcandi,tperfil,idReserva,comment])

def jsonReservas():
    data=reservado.get_all_records()
    nuevo=[]
    for i in data:
        i['url']='<button>edit</button>'
        nuevo.append(i)
    return json.loads(json.dumps(nuevo).encode('utf-8').decode('ascii'))
