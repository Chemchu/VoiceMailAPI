from pickle import TRUE
from flask import jsonify
from flask_cors import cross_origin
from flask_restful import Resource, request
from Utils.AppManager import AppManager
from gmailAPIFunctions.gmailAPI import createEmail, getMessages, sendEmail

from nltkFunctions.NLTKFunctions import NLTKFunctions


class Query(Resource):

    @cross_origin(supports_credentials=True)
    def get(self):
        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}

    @cross_origin(supports_credentials=True, allow_headers='*')
    def post(self):
        appManager = AppManager()
        nltkF = NLTKFunctions()
        jsonRequest = request.json

        token = jsonRequest["token"]
        if token is None:
            return {'message': 'El token no puede estar vacio', 'successful': False}

        query = jsonRequest["query"]
        if query is None:
            return {'message': 'El query no puede estar vacio', 'successful': False}

        steps = jsonRequest["steps"]
        intent = jsonRequest["intent"]
        if intent is None:
            # Entender la petición
            intention = nltkF.GetRequestIntention(query)
            response = appManager.IndentificarAccion(
                token=token, intent=intention, steps=[])
            return {'steps': [response], "intent": intention, 'successful': True}
        else:
            if steps is None:
                response = appManager.IndentificarAccion(
                    token=token, intent=intent, steps=[])
                return {'steps': [response], "intent": intent, 'successful': True}

            else:
                response = appManager.IndentificarAccion(
                    token=token, intent=intent, steps=steps)
                steps.append(response)
                return {'steps': steps, "intent": intent, 'successful': True}

        # # Creando la clase encargada de las funciones en NLTK
        # nltkF = NLTKFunctions()

        # # Ejecutar lógica de nltk
        # sentimiento = nltkF.GetSentimientoValue(query)

        # # Hacer uso del API de Gmail
        # getMessages(token=token, count=1)

        # return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}
