import tkinter as tk
import random
from utils.exercise_selector import ExerciseSelector
from utils.timer import workout_timer

class WorkoutTimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Timer Creator")
        self.selector = ExerciseSelector('exercises.json')
        self.exercises = []

        # Main Menu
        self.main_menu()

    def main_menu(self):
        """Create the main menu."""
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Select Timer Type:", font=("Arial", 14)).pack()

        self.timer_type = ttk.Combobox(
            frame, values=["Circuit Timer", "Custom Timer"], state="readonly", width=20
        )
        self.timer_type.pack(pady=5)
        self.timer_type.set("Circuit Timer")

        tk.Button(frame, text="Create Timer Layout", command=self.create_timer_layout).pack(pady=10)

    def create_timer_layout(self):
        """Create the timer layout."""
        timer_type = self.timer_type.get()
        if not timer_type:
            messagebox.showerror("Error", "Please select a timer type!")
            return

        # Clear previous content
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Input number of exercises
        tk.Label(frame, text="Number of Exercises:", font=("Arial", 14)).pack()
        self.num_exercises = tk.Entry(frame, width=5)
        self.num_exercises.pack(pady=5)

        tk.Button(frame, text="Create Exercise Slots", command=self.create_exercise_slots).pack(pady=10)

    def create_exercise_slots(self):
        """Create slots for exercises based on user input."""
        try:
            num_exercises = int(self.num_exercises.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of exercises!")
            return

        if num_exercises <= 0:
            messagebox.showerror("Error", "Number of exercises must be greater than zero!")
            return

        # Clear previous content
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.exercise_entries = []

        for i in range(num_exercises):
            tk.Label(frame, text=f"Exercise {i + 1}:", font=("Arial", 12)).pack(anchor="w", pady=2)

            # Manual entry option
            manual_entry = tk.Entry(frame, width=30)
            manual_entry.pack(anchor="w", pady=2)
            manual_entry.insert(0, "Enter custom exercise (optional)")

            # Random selection option
            random_frame = tk.Frame(frame)
            random_frame.pack(anchor="w", pady=5)

            type_label = tk.Label(random_frame, text="Type:")
            type_label.grid(row=0, column=0, padx=5)
            type_box = ttk.Combobox(
                random_frame, values=["flexibility", "strength", "mobility"], state="readonly", width=12
            )
            type_box.grid(row=0, column=1, padx=5)

            body_part_label = tk.Label(random_frame, text="Body Part:")
            body_part_label.grid(row=0, column=2, padx=5)
            body_part_box = ttk.Combobox(
                random_frame,
                values=["full_body", "legs", "chest", "back", "upper_body"],
                state="readonly",
                width=12,
            )
            body_part_box.grid(row=0, column=3, padx=5)

            self.exercise_entries.append((manual_entry, type_box, body_part_box))

        tk.Button(frame, text="Start Timer", command=self.start_timer).pack(pady=20)

    def start_timer(self):
        """Collect exercises and start the workout timer."""
        exercises = []

        for manual_entry, type_box, body_part_box in self.exercise_entries:
            manual_name = manual_entry.get().strip()
            exercise_name = None

            if manual_name and manual_name != "Enter custom exercise (optional)":
                exercise_name = manual_name
            else:
                exercise_type = type_box.get()
                body_part = body_part_box.get()
                if exercise_type and body_part:
                    exercise_name, _ = self.selector.select_exercise(exercise_type, body_part)
                else:
                    messagebox.showerror("Error", "Please complete all random exercise selections!")
                    return

            if exercise_name:
                exercises.append(exercise_name)

        if not exercises:
            messagebox.showerror("Error", "No exercises selected!")
            return

        # Ask for timer settings
        work_duration = self.get_duration_input("Work Duration (seconds):")
        if work_duration is None:
            return

        rest_duration = self.get_duration_input("Rest Duration (seconds):")
        if rest_duration is None:
            return

        rounds = self.get_duration_input("Number of Rounds:")
        if rounds is None:
            return

        # Start timer
        self.run_timer(exercises, work_duration, rest_duration, rounds)

    def get_duration_input(self, message):
        """Prompt the user for a duration."""
        input_value = tk.simpledialog.askinteger("Input", message)
        if input_value is None or input_value <= 0:
            messagebox.showerror("Error", "Please enter a valid positive number!")
            return None
        return input_value

    def run_timer(self, exercises, work_duration, rest_duration, rounds):
        """Run the workout timer."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Workout Timer Running!", font=("Arial", 16)).pack(pady=10)
        workout_timer(exercises, work_duration, rest_duration, rounds)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutTimerGUI(root)
    root.mainloop()
