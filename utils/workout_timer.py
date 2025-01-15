"""Workout timer GUI."""

from tkinter import ttk
import tkinter as tk
import webbrowser


class WorkoutTimerGUI:
    def __init__(self):
        # Variables to track paused state.
        self.paused = False
        self.pause_button = None
        self.pause_event = None

    def run_timer_with_gui(
        self, root, exercises, exercise_imgs, work_duration, rest_duration, rounds
    ):
        """Run the workout timer with a dedicated GUI window."""
        # Clear the previous frame.
        for widget in root.winfo_children():
            widget.destroy()

        # Create a new timer window
        frame = tk.Frame(root)
        frame.pack(pady=20)

        # Timer widgets
        round_label = tk.Label(frame, text="", font=("Arial", 16))
        round_label.pack(pady=10)

        current_exercise_label = tk.Label(frame, text="", font=("Arial", 16))
        current_exercise_label.pack(pady=10)

        exercise_link_label = tk.Label(frame)
        exercise_link_label.pack(pady=10)

        timer_label = tk.Label(frame, text="", font=("Arial", 16, "bold"))
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
                if self.pause_event:
                    self.pause_event()
                self.pause_event = None

        pause_button = tk.Button(frame, text="⏸️ Pause", command=toggle_pause)
        pause_button.pack(pady=5)

        def update_timer(
            remaining,
            round,
            phase,
            exercise,
            exercise_link,
            elapsed,
            total,
            next_action,
        ):
            """Update the GUI timer labels and progress bars."""
            if self.paused:
                # Save the paused event
                self.pause_event = lambda: update_timer(
                    remaining,
                    round,
                    phase,
                    exercise,
                    exercise_link,
                    elapsed,
                    total,
                    next_action,
                )
                return

            # Update labels
            round_label.config(text=f"Round: {round}")
            mins, secs = divmod(remaining, 60)
            timer_label.config(text=f"{mins:02}:{secs:02}")
            current_exercise_label.config(
                text=(
                    f"🚀 Exercise: {exercise}" if phase == "WORKING" else "😌 Rest Time"
                )
            )
            if exercise_imgs.get(exercise):
                exercise_link_label.config(image=exercise_imgs[exercise])
            elif exercise_link:
                exercise_link_label.config(
                    text=f"{exercise} example link",
                    fg="blue",
                    cursor="hand2",
                    font=("Arial", 12, "underline"),
                )
                # Bind the click event to the open_link function
                exercise_link_label.bind(
                    "<Button-1>", lambda e, link=exercise_link: webbrowser.open(link)
                )
            else:
                exercise_link_label.config(image="", text="")
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
                    round,
                    phase,
                    exercise,
                    exercise_link,
                    elapsed + 1,
                    total,
                    next_action,
                )
            else:
                next_action()

        def start_work(round, exercise, exercise_link, next_phase):
            """Start the work phase for an exercise."""
            nonlocal step_count
            step_count += work_duration
            update_timer(
                work_duration,
                round,
                "WORKING",
                exercise,
                exercise_link,
                0,
                work_duration,
                next_phase,
            )

        def start_rest(round, next_exercise_action):
            """Start the rest phase between exercises."""
            nonlocal step_count
            step_count += rest_duration
            update_timer(
                rest_duration,
                round,
                "RESTING",
                "Rest",
                None,
                0,
                rest_duration,
                next_exercise_action,
            )

        def next_exercise(round_index, exercise_index):
            """Move to the next exercise or round."""
            if exercise_index < len(exercises):
                # Next exercise in the same round
                start_work(
                    round_index,
                    exercises[exercise_index]["name"],
                    exercises[exercise_index]["link"],
                    lambda: start_rest(
                        round_index,
                        lambda: next_exercise(round_index, exercise_index + 1),
                    ),
                )
            elif round_index < rounds:
                # Start the next round
                next_exercise(round_index + 1, 0)
            else:
                # Workout complete
                round_label.config(text="🎉 Workout Complete!")
                current_exercise_label.config(text="Great job! 💪")
                timer_label.config(text="")
                exercise_link_label.config(image="", text="")
                phase_label.config(text="")
                individual_progress["value"] = 100
                overall_progress["value"] = 100

        # Start the timer
        next_exercise(1, 0)
