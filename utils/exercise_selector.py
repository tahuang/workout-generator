import json
import random


class ExerciseSelector:
    def __init__(self, exercise_bank_file):
        self.exercise_bank_file = exercise_bank_file
        self.exercise_bank = self.load_exercise_bank(exercise_bank_file)

    def load_exercise_bank(self, file_path):
        """Load the exercise bank from a JSON file."""
        with open(file_path, "r") as f:
            return json.load(f)

    def select_exercise(self, category, body_part):
        """Randomly select an exercise based on category and body part."""
        # If neither a category nor body part is given, randomly choose a category and body part.
        if not category and not body_part:
            category = random.choice(list(self.exercise_bank.keys()))
            body_part = random.choice(list(self.exercise_bank[category].keys()))
        # If a category isn't given, randomly choose a category that also contains the given body part.
        elif not category:
            valid_categories = []
            for k in self.exercise_bank.keys():
                if body_part in self.exercise_bank[k].keys():
                    valid_categories.append(k)
            if valid_categories:
                category = random.choice(valid_categories)
        # If a category is given, but a body part is not, randomly choose an exercise based solely
        # on category.
        elif not body_part:
            body_part = random.choice(list(self.exercise_bank[category].keys()))

        try:
            exercises = self.exercise_bank[category][body_part]
            exercise = random.choice(exercises)
            return exercise["name"], exercise["link"]
        except (KeyError, IndexError):
            return None, None

    def manual_entry(self, exercise_name):
        """Manually add an exercise to the selection."""
        return exercise_name, None

    def exercise_categories(self):
        """Return categories present in the exercise bank."""
        return list(self.exercise_bank.keys())

    def remove_exercise(self, exercise_name):
        """Remove exercise from the exercise bank if it exists to avoid duplicate exercise selection."""
        for category in self.exercise_bank.keys():
            for body_part in self.exercise_bank[category].keys():
                exercises = self.exercise_bank[category][body_part]
                for exercise in exercises:
                    if exercise["name"] == exercise_name:
                        exercises.remove(exercise)

    def reset(self):
        """Reset the exercise selector to the original exercise bank."""
        self.exercise_bank = self.load_exercise_bank(self.exercise_bank_file)
