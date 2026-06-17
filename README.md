# SQAlchemy-Summative-Lab

A Flask and SQLAlchemy backend API for tracking workouts and exercises. The application models a many-to-many relationship between workouts and exercises through an association object, allowing each exercise within a workout to track its own reps, sets, and duration.

## Installation

1. Clone the repository and navigate into it.
2. Install dependencies with Pipenv:
   ```
   pipenv install
   pipenv shell
   ```
3. Navigate into the server directory:
   ```
   cd server
   ```
4. Run the database migrations:
   ```
   flask db upgrade
   ```
5. Seed the database with starter data:
   ```
   python seed.py
   ```

## Running the App

From the `server` directory:
```
python app.py
```

The API will be available at `http://localhost:5555`.

## Endpoints

### Workouts

`GET /workouts` — Returns a list of all workouts.

`GET /workouts/<id>` — Returns a single workout, including its associated exercises (reps, sets, duration).

`POST /workouts` — Creates a new workout. Expects JSON with `date`, `duration_minutes`, and `notes`.

`DELETE /workouts/<id>` — Deletes a workout and its associated workout-exercise records.

### Exercises

`GET /exercises` — Returns a list of all exercises.

`GET /exercises/<id>` — Returns a single exercise and its associated workout history.

`POST /exercises` — Creates a new exercise. Expects JSON with `name`, `category`, and `equipment_needed`.

`DELETE /exercises/<id>` — Deletes an exercise and its associated workout-exercise records.

### Workout Exercises

`POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` — Adds an exercise to a workout, including `reps`, `sets`, and `duration_seconds`. Expects JSON with `workout_id`, `exercise_id`, and the above fields.