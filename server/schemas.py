from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import Exercise, Workout, WorkoutExercises

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    category = fields.String(validate=validate.OneOf(['run', 'weights', 'biking', 'hiking', 'swimming']))
    equipment_needed = fields.Boolean(load_default=False)
    workout_exercises = fields.Nested('WorkoutExercisesSchema', exclude=('exercise',), many=True)

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()
    workout_exercises = fields.Nested('WorkoutExercisesSchema', many=True)

    @validates_schema
    def check_duration_minutes(self, data, **kwargs):
        if not isinstance(data.get("duration_minutes"), int):
            raise ValidationError("Duration must be an int")
        if data.get("duration_minutes") <= 0:
            raise ValidationError("Workout duration must be greater than 0")

class WorkoutExercisesSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    exercise = fields.Nested('ExerciseSchema', exclude=('workout_exercises',))