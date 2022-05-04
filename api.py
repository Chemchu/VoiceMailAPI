from flask import Flask
from flask_restful import Api
from resources.Query import Query
from resources.Bienvenido import Bienvenido
import sys

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

api.add_resource(Bienvenido, '/')
api.add_resource(Query, '/query')

if __name__ == '__main__':
    app.run(debug=True)
    sys.setdefaultencoding('utf-8')
