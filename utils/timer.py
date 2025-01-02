import time

def countdown_timer_with_progress(duration, message, progress_callback=None):
    """Counts down the timer, displays the remaining time, and reports progress."""
    for elapsed in range(duration):
        remaining = duration - elapsed
        mins, secs = divmod(remaining, 60)
        timer_display = f"{mins:02d}:{secs:02d}"  # Format as MM:SS
        if progress_callback:
            progress_callback(elapsed, duration)
        print(f"\r{message} | Time Left: {timer_display}", end="")
        time.sleep(1)
    print("\r" + " " * 50, end="")  # Clear the line

def workout_timer_with_progress(exercises, work_duration, rest_duration, rounds, progress_callback):
    """
    Runs the workout timer with progress reporting for GUI updates.
    """
    total_steps = len(exercises) * rounds * (work_duration + rest_duration)
    step_count = 0

    for round_num in range(1, rounds + 1):
        for exercise in exercises:
            # Work Phase
            step_count += work_duration
            progress_callback(exercise, "WORKING", step_count, total_steps)
            countdown_timer_with_progress(
                work_duration, f"WORKING | {exercise}", lambda e, d: progress_callback(exercise, "WORKING", e, d)
            )

            # Rest Phase
            if rest_duration > 0:
                step_count += rest_duration
                progress_callback("Rest", "RESTING", step_count, total_steps)
                countdown_timer_with_progress(
                    rest_duration, "RESTING", lambda e, d: progress_callback("Rest", "RESTING", e, d)
                )
