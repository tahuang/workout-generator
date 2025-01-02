import json
import random

class ExerciseSelector:
    def __init__(self, exercise_bank_file):
        self.exercise_bank = self.load_exercise_bank(exercise_bank_file)

    def load_exercise_bank(self, file_path):
        """Load the exercise bank from a JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def select_exercise(self, category, body_part):
        """Randomly select an exercise based on category and body part."""
        try:
            exercises = self.exercise_bank[category][body_part]
            exercise = random.choice(exercises)
            return exercise["name"], exercise["link"]
        except KeyError:
            return "No exercises found for this selection!", None

    def manual_entry(self, exercise_name):
        """Manually add an exercise to the selection."""
        return exercise_name, None
