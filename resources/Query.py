from pickle import TRUE
from flask import jsonify
from flask_cors import cross_origin
from flask_restful import Resource, request
from gmailAPIFunctions.gmailAPI import getMessages

from nltkFunctions.NLTKFunctions import NLTKFunctions


class Query(Resource):

    @cross_origin(supports_credentials=True)
    def get(self):
        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}

    @cross_origin(supports_credentials=True)
    def post(self):
        jsonRequest = request.json

        token = jsonRequest["token"]
        if token is None:
            return {'message': 'El token no puede estar vacio', 'successful': False}

        query = jsonRequest["query"]
        if query is None:
            return {'message': 'El query no puede estar vacio', 'successful': False}

        # Creando la clase encargada de las funciones en NLTK
        nltkF = NLTKFunctions()

        # Entender la petición
        intention = nltkF.GetRequestIntention(query)

        # Ejecutar lógica de nltk
        sentimiento = nltkF.GetSentimientoValue(query)

        print(sentimiento)

        # Hacer uso del API de Gmail
        getMessages(token=token, count=10)

        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}
