from flask_restful import Resource, request
from flask_cors import cross_origin
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://mail.google.com/']


class Authenticate(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        jsonRequest = request.json
        token = Autenticar(jsonRequest['token'])

        if token == None:
            return {'token': None, 'successful': False}

        return {'token': token, 'successful': True}


def Autenticar(token) -> Credentials:
    creds = None
    try:
        creds = Credentials.from_authorized_user_info(token, SCOPES)
        return creds.to_json()

    except:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            return creds.to_json()

    return None
