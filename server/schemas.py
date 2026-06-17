from marshmallow import Schema, fields
from models import Exercise, Workout, WorkoutExercises

class ExerciseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()

class WorkoutSchema(Schema):
    id = fields.Integer()
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()

class WorkoutExercisesSchema(Schema):
    id = fields.Integer()
    workout_id = fields.Integer()
    exercise_id = fields.Integer()
    reps = fields.Integer()
    sets = fields.Integer()
    duration_seconds = fields.Integer()