from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import UniqueConstraint, ForeignKey
from flask_sqlalchemy import SQLAlchemy

from config import db

# Models
class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    day_scheduled = db.Column(db.String)
    time_scheduled = db.Column(db.Integer)
    course = db.Column(db.String)

    # Foreign Keys
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    tutee_id = db.Column(db.Integer, db.ForeignKey('tutees.id'))

    # Relationships
    tutor = db.relationship('Tutor', back_populates='sessions')
    tutee = db.relationship('Tutee', back_populates='sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'day_scheduled': self.day_scheduled,
            'time_scheduled': self.time_scheduled,
            'course': self.course,
            'tutor_id': self.tutor_id,
            'tutee_id': self.tutee_id,
            'tutor': {
                'id': self.tutor_id,
                'name': self.tutor.name,
                'certification_level': self.tutor.certification_level
            },
            'tutee': {
                'id': self.tutee_id,
                'name': self.tutee.name,
                'student_number': self.tutee.student_number
            }
        }

    __table_args__ = (
        UniqueConstraint('day_scheduled', 'time_scheduled', 'tutor_id', name='unique_date_time_tutor'),
    )

    def __repr__(self):
        return f'<Session {self.id}>'

class Tutor(db.Model, SerializerMixin):
    __tablename__ = 'tutors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    certification_level = db.Column(db.Integer)

    # Relationships
    courses = db.relationship('Course', back_populates='tutor', lazy=True)
    days_scheduled = db.relationship('ScheduledDay', back_populates='tutor', lazy=True)
    sessions = db.relationship('Session', back_populates='tutor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'certification_level': self.certification_level,
            'courses': [course.name for course in self.courses],
            'days_scheduled': [day.day for day in self.days_scheduled]
        }

    def __repr__(self):
        return f'<Tutor {self.id}: {self.name}>'

class ScheduledDay(db.Model):
    __tablename__ = 'scheduled_days'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)

    # Foreign Key
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))

    # Relationships
    tutor = db.relationship('Tutor', back_populates='days_scheduled', lazy=True)

    __table_args__ = (
        UniqueConstraint('day', 'tutor_id', name="unique_day_tutor"),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            'tutor': {
                'id': self.tutor.id,
                'name': self.tutor.name,
                'certification_level': self.tutor.certification_level
            }
        }

    def __repr__(self):
        return f'<Scheduled Day {self.id}: {self.day}>'

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Foreign Key
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))

    # Relationships
    tutor = db.relationship('Tutor', back_populates='courses', lazy=True)

    __table_args__ = (
        UniqueConstraint('name', 'tutor_id', name="unique_course_tutor"),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tutor': {
                'id': self.tutor.id,
                'name': self.tutor.name,
                'certification_level': self.tutor.certification_level
            }
        }

    def __repr__(self):
        return f'<Course {self.id}: {self.name}>'

class Tutee(db.Model, SerializerMixin):
    __tablename__ = 'tutees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    student_number = db.Column(db.Integer)

    # Relationships
    sessions = db.relationship('Session', back_populates='tutee', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'student_number': self.student_number,
            'sessions': [{
                'id': session.id,
                'day_scheduled': session.day_scheduled,
                'time_scheduled': session.time_scheduled,
                'tutor': session.tutor.name
            } for session in self.sessions]
        }

    def __repr__(self):
        return f'<Tutee {self.id}: {self.name}>'