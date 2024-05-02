import pytest
import json
from app import app, db, api
from models import Tutor, Tutee, Session, Course
from faker import Faker


class TestApp:
    '''Flask application in app.py'''

    def test_index_get(self):
        '''retrieves the index'''

        with app.app_context():
            response = app.test_client().get('/')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert 'Welcome to the Tutor Sign-up API' in str(response.data)

    def test_sessions_get(self):
        '''Gets Sessions'''

        with app.app_context():
            tutor = Tutor(
                name = "TEST Tutor",
                certification_level = 4
            )
            tutee = Tutee(
                name = "TEST Tutee",
                student_number = 4000123456
            )
            course = Course(
                name = "Test_1",
                tutor_id = tutor.id
            )
            db.session.add_all([tutor, tutee, course])
            db.session.commit()

            session_1 = Session(
                course = "Math_test",
                day_scheduled = "Tuesday",
                time_scheduled = 9,
                tutor_id = tutor.id,
                tutee_id = tutee.id,
            )
            session_2 = Session(
                course = "Science_test",
                day_scheduled = "Monday",
                time_scheduled = 14,
                tutor_id = tutor.id,
                tutee_id = tutee.id,
            )
            db.session.add_all([session_1, session_2])
            db.session.commit()

            response = app.test_client().get('/sessions').json
            sessions = Session.query.all()
            
            assert [session['id'] for session in response] == [
                session.id for session in sessions
            ]
            assert [session['course'] for session in response] == [
                session.course for session in sessions
            ]
            assert [session['day_scheduled'] for session in response] == [
                session.day_scheduled for session in sessions
            ]

    def test_sessions_post(self):
        with app.app_context():
            tutor = Tutor(
                name = "Test Tutor",
                certification_level = 1
            )
            tutee = Tutee(
                name = "Test Tutee",
                student_number = 4000123456
            )
            course = Course(
                name = "Test_1",
                tutor_id = tutor.id
            )
            db.session.add_all([tutor, tutee, course])
            db.session.commit()

            response = app.test_client().post(
                '/sessions',
                json={
                    "day_scheduled": "Monday",
                    "time_scheduled": 10,
                    "course": course.name,
                    "tutor_id": tutor.id,
                    "tutee_id": tutee.id
                }
            ).json
            print(response)
            assert response['id']
            assert response['tutor_id'] == tutor.id
            assert response['tutee_id'] == tutee.id
            assert response['course'] == course.name

            session = Session.query.filter(
                Session.tutor_id == tutor.id, Session.tutee_id == tutee.id).one_or_none()
            assert session.time_scheduled == 10