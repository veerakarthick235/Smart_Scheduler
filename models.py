# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for the many-to-many relationship between Faculty and Subjects
faculty_subject_association = db.Table('faculty_subject',
    db.Column('faculty_id', db.Integer, db.ForeignKey('faculty.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # In production, hash passwords!
    role = db.Column(db.String(50), nullable=False, default='editor') # e.g., 'admin', 'editor'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # The 'subjects' relationship will link a faculty to the subjects they can teach
    subjects = db.relationship('Subject', secondary=faculty_subject_association, back_populates='faculties')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    hours_per_week = db.Column(db.Integer, nullable=False)
    # The 'faculties' relationship links a subject back to the faculty who can teach it
    faculties = db.relationship('Faculty', secondary=faculty_subject_association, back_populates='subjects')

# This could be another model if you want to assign subjects to batches dynamically
# For now, we assume all subjects are for all batches for simplicity in the algorithm