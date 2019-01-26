from flask import Blueprint
from flask_restful import Api

from buyboxpredictor.api.resources import UserResource, UserList, PredictorResource


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)



api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(PredictorResource, '/predict')

@blueprint.route('/')
def index():
    return "Welcome to buyboxpredictor API. You need to login before you can use it.", 200