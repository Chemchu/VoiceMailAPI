from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources.Authenticate import Authenticate
from resources.Query import Query
from resources.Bienvenido import Bienvenido
import sys

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)
api = Api(app)

api.add_resource(Bienvenido, '/')
api.add_resource(Query, '/query')
api.add_resource(Authenticate, '/authenticate')

if __name__ == '__main__':
    app.run(debug=True)
    sys.setdefaultencoding('utf-8')
