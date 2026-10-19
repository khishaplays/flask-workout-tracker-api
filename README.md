# Workout Tracker API

## Description

Workout Tracker API is a Flask backend application that helps trainers and fitness enthusiasts organize workout sessions and exercises.

Users can create workouts, view exercises, and add exercises to different workouts while recording sets, reps, and duration.

I built this project to practice Flask, SQLAlchemy relationships, database migrations, Marshmallow serialization, and API development.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv

## Database Models

The application has three models:

**Exercise:** Stores an exercise's name, category, and whether equipment is needed.

**Workout:** Stores the workout date, duration in minutes, and optional notes.

**WorkoutExercise:** Connects workouts and exercises and stores the number of reps, sets, and duration in seconds.

A workout can contain multiple exercises, and an exercise can belong to multiple workouts.

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/khishaplays/flask-workout-tracker-api.git
cd flask-workout-tracker-api/server
```

Install the dependencies:

```bash
pipenv install
```

Apply the database migrations:

```bash
pipenv run flask --app app db upgrade
```

Add sample data:

```bash
pipenv run python seed.py
```

Start the Flask server:

```bash
pipenv run python app.py
```

The application runs at `http://127.0.0.1:5555`.

## API Endpoints

| Method | Endpoint                                                           | Description                  |
| ------ | ------------------------------------------------------------------ | ---------------------------- |
| GET    | `/workouts`                                                        | Get all workouts             |
| GET    | `/workouts/<id>`                                                   | Get a specific workout       |
| POST   | `/workouts`                                                        | Create a new workout         |
| DELETE | `/workouts/<id>`                                                   | Delete a workout             |
| GET    | `/exercises`                                                       | Get all exercises            |
| GET    | `/exercises/<id>`                                                  | Get a specific exercise      |
| POST   | `/exercises`                                                       | Create a new exercise        |
| DELETE | `/exercises/<id>`                                                  | Delete an exercise           |
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Requests

Create an exercise:

```bash
curl -X POST http://127.0.0.1:5555/exercises \
-H "Content-Type: application/json" \
-d '{
  "name": "Push-ups",
  "category": "Strength",
  "equipment_needed": false
}'
```

Create a workout:

```bash
curl -X POST http://127.0.0.1:5555/workouts \
-H "Content-Type: application/json" \
-d '{
  "date": "2026-10-19",
  "duration_minutes": 45,
  "notes": "Upper body workout"
}'
```

Attach an exercise to a workout:

```bash
curl -X POST \
http://127.0.0.1:5555/workouts/1/exercises/1/workout_exercises \
-H "Content-Type: application/json" \
-d '{
  "reps": 15,
  "sets": 3
}'
```

## Validations and Constraints

The application uses validations to prevent incorrect data from being saved.

**SQLAlchemy model validations:**

- Exercise names and categories cannot be empty.
- Workout duration must be positive.

**Database constraints:**

- Workout duration must be greater than zero.
- Sets, reps, and exercise duration cannot be negative.

**Marshmallow validations:**

- Workout duration must be at least one minute.
- Exercise names and categories have length limits.
- Sets, reps, and exercise duration must be nonnegative.

## Seed Data

The `seed.py` file creates four sample exercises, two workouts, and three workout-exercise associations.

The script clears existing records before inserting sample data, so it can be run multiple times without creating duplicates.

**Note:** Running the seed script replaces existing workout data.

## What I Learned

Through this project, I practiced creating REST API endpoints, designing related database models, using migrations, validating user input, and returning JSON responses.

I also learned how to test API endpoints and database constraints using terminal commands.

## Author

Khisha

GitHub: [khishaplays](https://github.com/khishaplays)
