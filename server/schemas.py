
from marshmallow import Schema, fields, validate


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0)
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0)
    )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    equipment_needed = fields.Bool(load_default=False)

    workouts = fields.List(
        fields.Nested("WorkoutSchema", only=("id", "date")),
        dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.Str(allow_none=True)

    workout_exercises = fields.List(
        fields.Nested(
            WorkoutExerciseSchema,
            exclude=("workout_id",)
        ),
        dump_only=True
    )

    exercises = fields.List(
        fields.Nested(
            ExerciseSchema,
            only=("id", "name", "category", "equipment_needed")
        ),
        dump_only=True
    )
