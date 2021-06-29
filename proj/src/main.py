from flask_restful import Api

from src.app import create_app
from src.views.users_views import Users, UsersList

app = create_app()

# API route
api = Api(app)
api.add_resource(UsersList, "/api/users/")
api.add_resource(Users, "/api/users/<int:id>/")
