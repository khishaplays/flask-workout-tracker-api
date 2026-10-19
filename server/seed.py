
from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():

    # Clear old records
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create exercises
    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    dumbbell_curls = Exercise(
        name="Dumbbell Curls",
        category="Strength",
        equipment_needed=True
    )

    db.session.add_all([
        pushups,
        squats,
        running,
        dumbbell_curls
    ])

    # Create workouts
    workout1 = Workout(
        date=date(2026, 10, 19),
        duration_minutes=45,
        notes="Upper body and leg workout"
    )

    workout2 = Workout(
        date=date(2026, 10, 18),
        duration_minutes=30,
        notes="Morning cardio session"
    )

    db.session.add_all([workout1, workout2])
    db.session.flush()

    # Connect exercises to workouts
    workout_exercise1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        reps=15,
        sets=3
    )

    workout_exercise2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=squats.id,
        reps=20,
        sets=3
    )

    workout_exercise3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=running.id,
        duration_seconds=1800
    )

    db.session.add_all([
        workout_exercise1,
        workout_exercise2,
        workout_exercise3
    ])

    db.session.commit()

    print("Database seeded successfully!")
    print("Exercises:", Exercise.query.count())
    print("Workouts:", Workout.query.count())
    print("Workout Exercises:", WorkoutExercise.query.count())
