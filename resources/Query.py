from pickle import TRUE
from flask import jsonify
from flask_cors import cross_origin
from flask_restful import Resource, request
from gmailAPIFunctions.gmailAPI import createEmail, getMessages, sendEmail

from nltkFunctions.NLTKFunctions import NLTKFunctions


class Query(Resource):

    @cross_origin(supports_credentials=True)
    def get(self):
        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}

    @cross_origin(supports_credentials=True, allow_headers='*')
    def post(self):
        jsonRequest = request.json
        intention = None

        token = jsonRequest["token"]
        if token is None:
            return {'message': 'El token no puede estar vacio', 'successful': False}

        query = jsonRequest["query"]
        if query is None:
            return {'message': 'El query no puede estar vacio', 'successful': False}

        steps = jsonRequest["steps"]
        if steps is None:
            # Entender la petición
            intention = nltkF.GetRequestIntention(query)
        else:
            intention = None

        if intention is None:
            # Hacer logica aqui <-------------
            pass

        # Creando la clase encargada de las funciones en NLTK
        nltkF = NLTKFunctions()

        # Ejecutar lógica de nltk
        sentimiento = nltkF.GetSentimientoValue(query)

        print(sentimiento)

        # Hacer uso del API de Gmail
        getMessages(token=token, count=1)
        createEmail(token=token, subject="Probando",
                    text="Carlos sexy", to="gustavolee26@gmail.com")

        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}
