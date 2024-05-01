from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy

from config import db


# Models go here!
class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    date_scheduled = db.Column(db.Date)
    time_scheduled = db.Column(db.Time)
    course = db.Column(db.String)

    # Relationships
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    tutee_id = db.Column(db.Integer, db.ForeignKey('tutees.id'))

    __table_args__ = (
        UniqueConstraint('date_scheduled', 'time_scheduled', 'tutor_id', name='unique_date_time_tutor'),
    )
    def __repr__(self):
        return f'<Session {self.id}>'

class Tutor(db.Model, SerializerMixin):
    __tablename__ = 'tutors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    certification_level = db.Column(db.String)

    # Relationships
    courses = db.relationship('Course', backref='tutors', lazy=True)
    days_scheduled = db.relationship('ScheduledDay', backref='tutor', lazy=True)

    def __repr__(self):
        return f'<Tutor {self.id}: {self.name}>'

class ScheduledDay(db.Model):
    __tablename__ = 'scheduled_days'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)

    # Relationships
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    
    #validation/constraints
    __table_args__ = (
        UniqueConstraint('day', 'tutor_id', name="unique_day_tutor"),
    )

    def __repr__(self):
        return f'<Scheduled Day {self.id}: {self.day}>'
    
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationships
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))

    def __repr__(self):
        return f'<Course {self.id}: {self.name}>'
    
class Tutee(db.Model, SerializerMixin):
    __tablename__ = 'tutees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    student_number = db.Column(db.Integer)

    # Relationships
    sessions = db.relationship('Session', backref='tutees', lazy=True)

    def __repr__(self):
        return f'<Tutee {self.id}: {self.name}>'