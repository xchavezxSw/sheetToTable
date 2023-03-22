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

def gmail_send_message(creds,to='',subject='',tipo='',candidato='',id=''):
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
        if tipo=='Reserva':
            TemplateHtml='Notif1.html'
            TituloMail = "Candidato Reservado con éxito";
            Info1 = "El candidato que usted intento reservar es:   " +candidato
            Info2 = "Por favor en caso de consultas ó aclaraciones sobre éste candidato responder éste mismo e-mail"
            Info3 = "IDs:  "+id
            Info4 = "";

        htmlText = []
        with open("FoldersHtml/"+TemplateHtml, encoding='utf8') as f:  # closes file after all the lines have been processed
            for line in f:  # not using readlines(), as this consumes the memory
                htmlText.append(line)
        final = ' '.join(htmlText)
        TituloMail = ''
        info1=''
        info2=''
        comentarios = ''
        info3 = ''
        info4 = ''

        html=final.format(TituloMail,info1,info2,comentarios,info3,info4)

        message.set_content(html)
        message.set_type('text/html')
        message['To'] = to
        message['From'] = 'conexion@conexion.app'
        message['Subject'] = subject

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

if __name__ == '__main__':
    creds=login()
    gmail_send_message(creds,'claudio.x.pc@gmail.com','test')
