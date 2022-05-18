from __future__ import print_function

import json
from flask_cors import cross_origin

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def read(token):
    try:
        jsonToken = json.loads(token)
        print(jsonToken)

        # creds = Credentials(token=jsonToken["token"], refresh_token=jsonToken["refresh_token"], token_uri=jsonToken["token_uri"],
        #                     client_id=jsonToken["client_id"], client_secret=jsonToken["client_secret"], scopes=jsonToken["scopes"], expiry=jsonToken["expiry"])
        creds = Credentials.from_authorized_user_info(info=jsonToken)
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        print(f'An error occurred: {error}')
