from __future__ import print_function
import base64
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json
from flask_cors import cross_origin

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def CreateService(token):
    try:
        jsonToken = json.loads(token)

        creds = Credentials.from_authorized_user_info(info=jsonToken)
        service = build('gmail', 'v1', credentials=creds)

        return service

    except HttpError as error:
        print(f'An error occurred: {error}')


def getMessage(token, message_id):
    service = CreateService(token)

    messages_dict = {}
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    # Get the message from its id
    txt = service.users().messages().get(userId="me", id=message_id,
                                         format="full", metadataHeaders=None).execute()
    try:
        in_reply_bool = False
        references_bool = False

        thread_id = txt['threadId']
        payload = txt['payload']
        headers = payload['headers']
        #print ('\nContenido de headers:', headers, '\n')

        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
            if d['name'] == 'In-Reply-To':
                in_reply_bool = True
                in_reply_to = d['value']
            if d['name'] == 'References':
                references_bool = True
                references = d['value']
            if d['name'] == 'Message-ID':
                message_id_to_reply = d['value']

        # Base 64 decoder
        parts = payload.get('parts')[0]
        #print ('\n-Parts:\n', parts)
        data = parts['body']['data']
        #print ('\n-Data:\n', data)
        data = data.replace("-", "+").replace("_", "/")
        decoded_data = base64.b64decode(data)

        # Parse with BeautifulSoup
        body = BeautifulSoup(decoded_data, "lxml").text
        body = body.rstrip()

        messages_dict[0] = {}
        messages_dict[0]['id'] = message_id
        #print ('ID del mensaje ', i, ': ', msg['id'])
        messages_dict[0]['threadId'] = thread_id

        if (in_reply_bool & references_bool):
            messages_dict[0]['in-reply-to'] = in_reply_to
            messages_dict[0]['references'] = references
        messages_dict[0]['message-id'] = message_id_to_reply
        try:
            messages_dict[0]['subject'] = subject
        except:
            messages_dict[0]['subject'] = ''
        #print ('Subject del mensaje ', i, ': ', subject)
        messages_dict[0]['from'] = sender
        #print ('Sender del mensaje ', i, ': ', sender)
        try:
            messages_dict[0]['message'] = body
        except:
            messages_dict[0]['message'] = ''

        i = i+1
    except:
        pass

    #print (messages_dict)
    return messages_dict


def getMessages(token, count):
    service = CreateService(token)

    i = 0
    if (count == None):
        count = 1000
    messages_dict = {}
    results = service.users().messages().list(userId='me').execute()

    messages = results.get('messages', [])
    for msg in messages:
        in_reply_bool = False
        references_bool = False
        if (i == count):
            break
        # Get the message from its id
        txt = service.users().messages().get(
            userId="me", id=msg['id'], format="full", metadataHeaders=None).execute()

        try:
            thread_id = txt['threadId']
            payload = txt['payload']
            headers = payload['headers']

            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
                if d['name'] == 'In-Reply-To':
                    in_reply_bool = True
                    in_reply_to = d['value']
                if d['name'] == 'References':
                    references_bool = True
                    references = d['value']
                if d['name'] == 'Message-ID':
                    message_id_to_reply = d['value']

            # Base 64 decoder
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            # Parse with BeautifulSoup
            body = BeautifulSoup(decoded_data, "lxml").text
            body = body.rstrip()

            messages_dict[i] = {}
            messages_dict[i]['id'] = msg['id']
            #print ('ID del mensaje ', i, ': ', msg['id'])
            messages_dict[i]['threadId'] = thread_id

            if (in_reply_bool & references_bool):
                messages_dict[i]['in-reply-to'] = in_reply_to
                messages_dict[i]['references'] = references
            messages_dict[i]['message-id'] = message_id_to_reply
            try:
                messages_dict[i]['subject'] = subject
            except:
                messages_dict[i]['subject'] = ''
            #print ('Subject del mensaje ', i, ': ', subject)
            messages_dict[i]['from'] = sender
            #print ('Sender del mensaje ', i, ': ', sender)
            try:
                messages_dict[i]['message'] = body
            except:
                messages_dict[i]['message'] = ''
            #print ('Body del mensaje ', i, ': ', body, '\n')

            i = i+1
        except Exception as e:
            # print(e)
            pass
    return messages_dict


