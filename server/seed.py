#!/usr/bin/env python3
import datetime
from app import app
from models import *

with app.app_context():
	# reset data and add new example data, committing to db 
    Exercise.query.delete()
    Workout.query.delete()
    WorkoutExercises.query.delete()

    db.session.commit()

    # Seed/Populate data
    ex1 = Exercise(name="push ups" , category="strength" , equipment_needed=False)
    ex2 = Exercise(name="weight lifting" , category="cardio" , equipment_needed=True)
    ex3 = Exercise(name="squats" , category="cardio" , equipment_needed=False)
    ex4 = Exercise(name="rope skipping" , category="flexibility" , equipment_needed=True)

    #workouts
    wo1 = Workout(date= datetime.datetime(2022, 5, 17) , duration_minutes= 5 , notes="fantastic! will try again")
    wo2 = Workout(date= datetime.datetime(2024, 9, 11) , duration_minutes= 15 , notes="fantastic! will try again")
    wo3 = Workout(date= datetime.datetime(2022, 12, 17) , duration_minutes= 5 , notes="fantastic! will try again")

    # Add workouts to exercises
    ex1.workouts.append(wo1)
    ex1.workouts.append(wo3)

    # Add exercises to workouts
    wo2.exercises.append(ex2)
    wo2.exercises.append(ex3)
    wo2.exercises.append(ex4)

    we1 = WorkoutExercises()
