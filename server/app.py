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
            notes=validated_data.get('notes')
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
    return jsonify([exercise.id for exercise in exercises]), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise:
        return jsonify({'id': exercise.id}), 200
    return jsonify({'error': 'Exercise not found'}), 404

@app.route('/exercises', methods=['POST'])
def create_exercise():
    exercise = Exercise(name='Test', category='run', equipment_needed=False)
    db.session.add(exercise)
    db.session.commit()
    return jsonify({'id': exercise.id, 'message': f'{exercise.name} created'}), 201

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
    we = WorkoutExercises(workout_id=workout_id, exercise_id=exercise_id, sets=None, reps=None, duration_seconds=1200)
    db.session.add(we)
    db.session.commit()
    return jsonify({'message': f'Exercise:{exercise_id} added to Workout:{workout_id}'}), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)