def createEmail(token, to, subject, text):
    service = CreateService(token)

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    emailMsg = text
    message.attach(MIMEText(emailMsg, 'plain'))
    raw_msg = {'raw': (base64.urlsafe_b64encode(message.as_bytes()).decode())}

    sendEmail(service, raw_msg)


def createReply(token, message_id, text):
    service = CreateService(token)
    data = getMessage(message_id)
    message = MIMEText(text)

    destination = data[0]['from']
    destination = destination.split('<')[1]
    destination = destination.split('>')[0]
    message['to'] = destination

    message['subject'] = data[0]['subject']

    try:
        message.add_header('Reference', data[0]['references'])
        message.add_header('In-Reply-To', data[0]['in-reply-to'])
    except:
        message.add_header('Reference', data[0]['message-id'])
        message.add_header('In-Reply-To', data[0]['message-id'])

    raw_msg = {'raw': (base64.urlsafe_b64encode(message.as_bytes()).decode())}

    thread_id = data[0]['threadId']
    raw_msg['threadId'] = thread_id

    sendEmail(service, raw_msg)


def readEmail(token, message_id):
    service = CreateService(token)

    results = service.users().messages().list(userId='me').execute()
    service.users().messages().modify(userId='me', id=message_id,
                                      body={'removeLabelIds': ['UNREAD']}).execute()
    #print ('El mensaje con id', message_id, 'ha sido marcado como leído.')


def readAllUnreadEmails(token):
    service = CreateService(token)

    results = service.users().messages().list(
        userId='me', labelIds=['UNREAD']).execute()
    messages = results.get('messages', [])

    for msg in messages:
        service.users().messages().modify(userId='me', id=msg['id'], body={
            'removeLabelIds': ['UNREAD']}).execute()

    #print ('Todos los mensajes han sido marcados como leídos.')


def deleteEmail(token, message_id):
    service = CreateService(token)

    results = service.users().messages().delete(
        userId='me', id=message_id).execute()
    #print ('El mensaje ha sido eliminado con éxito.')


def createLabel(token, label_name):
    service = CreateService(token)

    label = {
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
        "name": label_name
    }
    results = service.users().labels().create(userId='me', body=label).execute()


def moveToLabel(token, message_id, label_name):
    service = CreateService(token)

    old_label = getMessageLabel(token, message_id)
    if 'IMPORTANT' in old_label:
        old_label.remove('IMPORTANT')
    if 'SENT' in old_label:
        old_label.remove('SENT')
    #print ('Labels del mensaje:', old_label)

    id_label = getLabelID(token, label_name)
    #print ('Label al que se va a mover el mensaje:', label_name, '(ID:', id_label, ')')

    if id_label not in old_label:
        new_label = {
            "removeLabelIds": [
                old_label[0]
            ],
            "addLabelIds": [
                id_label
            ],
        }
        result = service.users().messages().modify(
            userId='me', id=message_id, body=new_label).execute()
        #print ('Cambiada la etiqueta', old_label[0], 'a', label_name)
    # else:
        #print ('El mensaje', message_id, 'ya contiene la etiqueta', label_name)


def getMessageLabel(token, message_id):
    service = CreateService(token)

    result = service.users().messages().get(userId="me", id=message_id,
                                            format="full", metadataHeaders=None).execute()
    #print (result['labelIds'])
    return result['labelIds']


def getLabelID(token, label_name):
    service = CreateService(token)

    label_name = label_name.upper()
    results = service.users().labels().list(userId='me').execute()
    results = results['labels']
    aux = 0
    for i in results:
        if i['name'].upper() == label_name:
            id_label = results[aux]['id']
            break
        aux = aux + 1
    return id_label


def sendEmail(service, message):
    try:
        message = (service.users().messages().send(userId='me', body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    # except errors.HttpError, error:
    except ValueError:
        print('An error occurred: %s' % ValueError.__name__)
