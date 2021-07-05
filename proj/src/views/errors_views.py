from flask_restful import Resource


class Errors(Resource):
    def get(self):
        return "Oups!!! Somsing going wrong :(((((((((((((", 404


class Done(Resource):
    def get(self):
        return "You are welkome", 404
