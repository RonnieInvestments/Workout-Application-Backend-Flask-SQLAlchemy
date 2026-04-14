from flask import Flask, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route("/", methods=["GET"])
def index():
    body = {"message": "Welcome to our workout platform!"}
    make_response(body,200)

# CRUD Operations
# Read Workout Resources
@app.route("/workouts", methods=["GET"])
def get_all_workouts():
    workouts = []

    for workout in Workout.query.all():
        workout_dict = {
            "id": workout.id,
            "date": workout.date,
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }

        workouts.append(workout_dict)
    
    body = {
        "workouts": workouts
    }

    return make_response(body, 200)

# Read a specific /workouts resource -> using id
@app.route("/workouts/<id>", methods=["GET"])
def get_workout(id):

    workout = Workout.query.filter_by(id=id).first()

    if workout:
        body = {
            "id": workout.id,
            "date": workout.date,
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }
        status = 200
        return make_response(body, status)
    else:
        return make_response({"error": f"Workout with id {id} not found."}, 404)
    
# CREATE a /workouts resource
@app.route("/workouts", methods=["POST"])
def create_workout():
    data =[]

    #New_workout from incoming data
    new_workout = Workout(
        date=data["date"], 
        duration_minutes=data["duration_minutes"], 
        notes= data["notes"]
    )
    #Try to add and commit new data to the db
    try: 
        db.session.add(new_workout)
        db.session.commit()

        body = {
            "message": "New workout added successfully into database."
        }
        return make_response(body, 201)

    except Exception as e:
        body = {
            "error": f"There was an error inserting into the database {e}"
        }
        return make_response(body, 404)
    
# DELETE a /workouts resource
@app.route("/workouts/<id>", methods=["DELETE"])
def delete_workout(id):
    
    #Look for workout in the database
    workout = Workout.query.filter_by(id=id).first()

    #Check if workout with a specific id does not exist in the database
    if not workout:
        return make_response({{"error": f"Workout with id:{id} not found"}, 404})
    
    #If the workout exists in the database
    try:
        db.session.delete(workout)
        db.session.commit()

        return make_response(
            {
            "message": f"Workout deleted successfully",
            "workout": {}
            }, 200
        )
    except Exception as e:
        return make_response({"error": f"Could not delete workout: {e}"},404)

#CRUD operations to /exercises resource
# READ /exercises resource
@app.route("/exercises", methods=["GET"])
def get_all_exercises():
    exercises = []

    for exercise in Exercise.query.all():
        exercise_dict = {
            "id": exercise.id,
            "name": exercise.id,
            "category": exercise.category,
            "notes": exercise.notes
        }
        exercises.append(exercise_dict)
    
    body = {
        "exercises": exercises
    }

    return make_response(body, 200)

# READ a specific /exercises resource
@app.route("/exercises/<id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()

    if exercise:
        body = {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        }
        status = 200
        return make_response(body, status)
    else:
        return make_response({"error": f"Exercise of id {id} not found."}, 404)
    
# CREATE a /exercises resource
@app.route("/exercises", methods=["POST"])
def create_exercise():
    #extract data
    data = []

    #Instance of new_workout from incoming data
    new_exercise = Workout(
        name=data["name"], 
        category=data["category"], 
        equipment_needed= data["equipment_needed"]
    )

    try: 
        db.session.add(new_exercise)
        db.session.commit()

        body = {
            "msg": "a new exercise has been added successfully into database"
        }
        return make_response(body, 201)

    except Exception as e:
        body = {
            "error": f"There was an error inserting into the database {e}"
        }
        return make_response(body, 404)

# DELETE a /exercises resource
@app.route("/exercises/<id>", methods=["DELETE"])
def delete_exercise(id):
    # Check for existence in the database
    exercise = Exercise.query.filter_by(id=id).first()

    # Logic to handle an exercise that does not exist
    if not exercise:
        return make_response({{"error": f"Exercise id:{id} not found"}, 404})
    
    # If the exercise exists proceed
    try:
        db.session.delete(exercise)
        db.session.commit()

        return make_response(
            {
            "message": f"Exercise deleted successfully!",
            "exercise": {}
            }, 200
        )
    except Exception as e:
        return make_response({"error": f"Could not delete exercise: {e}"},404)

@app.route("/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises", methods=["DELETE"])
def delete_exercise(workout_id, exercise_id):
    # Look for the workout_exercise in the database
    workout_exercise = WorkoutExercises.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    # Check if it does not exist
    if not workout_exercise:
        return make_response(
            {"error": f"Exercise with id:{exercise_id} not found in workout:{workout_id}"}, 
            404
        )
    
    # If it exists
    try:
        db.session.delete(workout_exercise)
        db.session.commit()

        return make_response(
            {
                "message": "Exercise removed from workout successfully",
                "workout_exercise": {}
            }, 
            200
        )
    except Exception as e:
        return make_response(
            {"error": f"Could not delete exercise from workout: {e}"}, 
            404
        )


if __name__ == '__main__':
    app.run(port=5555, debug=True)