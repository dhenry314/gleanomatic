from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

from services import test

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
