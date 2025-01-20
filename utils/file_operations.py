import json
import os

SAVED_WORKOUTS_PATH = "saved_data/workouts/"
SAVED_TIMERS_PATH = "saved_data/timers/"


def ensure_save_dir(dir):
    """Ensure the save directory exists."""
    if not os.path.exists(dir):
        os.makedirs(dir)


def save_workout(filename, exercises):
    """Save workouts to a JSON file."""
    ensure_save_dir(SAVED_WORKOUTS_PATH)
    with open(os.path.join(SAVED_WORKOUTS_PATH, filename), "w") as f:
        json.dump(exercises, f, indent=4)


def load_workouts(filename):
    """Load workouts from a JSON file."""
    workout = {}
    full_path = os.path.join(SAVED_WORKOUTS_PATH, filename)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            exercises = json.load(f)
        for exercise in exercises:
            workout[exercise["name"]] = exercise
    return workout


def save_timer_config(filename, timer_config):
    """Save timer configurations to a JSON file."""
    ensure_save_dir(SAVED_TIMERS_PATH)
    with open(os.path.join(SAVED_TIMERS_PATH, filename), "w") as f:
        json.dump(
            timer_config,
            f,
            indent=4,
        )


def load_timer_config(filename):
    """Load timer configurations from a JSON file."""
    full_path = os.path.join(SAVED_TIMERS_PATH, filename)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            return json.load(f)
    return []
