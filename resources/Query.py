from pickle import TRUE
from flask import jsonify
from flask_restful import Resource, request

from nltkFunctions.analizadorSentimientos import NLTKFunctions


class Query(Resource):
    def get(self):
        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}

    def post(self):
        jsonRequest = request.json

        apiKey = jsonRequest["apiKey"]
        if apiKey is None:
            return {'message': 'El APIKey no puede estar vacio', 'successful': False}

        userQuery = jsonRequest["userQuery"]
        if userQuery is None:
            return {'message': 'El UserQuery no puede estar vacio', 'successful': False}

        # Entender la petición

        # Ejecutar lógica de nltk
        nltkF = NLTKFunctions()
        sentimiento = nltkF.GetSentimientoValue(
            "Qué felicidad! Te quiero, eres muy divertido")

        print(sentimiento)

        # Hacer uso del API de Gmail

        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}
