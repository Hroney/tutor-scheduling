#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import db, Session, Tutor, Course, ScheduledDay, Tutee



# Views go here!
class Index(Resource):

    def get(self):
        response_dict = {
            "index": "Welcome to the Tutor Sign-up API",
        }
        response = make_response(
            response_dict,
            200,
        )
        return response


class Sessions(Resource):

    def get(self):
        response_dict_list = [s.to_dict() for s in Session.query.all()]
        response = make_response(
            response_dict_list,
            200,
        )
        return response


class Tutors(Resource):

    def get(self):
        response_dict_list = [t.to_dict() for t in Tutor.query.all()]
        response = make_response(
            response_dict_list,
            200,
        )
        return response


class Tutor_by_id(Resource):

    def get(self, id):
        response_dict = Tutor.query.filter_by(id=id).first().to_dict()
        response = make_response(
            response_dict,
            200,
        )
        return response

class Tutees(Resource):

    def get(self):
        response_dict_list = [t.to_dict() for t in Tutee.query.all()]
        response = make_response(
            response_dict_list,
            200,
        )
        return response

class Tutee_by_id(Resource):

    def get(self, id):
        response_dict = Tutee.query.filter_by(id=id).first().to_dict()
        response = make_response(
            response_dict,
            200,
        )
        return response

api.add_resource(Index, '/')
api.add_resource(Sessions, '/sessions')
api.add_resource(Tutors, '/tutors')
api.add_resource(Tutor_by_id, '/tutors/<int:id>')
api.add_resource(Tutees, '/tutees')
api.add_resource(Tutee_by_id, '/tutees/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

