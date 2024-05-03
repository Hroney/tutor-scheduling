import pytest
import json
from app import app, db, api
from models import Tutor, Tutee, Session, Course
from faker import Faker
import subprocess

fake = Faker()


# Cleans up the DB after test usage
@pytest.fixture(scope="session", autouse=True)
def seed_database():
    yield
    print("Seeding database...")
    subprocess.run(["python3", "../server/seed.py"])


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
            assert response['id']
            assert response['tutor_id'] == tutor.id
            assert response['tutee_id'] == tutee.id
            assert response['course'] == course.name

            session = Session.query.filter(
                Session.tutor_id == tutor.id, Session.tutee_id == tutee.id).one_or_none()
            assert session.time_scheduled == 10

    def test_tutors_get(self):
        with app.app_context():
            fake = Faker()
            for _ in range(10):
                tutor = Tutor(
                    name = fake.name(),
                    certification_level = fake.random_int(min = 1, max = 4)
                )
                db.session.add(tutor)
                db.session.commit()
            response = app.test_client().get('/tutors').json
            tutors = Tutor.query.all()
            assert [tutor['id'] for tutor in response] == [
                tutor.id for tutor in tutors
            ]
            assert [tutor['name'] for tutor in response] == [
                tutor.name for tutor in tutors
            ]
            assert [tutor['certification_level'] for tutor in response] == [
                tutor.certification_level for tutor in tutors
            ]
    
    def test_tutors_post(self):
        with app.app_context():
            fake = Faker()
            name = fake.name()
            cert_level = fake.random_int(min=1, max=4)
            response = app.test_client().post(
                '/tutors',
                json={
                    "name": name,
                    "certification_level": cert_level
                }
            ).json
            assert response['id']
            assert response['name'] == name
            assert response['certification_level'] == cert_level
    
    def test_tutees_get(self):
        with app.app_context():
            fake = Faker()
            random_suffix = fake.random_int(min=0, max=999999)
            student_number = f"4000{random_suffix:06d}"
            for _ in range(10):
                tutee = Tutee(
                    name = fake.name(),
                    student_number = student_number
                )
                db.session.add(tutee)
                db.session.commit()
            response = app.test_client().get('/tutees').json
            tutees = Tutee.query.all()
            assert [tutee['id'] for tutee in response] == [
                tutee.id for tutee in tutees
            ]
            assert [tutee['name'] for tutee in response] == [
                tutee.name for tutee in tutees
            ]
            assert [tutee['student_number'] for tutee in response] == [
                tutee.student_number for tutee in tutees
            ]
    
    def test_tutees_post(self):
        with app.app_context():
            fake = Faker()
            name = fake.name()
            random_suffix = fake.random_int(min=0, max=999999)
            student_number = int(f"4000{random_suffix:06d}")
            response = app.test_client().post(
                '/tutees',
                json={
                    "name": name,
                    "student_number": student_number
                }
            ).json


            assert response['id']
            assert response['name'] == name
            assert response['student_number'] == student_number