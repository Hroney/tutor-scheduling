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
            "_index_": "Welcome to the Tutor Sign-up API",
            "sessions": "/sessions",
            "tutors": "/tutors",
            "tutees": "/tutees",
            "scheduled_days": "/scheduled_days",
            "courses": "/courses",
        }
        response = make_response(
            response_dict,
            200,
        )
        return response

class Sessions(Resource):
    def get(self):
        sessions = Session.query.all()
        session_dicts = [session.to_dict() for session in sessions]
        return session_dicts, 200
    
    def post(self):
        try:
            data = request.json
            required_fields = ['day_scheduled', 'time_scheduled', 'course', 'tutor_id', 'tutee_id']
            
            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field {field}'}, 400

            new_session = Session(
                day_scheduled=data['day_scheduled'],
                time_scheduled=data['time_scheduled'],
                course=data['course'],
                tutor_id=data['tutor_id'],
                tutee_id=data['tutee_id']
            )

            db.session.add(new_session)
            db.session.commit()

            return new_session.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred while processing the request: {e}'}, 500

    



class Tutors(Resource):
    def get(self):
        tutors = Tutor.query.all()
        tutor_dicts = [tutor.to_dict() for tutor in tutors]
        return tutor_dicts, 200
    
    def post(self):
        try:
            data = request.json
            required_fields = ['name', 'certification_level']

            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field {field}'}, 400

            existing_tutor = Tutor.query.filter_by(name=data['name']).first()
            if existing_tutor:
                return {'error': 'Tutor with the same name already exists'}, 400

            new_tutor = Tutor(
                name=data['name'],
                certification_level=data['certification_level']
            )

            db.session.add(new_tutor)
            db.session.commit()

            return new_tutor.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred while processing the request: {e}'}, 500

    

class Tutees(Resource):
    def get(self):
        tutees = Tutee.query.all()
        tutee_dicts = [tutee.to_dict() for tutee in tutees]
        return tutee_dicts, 200
    
    def post(self):
        data = request.json
        required_fields = ['name', 'student_number']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field {field}'}, 400
        new_tutee = Tutee(
            name=data.get('name'),
            student_number=data.get('student_number')
        )
        print(new_tutee.to_dict())
        db.session.add(new_tutee)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            existing_tutee = Tutee.query.filter_by(student_number=data['student_number']).first()
            if existing_tutee:
                return existing_tutee.to_dict(), 200
            else:
                return {'error': f'An error occurred while processing the request: {e}'}, 500
        return new_tutee.to_dict(), 201

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
        record = Tutee.query.filter_by(student_number=student_number).first()
        if record is None:
            return {'error': 'Tutee not found'}, 404
        response = make_response(
            record.to_dict(),
            200,
        )
        return response
    

class Scheduled_days(Resource):
    def get(self):
        response_dict_list = [s.to_dict() for s in ScheduledDay.query.all()]
        response = make_response(
            response_dict_list,
            200,
        )
        return response
    
    def post(self):
        try:
            data = request.json
            required_fields = ['day', 'tutor_id']

            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field {field}'}, 400
                
            new_day = ScheduledDay(
                day = data.get('day'),
                tutor_id = data.get('tutor_id')
            )

            db.session.add(new_day)
            db.session.commit()
            return new_day.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An {e} error occured while processing the request'}, 500


class Courses(Resource):

    def get(self):
        response_dict_list = [s.to_dict() for s in Course.query.all()]
        response = make_response(
            response_dict_list,
            200,
        )
        return response
    
    def post(self):
        try:
            data = request.json
            required_fields = ['name', 'tutor_id']

            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field {field}'}, 400
                
            new_course = Course(
                name = data.get('name'),
                tutor_id = data.get('tutor_id')
            )

            db.session.add(new_course)
            db.session.commit()
            return new_course.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An {e} error occured while processing the request'}, 500

api.add_resource(Index, '/')
api.add_resource(Sessions, '/sessions')
api.add_resource(Scheduled_days, '/scheduled_days')
api.add_resource(Courses, '/courses')
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

