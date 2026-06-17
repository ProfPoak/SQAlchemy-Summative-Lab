from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    __table_args__ = (
        db.UniqueConstraint('name', name='unique_exercise_name'),
    )

    @validates('category')
    def category_validation(self, key, value):
        exercise_list = ['run', 'weights', 'biking', 'hiking', 'swimming']
        if value not in exercise_list:
            raise ValueError(f"{key} must be one of the following {exercise_list}")
        return value

    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise', cascade='all, delete-orphan')
    workouts = association_proxy('workout_exercises', 'workout')

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name} ({self.category})>'

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='minimum_workout_duration'),
    )

    workout_exercises = db.relationship('WorkoutExercises', back_populates='workout', cascade='all, delete-orphan')
    exercises = association_proxy('workout_exercises', 'exercise')

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}, {self.duration_minutes} min>'

class WorkoutExercises(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    @validates('reps', 'sets')
    def sets_reps_validation(self, key, value):
        if value is None:
            return value
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        return value

    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    workout = db.relationship('Workout', back_populates='workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercises {self.id}: workout={self.workout_id}, exercise={self.exercise.name}, reps={self.reps}, sets={self.sets}>'
