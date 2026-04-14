from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from marshmallow import Schema, ValidationError, fields, validates_schema


from datetime import date
db = SQLAlchemy()

# Define models here
class Exercise(db.Model):

    __tablename__="exercises"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    category=db.Column(db.String)
    equipment_needed=db.Column(db.Boolean)

    workout_exercises = db.relationship("WorkoutExercises", back_populates="exercise")

    #validate category
    @validates("category")
    def validate_category(self, key, value):
        acceptedCategories = ["strength", "cardio", "flexibility"]

        if value not in acceptedCategories:
            return f"The category not found. The following are the accepted categories {acceptedCategories}"
        

    #validate name
    @validates("name")
    def validate_category(self, key, name):

        #check if it is not empty
        if not name:
            return f"The name cannot be empty"
        
        #check the length of the name
        if not 3 < len(name) < 20:
            return f"The number of characters should be between 3 and 20"
        
#create schema for exercise model
class ExerciseSchema(Schema):

    id = fields.Int(dump_only=True)
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()

    workouts = fields.Nested(lambda:WorkoutSchema(exclude=("exercises",)))

    @validates_schema('name','category','equipment_needed')
    def validate_duplicate_exercise(self, data, **kwargs):

        existing_exercise = Exercise.query.filter_by(

            name = data["name"],
            category = data["category"],
            equipment_needed =  data["equipment_needed"]

        ).first()

        if existing_exercise:
            raise ValidationError("Exercise already exists")

class Workout(db.Model):

    __tablename__="workout"

    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date)
    duration_minutes=db.Column(db.Integer)
    notes=db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercises", back_populates="workout")

    @validates("date")
    def validate_date(self, key, value):
        
        #Convert datetime -> date if needed
        if hasattr(value, "date"):
            value=value.date()
        
        #check if date is correct
        if value > date.today():
            raise ValueError("Date cannot be in future")
        
        return value

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        
        #check if the minutes are negative
        if value <= 0:
            raise("The duration must be positive")
        
#create schema for the workout model
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()

    exercises = fields.Nested(lambda:ExerciseSchema(exclude=("workouts",)))

    @validates_schema('date','duration_minutes','notes')
    def validate_duplicate_workout(self, data, **kwargs):
        existing_workout = Workout.query.filter_by(

            date = data["date"],
            duration_minutes = data["duration_minutes"],
            notes =  data["notes"]

        ).first()

        if existing_workout:
            raise ValidationError("Workout already exists")

class WorkoutExercises(db.Model):

    __tablename__="workout_exercises"

    id=db.Column(db.Integer, primary_key=True)
    
    workout_id=db.Column(db.Integer, db.ForeignKey("workout.id")) # foreign key to Workout
    exercise_id=db.Column(db.Integer, db.ForeignKey("exercises.id")) # foreign key to Exercise
    
    reps=db.Column(db.Integer)
    sets=db.Column(db.Integer)
    duration_seconds=db.Column(db.Integer)

    exercise = db.relationship("Exercise", back_populates= "workout_exercises")
    workout = db.relationship("Workout", back_populates= "workout_exercises")