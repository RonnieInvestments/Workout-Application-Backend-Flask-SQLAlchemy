from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define models here
class Exercise(db.Model):

    __tablename__="exercises"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    category=db.Column(db.String)
    equipment_needed=db.Column(db.Boolean)

    workout = db.relationship('Workout', secondary="workout_exercises", back_populates="exercises")

class Workout(db.Model):

    __tablename__="workout"

    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date)
    duration_minutes=db.Column(db.Integer)
    notes=db.Column(db.Text)

    exercise = db.relationship('Exercise', secondary="workout_exercises", back_populates="workout")

class WorkoutExercises(db.Model):

    __tablename__="workout_exercises"

    id=db.Column(db.Integer, primary_key=True)
    workout_id=db.Column(db.Integer) # foreign key to Workout
    exercise_id=db.Column(db.Integer) # foreign key to Exercise
    reps=db.Column(db.Integer)
    sets=db.Column(db.Integer)
    duration_seconds=db.Column(db.Integer)

    exercise = db.relationship('Exercise', back_populates= "workout_exercises")
    workout = db.relationship('Workout', back_populates= "workout_exercises")