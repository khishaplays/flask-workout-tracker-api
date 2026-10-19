from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return {"message": "Welcome to Workout Tracker API"}, 200


# Get all workouts
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    result = WorkoutSchema(many=True).dump(workouts)

    return jsonify(result), 200


# Get one workout
@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(WorkoutSchema().dump(workout)), 200


# Create a workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        validated_data = WorkoutSchema().load(data)

        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(WorkoutSchema().dump(workout)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


# Delete a workout
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return "", 204

# Get all exercises
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    result = ExerciseSchema(many=True).dump(exercises)

    return jsonify(result), 200


# Get one exercise
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(ExerciseSchema().dump(exercise)), 200


# Create an exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        validated_data = ExerciseSchema().load(data)

        exercise = Exercise(**validated_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(ExerciseSchema().dump(exercise)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


# Delete an exercise
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return "", 204

# Add an exercise to a workout
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout or not exercise:
        return jsonify({"error": "Workout or exercise not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        # The IDs come from the URL, not the request body
        exercise_data = {
            "workout_id": workout_id,
            "exercise_id": exercise_id,
            "reps": data.get("reps"),
            "sets": data.get("sets"),
            "duration_seconds": data.get("duration_seconds")
        }

        validated_data = WorkoutExerciseSchema().load(exercise_data)

        workout_exercise = WorkoutExercise(**validated_data)

        db.session.add(workout_exercise)
        db.session.commit()

        result = WorkoutExerciseSchema().dump(workout_exercise)

        return jsonify(result), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
