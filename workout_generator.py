import os
from tkinter import ttk
import tkinter as tk
from utils.exercise_selector import ExerciseSelector
import utils.file_operations as file_ops


class WorkoutTimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Timer Creator")
        self.selector = ExerciseSelector("exercises.json")
        self.exercises = []
        self.num_exercises = 0

        # Global variables to track paused state.
        self.paused = False
        self.pause_button = None
        self.pause_event = None

        # Timer config.
        self.timer_config = {}

        # Main Menu
        self.main_menu()

    def main_menu(self):
        """Create the main menu."""
        frame = tk.Frame(self.root)
        frame.pack(pady=30)

        # Buttons for creating a workout and loading saved data.
        tk.Label(frame, text="Load Workout:", font=("Arial", 14)).pack()
        loaded_workout = ttk.Combobox(
            frame,
            values=[
                f
                for f in os.listdir(file_ops.SAVED_WORKOUTS_PATH)
                if os.path.isfile(os.path.join(file_ops.SAVED_WORKOUTS_PATH, f))
            ],
            state="readonly",
            width=20,
        )
        loaded_workout.pack(pady=10)

        tk.Label(frame, text="Load Timer:", font=("Arial", 14)).pack()
        loaded_timer = ttk.Combobox(
            frame,
            values=[
                f
                for f in os.listdir(file_ops.SAVED_TIMERS_PATH)
                if os.path.isfile(os.path.join(file_ops.SAVED_TIMERS_PATH, f))
            ],
            state="readonly",
            width=20,
        )
        loaded_timer.pack(pady=10)

        # Input number of exercises if not loading a saved workout.
        tk.Button(
            frame,
            text="Create Workout",
            command=lambda: self.create_workout(loaded_workout, loaded_timer),
        ).pack(pady=10)

    def create_workout(self, loaded_workout, loaded_timer):
        """Create a new workout or load a workout/timer config."""
        if loaded_timer.get():
            timer_config = file_ops.load_timer_config(loaded_timer.get())
            self.num_rounds = timer_config["rounds"]
            self.work_duration = timer_config["work_duration"]
            self.rest_duration = timer_config["rest_duration"]

        if loaded_workout.get():
            self.exercises = file_ops.load_workouts(loaded_workout.get())
            self.num_exercises = len(self.exercises)
            self.create_exercise_slots(None)
        else:
            self.input_num_exercises()

    def input_num_exercises(self):
        """Input the number of exercises."""
        # Clear previous content
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Input number of exercises
        tk.Label(frame, text="Number of Exercises:", font=("Arial", 14)).pack()
        num = tk.Entry(frame, width=5)
        num.pack(pady=5)

        tk.Button(
            frame,
            text="Create Exercise Slots",
            command=lambda: self.create_exercise_slots(num),
        ).pack(pady=10)

    def create_exercise_slots(self, num_exercise_entry):
        """Create slots for exercises and timer configuration in one window."""
        if num_exercise_entry:
            try:
                self.num_exercises = int(num_exercise_entry.get())
            except ValueError:
                tk.messagebox.showerror(
                    "Error", "Please enter a valid number of exercises!"
                )
                return

        if self.num_exercises <= 0:
            tk.messagebox.showerror(
                "Error", "Number of exercises must be greater than zero!"
            )
            return

        # Clear previous content
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.exercise_entries = []

        # Section: Exercise Selection
        tk.Label(frame, text="Configure Exercises:", font=("Arial", 16)).pack(pady=10)
        for i in range(self.num_exercises):
            exercise = None
            if i < len(self.exercises) - 1:
                exercise = self.exercises[i]

            tk.Label(frame, text=f"Exercise {i + 1}:", font=("Arial", 12)).pack(
                anchor="w", pady=2
            )

            # Manual entry option with placeholder text
            manual_entry = tk.Entry(
                frame,
                width=30,
                fg=(
                    "black"
                    if exercise
                    and not exercise.get("type")
                    and not exercise.get("body_part")
                    else "grey"
                ),
            )
            placeholder_text = "Enter custom exercise (optional)"
            manual_entry.insert(
                0,
                (
                    exercise["name"]
                    if exercise and not exercise["type"] and not exercise["body_part"]
                    else placeholder_text
                ),
            )

            # Bind events to handle placeholder behavior
            def on_focus_in(event, entry=manual_entry, placeholder=placeholder_text):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg="black")

            def on_focus_out(event, entry=manual_entry, placeholder=placeholder_text):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.config(fg="grey")

            manual_entry.bind("<FocusIn>", on_focus_in)
            manual_entry.bind("<FocusOut>", on_focus_out)
            manual_entry.pack(anchor="w", pady=2)

            # Random selection option
            random_frame = tk.Frame(frame)
            random_frame.pack(anchor="w", pady=5)

            type_label = tk.Label(random_frame, text="Type:")
            type_label.grid(row=0, column=0, padx=5)
            type_box = ttk.Combobox(
                random_frame,
                values=self.selector.exercise_categories(),
                state="readonly",
                width=12,
            )
            type_box.grid(row=0, column=1, padx=5)

            body_part_label = tk.Label(random_frame, text="Body Part:")
            body_part_label.grid(row=0, column=2, padx=5)
            body_part_box = ttk.Combobox(
                random_frame,
                values=["full_body", "legs", "chest", "abs", "upper_body"],
                state="readonly",
                width=12,
            )
            body_part_box.grid(row=0, column=3, padx=5)

            # Set dropdown values based on stored exercise data
            if exercise:
                if exercise.get("type"):
                    type_box.set(exercise["type"])
                if exercise.get("body_part"):
                    body_part_box.set(exercise["body_part"])

            self.exercise_entries.append((manual_entry, type_box, body_part_box))

        # Section: Timer Configuration
        tk.Label(frame, text="Configure Timer:", font=("Arial", 16)).pack(pady=10)

        # Number of Rounds
        tk.Label(frame, text="Number of Rounds:", font=("Arial", 12)).pack(
            anchor="w", pady=2
        )
        num_rounds_entry = tk.Entry(frame, width=10)
        if self.timer_config.get("num_rounds"):
            num_rounds_entry.insert(0, self.timer_config["num_rounds"])
        num_rounds_entry.pack(anchor="w", pady=5)

        # Work Duration
        tk.Label(frame, text="Work Duration (seconds):", font=("Arial", 12)).pack(
            anchor="w", pady=2
        )
        work_duration_entry = tk.Entry(frame, width=10)
        if self.timer_config.get("work_duration"):
            work_duration_entry.insert(0, self.timer_config["work_duration"])
        work_duration_entry.pack(anchor="w", pady=5)

        # Rest Duration
        tk.Label(frame, text="Rest Duration (seconds):", font=("Arial", 12)).pack(
            anchor="w", pady=2
        )
        rest_duration_entry = tk.Entry(frame, width=10)
        if self.timer_config.get("rest_duration"):
            rest_duration_entry.insert(0, self.timer_config["rest_duration"])
        rest_duration_entry.pack(anchor="w", pady=5)

        # Buttons
        tk.Button(
            frame,
            text="Preview Workout",
            command=lambda: self.preview_workout(
                num_rounds_entry, work_duration_entry, rest_duration_entry
            ),
        ).pack(pady=20)

    def preview_workout(
        self, num_rounds_entry, work_duration_entry, rest_duration_entry
    ):
        """Show a preview of the workout and timer settings after validation."""
        self.exercises = []

        for i, entry in enumerate(self.exercise_entries):
            manual_entry, type_box, body_part_box = entry
            manual_name = manual_entry.get().strip()
            exercise_name = None
            link = None
            exercise_type = None
            body_part = None

            # Validate manual entry or random selection
            if manual_name and manual_name != "Enter custom exercise (optional)":
                exercise_name = manual_name
            else:
                exercise_type = type_box.get()
                body_part = body_part_box.get()
                if exercise_type and body_part:
                    exercise_name, link = self.selector.select_exercise(
                        exercise_type, body_part
                    )
                elif exercise_type:
                    exercise_name, link = self.selector.select_exercise(
                        exercise_type, None
                    )
                elif body_part:
                    exercise_name, link = self.selector.select_exercise(None, body_part)
                else:
                    # If nothing is input, show an error.
                    tk.messagebox.showerror(
                        "Error",
                        f"Please fill out all exercise fields for Exercise {i + 1} correctly.\n"
                        "Ensure you select at least one of type and body part for random exercises or manually input an exercise.",
                    )
                    return  # Prevent proceeding to preview

            if exercise_name:
                self.exercises.append(
                    {
                        "name": exercise_name,
                        "link": link,
                        "type": exercise_type,
                        "body_part": body_part,
                    }
                )
            else:
                # If an exercise is empty or invalid, show an error
                tk.messagebox.showerror(
                    "Error",
                    f"Exercise {i + 1} could not be found for this combination of type and body part.",
                )
                return  # Prevent proceeding to preview

        if not self.exercises:
            tk.messagebox.showerror("Error", "No exercises selected!")
            return

        # Validate timer settings
        try:
            work_duration = int(work_duration_entry.get())
            rest_duration = int(rest_duration_entry.get())
            rounds = int(num_rounds_entry.get())
        except ValueError:
            tk.messagebox.showerror(
                "Error", "Please enter valid numeric values for the timer settings."
            )
            return

        if work_duration <= 0 or rest_duration < 0 or rounds <= 0:
            tk.messagebox.showerror("Error", "Timer values must be positive numbers.")
            return

        self.timer_config = {
            "work_duration": work_duration,
            "rest_duration": rest_duration,
            "rounds": rounds,
        }

        # If all validations pass, proceed to the preview screen
        self.show_preview_screen()

    def show_preview_screen(self):
        """Display the preview screen after successful validation."""
        # Clear window and show preview screen
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Workout Preview", font=("Arial", 16)).pack(pady=10)

        for i, exercise in enumerate(self.exercises, 1):
            tk.Label(frame, text=f"{i}. {exercise['name']}", font=("Arial", 12)).pack(
                anchor="w"
            )

        timer_info = (
            f"Timer: {self.timer_config['work_duration']}s work, "
            f"{self.timer_config['rest_duration']}s rest, {self.timer_config['rounds']} rounds"
        )
        tk.Label(frame, text=timer_info, font=("Arial", 12)).pack(pady=10)

        tk.Button(
            frame,
            text="Save Workout",
            command=lambda: self.input_filename(file_ops.save_workout, self.exercises),
        ).pack(pady=5)
        tk.Button(
            frame,
            text="Save Timer Config",
            command=lambda: self.input_filename(
                file_ops.save_timer_config, self.timer_config
            ),
        ).pack(pady=5)

        # Add Back to Edit button
        tk.Button(
            frame, text="Back to Edit", command=lambda: self.create_exercise_slots(None)
        ).pack(pady=5)

        # Add Start Timer button
        tk.Button(
            frame,
            text="Start Timer",
            command=lambda: self.run_timer_with_gui(
                self.exercises,
                self.timer_config["work_duration"],
                self.timer_config["rest_duration"],
                self.timer_config["rounds"],
            ),
        ).pack(pady=20)

    def input_filename(self, func, *args):
        """Choose a filename to save data."""
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Filename:", font=("Arial", 12)).pack(anchor="w", pady=2)
        filename_entry = tk.Entry(frame, width=20)
        filename_entry.pack(anchor="w", pady=5)

        tk.Button(
            frame,
            text="Save",
            command=lambda: self.save_data(frame, filename_entry, func, *args),
        ).pack(pady=5)

    def save_data(self, frame, filename_entry, func, *args):
        """Save data and remove the given frame."""
        func(filename_entry.get(), *args)
        frame.destroy()

    def run_timer_with_gui(self, exercises, work_duration, rest_duration, rounds):
        """Run the workout timer with a dedicated GUI window."""
        # Clear the previous frame.
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a new timer window
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Timer widgets
        current_exercise_label = tk.Label(frame, text="", font=("Arial", 16))
        current_exercise_label.pack(pady=10)

        timer_label = tk.Label(frame, text="", font=("Arial", 20, "bold"))
        timer_label.pack(pady=10)

        phase_label = tk.Label(frame, text="", font=("Arial", 14))
        phase_label.pack(pady=5)

        individual_progress = ttk.Progressbar(
            frame, orient="horizontal", length=300, mode="determinate"
        )
        individual_progress.pack(pady=10)

        overall_progress = ttk.Progressbar(
            frame, orient="horizontal", length=300, mode="determinate"
        )
        overall_progress.pack(pady=10)

        total_steps = len(exercises) * rounds * (work_duration + rest_duration)
        step_count = 0

        def toggle_pause():
            """Pause/resume the timer."""
            self.paused = not self.paused
            if self.paused:
                pause_button.config(text="▶️ Resume")
            else:
                pause_button.config(text="⏸️ Pause")
                self.pause_event()
                self.pause_event = None

        pause_button = tk.Button(frame, text="⏸️ Pause", command=toggle_pause)
        pause_button.pack(pady=5)

        def update_timer(remaining, phase, exercise, elapsed, total, next_action):
            """Update the GUI timer labels and progress bars."""
            if self.paused:
                # Save the paused event
                self.pause_event = lambda: update_timer(
                    remaining, phase, exercise, elapsed, total, next_action
                )
                return

            # Update labels
            mins, secs = divmod(remaining, 60)
            timer_label.config(text=f"{mins:02}:{secs:02}")
            current_exercise_label.config(
                text=(
                    f"🚀 Exercise: {exercise}" if phase == "WORKING" else "😌 Rest Time"
                )
            )
            phase_label.config(text=f"Phase: {phase}")

            # Update progress bars
            individual_progress["value"] = (elapsed / total) * 100
            overall_progress["value"] = (step_count / total_steps) * 100

            # Schedule next action or end
            if remaining > 0:
                frame.after(
                    1000,
                    update_timer,
                    remaining - 1,
                    phase,
                    exercise,
                    elapsed + 1,
                    total,
                    next_action,
                )
            else:
                next_action()

        def start_work(exercise, next_phase):
            """Start the work phase for an exercise."""
            nonlocal step_count
            step_count += work_duration
            update_timer(
                work_duration, "WORKING", exercise, 0, work_duration, next_phase
            )

        def start_rest(next_exercise_action):
            """Start the rest phase between exercises."""
            nonlocal step_count
            step_count += rest_duration
            update_timer(
                rest_duration, "RESTING", "Rest", 0, rest_duration, next_exercise_action
            )

        def next_exercise(round_index, exercise_index):
            """Move to the next exercise or round."""
            if exercise_index < len(exercises):
                # Next exercise in the same round
                start_work(
                    exercises[exercise_index]["name"],
                    lambda: start_rest(
                        lambda: next_exercise(round_index, exercise_index + 1)
                    ),
                )
            elif round_index < rounds - 1:
                # Start the next round
                next_exercise(round_index + 1, 0)
            else:
                # Workout complete
                timer_label.config(text="🎉 Workout Complete!")
                current_exercise_label.config(text="Great job! 💪")
                phase_label.config(text="")
                individual_progress["value"] = 100
                overall_progress["value"] = 100

        # Start the timer
        next_exercise(0, 0)

    def open_link(self, link):
        """Open the exercise link in the browser."""
        import webbrowser

        webbrowser.open(link)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutTimerGUI(root)
    root.mainloop()
