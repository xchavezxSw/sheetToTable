from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
import google.auth

SCOPES = ['https://mail.google.com/']


def login_mail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'clientmail.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def gmail_send_message(creds,to='',subject='',tipo='',candidato='',id='',sourcer='',estado='',reclutador=''):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        TemplateHtml=''
        TituloMail = ''
        info1 = ''
        info2 = ''
        comentarios = ''
        info3 = ''
        info4 = ''
        if tipo=='Reserva':
            TemplateHtml='Notif1.html'
            TituloMail = "Candidato Reservado con éxito";
            info1 = "El candidato que usted intento reservar es:   " +candidato
            info2 = "Por favor en caso de consultas ó aclaraciones sobre éste candidato responder éste mismo e-mail"
            info3 = "IDs:  "+id
            info4 = "";
        if tipo=='source':
            TemplateHtml='Notif1.html'
            TituloMail = "Tenes asignado un Candidato que fue cargado como sourcer";
            info1 = "Candidato asignado: " +candidato
            info2 = "Reclutador como Sourcer: "+sourcer
            info3 = "Los siguientes IDs fueron cargados: "+id
            info4 = "Podes ver el Pipeline para ver los detalles del Candidato.";
        if tipo=='sourcedest':
            TemplateHtml='Notif1.html'
            TituloMail = "Tu candidato fue asignado a un Reclutador y estarás como Sourcer";
            info1 = "Candidato asignado: " + candidato
            info2 = "No podrás cargar nuevos IDs en la Aplicación y en caso de encontrar que el candidato aplique a uno nuevo, deberas notificarlo por mail en este mismo hilo respondiendolo. Podrás ver el avance del candidato en el Pipeline."
            info3 = ""
            info4 = "";
        if tipo == 'estado':
            TemplateHtml = 'sendmail.html'
            TituloMail = "El candidato cambió de estado con éxito.";
            info1 = "El candidato que modificaste es:" + candidato
            info2 = "El email Reclutador que ingresaste es:" + reclutador
            info3 = "El estado actual ahora es:" + estado
            info4 = "El id actualizado es:" + id
        htmlText = []
        with open("FoldersHtml/"+TemplateHtml, encoding='utf8') as f:  # closes file after all the lines have been processed
            for line in f:  # not using readlines(), as this consumes the memory
                htmlText.append(line)
        final = ' '.join(htmlText)


        html=final.format(TituloMail,info1,info2,comentarios,info3,info4)

        message.set_content(html)
        message.set_type('text/html')
        message['To'] = to
        message['From'] = 'conexion@conexion.app'
        message['Subject'] = subject
        message['cc']="recruiting@conexion-hr.com"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message

