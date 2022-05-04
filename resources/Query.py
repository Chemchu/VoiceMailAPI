from pickle import TRUE
from flask import jsonify
from flask_restful import Resource, request


class Query(Resource):
    def get(self):
        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}

    def post(self):
        jsonRequest = request.json
        print(jsonRequest["query"])
        print(jsonRequest["apiKey"])

        # Ejecutar lógica de nltk

        # Hacer uso del API de Gmail

        return {'message': 'Este es el endpoint encargado de recibir las querys y ejecutar los algoritmos PV mediante NLTK', 'successful': True}
