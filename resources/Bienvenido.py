from flask_restful import Resource


class Bienvenido(Resource):
    def get(self):
        return {'message': 'Hola!, acabas de hacer una peticion GET al API Rest de VoiceMail. Para más documentación acerca del proyecto, accede a https://github.com/Chemchu/VoiceMailAPI', 'successful': True}
