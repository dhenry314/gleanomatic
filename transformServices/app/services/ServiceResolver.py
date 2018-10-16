from ..main import app, api
from flask_restful import Resource

class HelloWorld(Resource):
    def get(self):
        return {'howdy': 'world'}

api.add_resource(HelloWorld, '/')

