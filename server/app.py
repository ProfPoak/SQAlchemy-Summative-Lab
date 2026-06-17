from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from datetime import date

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([workout.id for workout in workouts]), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout:
        return jsonify({'id': workout.id}), 200
    return jsonify({'error': 'Workout not found'}), 404

@app.route('/workouts', methods=['POST'])
def create_workout():
    workout = Workout(date=date(2026, 6, 17), duration_minutes=30, notes='Test')
    db.session.add(workout)
    db.session.commit()
    return jsonify({'id': workout.id, 'message': 'Workout created'}), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    db.session.delete(workout)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)