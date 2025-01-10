import json
import os

SAVE_DIR = "saved_data"
WORKOUT_FILE = os.path.join(SAVE_DIR, "saved_workouts.json")
TIMER_FILE = os.path.join(SAVE_DIR, "saved_timers.json")


def ensure_save_dir():
    """Ensure the save directory exists."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def save_workout(workouts):
    """Save workouts to a JSON file."""
    ensure_save_dir()
    with open(WORKOUT_FILE, "w") as f:
        json.dump(workouts, f, indent=4)


def load_workouts():
    """Load workouts from a JSON file."""
    if os.path.exists(WORKOUT_FILE):
        with open(WORKOUT_FILE, "r") as f:
            return json.load(f)
    return []


def save_timer_config(timer_config):
    """Save timer configurations to a JSON file."""
    ensure_save_dir()
    with open(TIMER_FILE, "w") as f:
        json.dump(timer_config, f, indent=4)


def load_timer_config():
    """Load timer configurations from a JSON file."""
    if os.path.exists(TIMER_FILE):
        with open(TIMER_FILE, "r") as f:
            return json.load(f)
    return {"work_duration": 30, "rest_duration": 15, "rounds": 1}  # Default values
