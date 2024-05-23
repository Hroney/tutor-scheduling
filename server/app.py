#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api
# Add your model imports
from models import db, Session, Tutor, Course, ScheduledDay, Tutee

# Views go here!
class Index(Resource):

    def get(self):
        response_dict = {
            "index": "Welcome to the Tutor Sign-up API",
            "sessions": "/sessions",
            "tutors": "/tutors",
            "tutees": "/tutees",
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
    
    def post(self):
        try:
            data = request.json
            required_fields = ['day_scheduled', 'time_scheduled', 'course', 'tutor_id', 'tutee_id']
            
            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field {field}'}, 400

            day = data.get('day_scheduled')
            time = data.get('time_scheduled')
            course = data.get('course')
            tutor = data.get('tutor_id')
            tutee = data.get('tutee_id')

            new_session = Session(
                day_scheduled = day,
                time_scheduled = time,
                course = course,
                tutor_id = tutor,
                tutee_id = tutee
            )

            db.session.add(new_session)
            db.session.commit()

            return new_session.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error {e} occurred while processing the request'}, 500
    



class Tutors(Resource):

    def get(self):
        response_dict_list = [t.to_dict() for t in Tutor.query.all()]
        for t in response_dict_list:
            t_id = t['id']
            t.update({"tutor": f"/tutors/{t_id}"})
        response = make_response(
            response_dict_list,
            200,
        )
        
        return response
    
    def post(self):
        try:
            data = request.json
            required_fields = ['name', 'certification_level']

            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field {field}'}, 400
                
            new_tutor = Tutor(
                name = data.get('name'),
                certification_level = data.get('certification_level')
            )

            db.session.add(new_tutor)
            db.session.commit()
            return new_tutor.to_dict(), 201
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Tutor with the same name already exists'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': 'An error occured while processing the request'}, 500
    

class Tutees(Resource):

    def get(self):
        response_dict_list = [t.to_dict() for t in Tutee.query.all()]
        for t in response_dict_list:
            t_id = t['id']
            t.update({"tutee": f"/tutees/{t_id}"})
        response = make_response(
            response_dict_list,
            200,
        )
        return response
    
    def post(self):
        try:
            data = request.json
            required_fields = ['name', 'student_number']

            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field {field}'}, 400
                
            new_tutee = Tutee(
                name = data.get('name'),
                student_number = data.get('student_number')
            )

            db.session.add(new_tutee)
            db.session.commit()
            return new_tutee.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An {e} error occured while processing the request'}, 500


# relational views




class Sessions_by_id(Resource):

    def get(self, id):
        response_dict = Session.query.filter_by(id=id).first().to_dict()
        response = make_response(
            response_dict,
            200,
        )
        return response
    
    def patch(self, id):
        try:
            record = Session.query.filter_by(id=id).first()
            for attr in request.json:
                setattr(record, attr, request.json[attr])
            db.session.add(record)
            db.session.commit()

            return record.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error {e} occurred while processing the request'}, 500
        
    def delete(self, id):
        record = Session.query.filter_by(id=id).first()
        if not record:
            return {'error': 'Record not found'}, 404
        db.session.delete(record)
        db.session.commit()
        return {"message": "record successfully deleted"}, 200

class Tutor_by_id(Resource):

    def get(self, id):
        response_dict = Tutor.query.filter_by(id=id).first().to_dict()
        response_dict.update({"sessions": f"/tutors/{response_dict['id']}/sessions"})        
        response = make_response(
            response_dict,
            200,
        )
        return response
    
    def delete(self, id):
        record = Tutor.query.filter_by(id=id).first()
        if not record:
            return {'error': 'Record not found'}, 404
        db.session.delete(record)
        db.session.commit()
        return {"message": "record successfully deleted"}, 200   

    def patch(self, id):
        try:
            record = Tutor.query.filter_by(id=id).first()
            for attr in request.json:
                setattr(record, attr, request.json[attr])
            db.session.add(record)
            db.session.commit()

            return record.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error {e} occurred while processing the request'}, 500 


class Tutors_sessions(Resource):

    def get(self, id):
        response_dict_list = [s.to_dict() for s in Session.query.filter_by(tutor_id=id).all()]
        response = make_response(
            response_dict_list,
            200,
        )
        return response
    
class Tutee_by_id(Resource):

    def get(self, id):
        response_dict = Tutee.query.filter_by(id=id).first().to_dict()
        response_dict.update({"sessions": f"/tutees/{response_dict['id']}/sessions"}) 
        response = make_response(
            response_dict,
            200,
        )
        return response
    
    def delete(self, id):
        record = Tutee.query.filter_by(id=id).first()
        if not record:
            return {'error': 'Record not found'}, 404
        db.session.delete(record)
        db.session.commit()
        return {"message": "record successfully deleted"}, 200   
    
    def patch(self, id):
        try:
            record = Tutee.query.filter_by(id=id).first()
            for attr in request.json:
                setattr(record, attr, request.json[attr])
            db.session.add(record)
            db.session.commit()

            return record.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error {e} occurred while processing the request'}, 500     
    
class Tutees_sessions(Resource):

    def get(self, id):
        response_dict_list = [s.to_dict() for s in Session.query.filter_by(tutee_id=id).all()]
        response = make_response(
            response_dict_list,
            200,
        )
        return response

class Tutees_id_number_check(Resource):
    def get(self, student_number):
        record = Tutee.query.filter_by(student_number = student_number).first()
        print(record)
        response = make_response(
            record.to_dict(),
            200,
        )
        return response

api.add_resource(Index, '/')
api.add_resource(Sessions, '/sessions')
api.add_resource(Sessions_by_id, '/sessions/<int:id>')
api.add_resource(Tutors, '/tutors')
api.add_resource(Tutees, '/tutees')
api.add_resource(Tutor_by_id, '/tutors/<int:id>')
api.add_resource(Tutors_sessions, '/tutors/<int:id>/sessions')
api.add_resource(Tutee_by_id, '/tutees/<int:id>')
api.add_resource(Tutees_sessions, '/tutees/<int:id>/sessions')
api.add_resource(Tutees_id_number_check, '/tutees/<int:student_number>/student_number')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

