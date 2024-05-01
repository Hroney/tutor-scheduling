#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from sqlalchemy.exc import IntegrityError

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Session, Tutor, Course, ScheduledDay, Tutee

fake = Faker()

def create_tutors():
    tutors = []
    for _ in range(10):
        t = Tutor(
            name=fake.name(),
            certification_level=fake.random_int(min=1, max=4)
        )
        tutors.append(t)
    return tutors

def create_tutees():
    tutees = []
    for _ in range(30):
        random_suffix = fake.random_int(min=0, max=999999)
        student_number = f"4000{random_suffix:06d}"
        t = Tutee(
            name = fake.name(),
            student_number = student_number
        )
        tutees.append(t)
    return tutees

course_list = ["math_1","math_2","math_3","math_4",
               "science_1","science_2","science_3","science_4",
               "english_1","english_2","english_3","english_4"
               ]

def create_courses(tutors):
    courses = []
    for tutor in tutors:
        try:
            for _ in range(len(course_list)):
                course_name = rc(course_list)

                c = Course(
                    name = course_name,
                    tutor_id = tutor.id
                )
                courses.append(c)
        except Exception as e:
            print(f"Course name and Tutor ID are not unique")
    return courses

day_list = ["Monday","Tuesday", "Wednesday","Thursday","Friday"]

def create_scheduled_days(tutors):
    scheduled_days = []
    for tutor in tutors:
        try:
            for _ in range(5):
                scheduled_day = rc(day_list)
                s = ScheduledDay(
                    day = scheduled_day,
                    tutor_id = tutor.id
                )
                scheduled_days.append(s)
        except Exception as e:
            print(f"Tutor is already scheduled for that day.")
    return scheduled_days


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Clearing db...")
        Session.query.delete()
        Tutor.query.delete()
        Course.query.delete()
        ScheduledDay.query.delete()
        Tutee.query.delete()

        print("Seeding Tutors...")
        tutors = create_tutors()
        db.session.add_all(tutors)
        db.session.commit()

        print("Seeding Tutees...")
        tutees = create_tutees()
        db.session.add_all(tutees)
        db.session.commit()

        print("Seeding Courses...")
        courses = create_courses(tutors)
        for course in courses:
            db.session.add(course)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()

        print("Seeding ScheduledDays...")
        scheduled_days = create_scheduled_days(tutors)
        for day in scheduled_days:
            db.session.add(day)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()

        print("Done Seeding!")
        # sessions = create_sessions()
        # Seed code goes here!
