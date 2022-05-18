from pickle import TRUE
from flask import jsonify
from flask_cors import cross_origin
from flask_restful import Resource, request
from gmailAPIFunctions.read import read

from nltkFunctions.analizadorSentimientos import NLTKFunctions


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

        # Entender la petición

        # Ejecutar lógica de nltk
        nltkF = NLTKFunctions()
        sentimiento = nltkF.GetSentimientoValue(
            "Qué felicidad! Te quiero, eres muy divertido")

        print(sentimiento)

        # Hacer uso del API de Gmail
        # read(token)

        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}
