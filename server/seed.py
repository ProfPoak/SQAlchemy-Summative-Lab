#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercises
from datetime import date

with app.app_context():

    # reset data
    WorkoutExercises.query.delete()
    Exercise.query.delete()
    Workout.query.delete()

    # create exercises
    curls = Exercise(name='Curls', category='weights', equipment_needed=True)
    deadlift = Exercise(name='Deadlift', category='weights', equipment_needed=True)
    bench_press = Exercise(name='Bench Press', category='weights', equipment_needed=True)
    running = Exercise(name='5k', category='run', equipment_needed=False)
    cycling = Exercise(name='Mountain Biking', category='biking', equipment_needed=True)
    swimming = Exercise(name='Lap Swim', category='swimming', equipment_needed=False)
    trail_hike = Exercise(name='Mountain Hike', category='hiking', equipment_needed=True)

    db.session.add_all([curls, deadlift, bench_press, running, cycling, swimming, trail_hike])
    db.session.commit()

    # create workouts
    workout_1 = Workout(date=date(2026, 6, 1), duration_minutes=45, notes='Morning workout, felt strong.')
    workout_2 = Workout(date=date(2026, 6, 3), duration_minutes=30, notes='Quick session before work.')
    workout_3 = Workout(date=date(2026, 6, 5), duration_minutes=60, notes='Long weekend session.')

    db.session.add_all([workout_1, workout_2, workout_3])
    db.session.commit()

    # create workout_exercises (the join records)
    we_1 = WorkoutExercises(workout_id=workout_1.id, exercise_id=curls.id, reps=15, sets=3, duration_seconds=None)
    we_2 = WorkoutExercises(workout_id=workout_1.id, exercise_id=deadlift.id, reps=7, sets=4, duration_seconds=None)
    we_3 = WorkoutExercises(workout_id=workout_1.id, exercise_id=bench_press.id, reps=7, sets=4, duration_seconds=None)
    we_4 = WorkoutExercises(workout_id=workout_2.id, exercise_id=running.id, reps=None, sets=None, duration_seconds=1200)
    we_5 = WorkoutExercises(workout_id=workout_2.id, exercise_id=cycling.id, reps=None, sets=None, duration_seconds=900)
    we_6 = WorkoutExercises(workout_id=workout_3.id, exercise_id=swimming.id, reps=None, sets=None, duration_seconds=1800)
    we_7 = WorkoutExercises(workout_id=workout_3.id, exercise_id=trail_hike.id, reps=None, sets=None, duration_seconds=3600)

    db.session.add_all([we_1, we_2, we_3, we_4, we_5, we_6, we_7])
    db.session.commit()

    print('Seed data created successfully!')