from flask import Flask, make_response, request
from flask_migrate import Migrate
from datetime import date
from marshmallow import ValidationError

from models import *
from schemas import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

workout_schema = WorkoutSchema(exclude=('workout_exercises',))
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
workout_detail_schema = WorkoutSchema()
exercise_schema = ExerciseSchema(exclude=('workout_exercises',))
exercises_schema = ExerciseSchema(many=True, exclude=('workout_exercises',))
exercise_detail_schema = ExerciseSchema()
workout_exercises_schema = WorkoutExercisesSchema(exclude=('exercise',))


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    response_body = workouts_schema.dump(workouts)
    return make_response(response_body, 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout:
        response_body = workout_detail_schema.dump(workout)
        response_status = 200
    else:
        response_body = {'error': f'Workout id: {id} not found'}
        response_status = 404
    return make_response(response_body, response_status)

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    if not data:
        return make_response({'error': 'No input data provided'}, 400)
    try:
        validated_data = workout_schema.load(data)
        workout = Workout(
            date=validated_data['date'],
            duration_minutes=validated_data['duration_minutes'],
            notes=validated_data['notes']
        )
        db.session.add(workout)
        db.session.commit()
        response_body = workout_schema.dump(workout)
        response_status = 201
    except ValidationError as err:
        response_body = err.messages
        response_status = 400

    return make_response(response_body, response_status)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response({'error': f'Workout id: {id} not found'}, 404)
    db.session.delete(workout)
    db.session.commit()
    return '', 204

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    response_body = exercises_schema.dump(exercises)
    return make_response(response_body, 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise:
        response_body = exercise_detail_schema.dump(exercise)
        response_status = 200
    else:
        response_body = {'error': f'Exercise id: {id} not found'}
        response_status = 404
    return make_response(response_body, response_status)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if not data:
        return make_response({'error': 'No input data provided'}, 400)
    try:
        validated_data = exercise_schema.load(data)
        exercise = Exercise(
            name=validated_data['name'],
            category=validated_data['category'],
            equipment_needed=validated_data['equipment_needed']
        )
        db.session.add(exercise)
        db.session.commit()
        response_body = exercise_schema.dump(exercise)
        response_status = 201
    except ValidationError as err:
        response_body = err.messages
        response_status = 400

    return make_response(response_body, response_status)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response({'error': f'Exercise id: {id} not found'}, 404)
    db.session.delete(exercise)
    db.session.commit()
    return '', 204

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    data = request.get_json()
    if not data:
        return make_response({'error': 'No input data provided'}, 400)
    try:
        validated_data = workout_exercises_schema.load(data)
        we = WorkoutExercises(
            workout_id=validated_data['workout_id'],
            exercise_id=validated_data['exercise_id'],
            reps=validated_data['reps'],
            sets=validated_data['sets'],
            duration_seconds=validated_data['duration_seconds']
        )
        db.session.add(we)
        db.session.commit()
        response_body = workout_exercises_schema.dump(we)
        response_status = 201
    except ValidationError as err:
        response_body = err.messages
        response_status = 400

    return make_response(response_body, response_status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)