import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import utils.file_operations as file_ops
from utils.exercise_selector import ExerciseSelector

# Initialize session state.
# Workout creation variables.
if "exercises" not in st.session_state:
    st.session_state.exercises = []
if "timer_config" not in st.session_state:
    st.session_state.timer_config = {}
if "selector" not in st.session_state:
    st.session_state.selector = ExerciseSelector("exercises.json")
if "num_exercises" not in st.session_state:
    st.session_state.num_exercises = 0
if "saved_exercises" not in st.session_state:
    st.session_state.saved_exercises = {}

# Keep track of different modes.
if "loading_screen" not in st.session_state:
    st.session_state.loading_screen = True
if "new_workout_screen" not in st.session_state:
    st.session_state.new_workout_screen = False
if "create_exercise_screen" not in st.session_state:
    st.session_state.create_exercise_screen = False
if "preview_screen" not in st.session_state:
    st.session_state.preview_screen = False
if "save_workout" not in st.session_state:
    st.session_state.save_workout = False
if "save_timer" not in st.session_state:
    st.session_state.save_timer = False
if "run_timer" not in st.session_state:
    st.session_state.run_timer = False

# Timer states.
if "paused" not in st.session_state:
    st.session_state.paused = False
if "round" not in st.session_state:
    st.session_state.round = 1
if "exercise_index" not in st.session_state:
    st.session_state.exercise_index = 0
if "phase" not in st.session_state:
    st.session_state.phase = "WORK"
if "time_remaining" not in st.session_state:
    st.session_state.time_remaining = 0
if "time_elapsed" not in st.session_state:
    st.session_state.time_elapsed = 0
if "step_count" not in st.session_state:
    st.session_state.step_count = 0


def show_exercise_link(exercise):
    """Show the exercise link either as an image or a HTML link."""
    if exercise["link"] and exercise["link"].endswith(("jpg", "png")):
        _, col2, _ = st.columns(3)
        with col2:
            st.image(exercise["link"], width=300)
    elif exercise["link"]:
        st.video(exercise["link"], muted=True)


def create_workout(selected_workout, selected_timer):
    """Transition from loading workout screen to either inputting new workout params or loading the saved workout/timer config."""
    # Load selected workout/timer if applicable
    if selected_timer:
        st.session_state.timer_config = file_ops.load_timer_config(selected_timer)
    if selected_workout:
        st.session_state.saved_exercises = file_ops.load_workouts(selected_workout)
        st.session_state.num_exercises = len(st.session_state.saved_exercises)
        st.session_state.create_exercise_screen = True
    else:
        st.session_state.new_workout_screen = True

    st.session_state.loading_screen = False


def select_exercises():
    """Transition from inputting new workout params to selecting exercises."""
    st.session_state.new_workout_screen = False
    st.session_state.create_exercise_screen = True


def preview_workout(exercise_entries, timer_config):
    """Select exercises based on user input and transition from inputting exercises to previewing the workout."""
    # Reset saved exercises.
    st.session_state.exercises = []
    st.session_state.timer_config = timer_config

    for i, entry in enumerate(exercise_entries, 1):
        manual_entry, exercise_type, body_part = entry
        exercise_name = None
        link = None

        if manual_entry:
            exercise_name = manual_entry
        elif exercise_type or body_part:
            exercise_name, link = st.session_state.selector.select_exercise(
                exercise_type, body_part
            )

        if exercise_name:
            if exercise_name in st.session_state.saved_exercises:
                st.session_state.exercises.append(
                    st.session_state.saved_exercises[exercise_name]
                )
            else:
                st.session_state.exercises.append(
                    {
                        "name": exercise_name,
                        "link": link,
                        "type": exercise_type,
                        "body_part": body_part,
                    }
                )
            st.session_state.selector.remove_exercise(exercise_name)
        else:
            # If an exercise is empty or invalid, show an error.
            st.error(
                f"Exercise {i} could not be found for this combination of type ({exercise_type}) and body part ({body_part})."
            )

    st.session_state.create_exercise_screen = False
    st.session_state.preview_screen = True


def back_to_edit():
    """Transition from workout preview screen back to the execise selection screen."""
    # Save current exercises.
    st.session_state.saved_exercises = {}
    for exercise in st.session_state.exercises:
        st.session_state.saved_exercises[exercise["name"]] = exercise

    st.session_state.preview_screen = False
    st.session_state.create_exercise_screen = True


def run_timer():
    """Transition from the workout preview screen to the workout timer."""
    # Set up timer start conditions.
    st.session_state.round = 1
    st.session_state.exercise_index = 0
    st.session_state.phase = "WORK"
    st.session_state.time_remaining = st.session_state.timer_config["work_duration"]
    st.session_state.time_elapsed = 0

    st.session_state.preview_screen = False
    st.session_state.run_timer = True


# Main Title
st.title("🏋️ Workout Generator")

# Start with loading screen.
if st.session_state.loading_screen:
    # Load existing workouts and timers
    saved_workouts = [f for f in os.listdir(file_ops.SAVED_WORKOUTS_PATH)]
    saved_timers = [f for f in os.listdir(file_ops.SAVED_TIMERS_PATH)]

    selected_workout = st.selectbox("Load Workout:", [""] + saved_workouts)
    selected_timer = st.selectbox("Load Timer Config:", [""] + saved_timers)

    # Button to start creating a new workout
    st.button(
        "Create Workout",
        on_click=lambda: create_workout(selected_workout, selected_timer),
    )


if st.session_state.new_workout_screen:
    st.session_state.selector = ExerciseSelector(
        "exercises.json"
        if st.radio("Equipment?", ["No Equipment", "Equipment"]) == "Equipment"
        else "no_equipment_exercises.json"
    )
    num_exercises = st.number_input(
        "Number of Exercises:", min_value=1, max_value=50, value=4
    )
    st.session_state.num_exercises = num_exercises

    st.button("Enter", on_click=select_exercises)

# Create Exercise Slots
if st.session_state.create_exercise_screen:
    # Exercise and Timer Configuration
    st.header("Exercise and Timer Configuration")

    # Exercise Configuration
    st.subheader("Configure Exercises")
    exercise_entries = []

    for i in range(st.session_state.num_exercises):
        saved_exercise = None
        if i < len(st.session_state.saved_exercises):
            saved_exercise = list(st.session_state.saved_exercises.keys())[i]
        manual_entry = st.text_input(
            f"Exercise {i + 1}",
            value=(saved_exercise if saved_exercise else ""),
            placeholder=(
                "Enter custom exercise (optional)" if not saved_exercise else None
            ),
        )

        # Create two columns
        col1, col2 = st.columns(2)
        with col1:
            exercise_type = st.selectbox(
                f"Type of Exercise {i + 1}",
                options=[""] + st.session_state.selector.exercise_categories(),
            )

        with col2:
            body_part = st.selectbox(
                f"Body Part for Exercise {i + 1}",
                options=["", "legs", "upper_body", "abs", "cardio"],
            )
        exercise_entries.append((manual_entry, exercise_type, body_part))

    # Timer Configuration
    st.subheader("Configure Timer")
    timer_config = {}
    timer_config["rounds"] = st.number_input(
        "Number of Rounds:",
        min_value=1,
        value=(st.session_state.timer_config.get("rounds", 3)),
    )
    timer_config["work_duration"] = st.number_input(
        "Work Duration (seconds):",
        min_value=1,
        value=st.session_state.timer_config.get("work_duration", 30),
    )
    timer_config["rest_duration"] = st.number_input(
        "Rest Duration (seconds):",
        min_value=0,
        value=st.session_state.timer_config.get("rest_duration", 15),
    )

    # Save or Preview Options
    st.button(
        "Preview Workout",
        on_click=lambda: preview_workout(exercise_entries, timer_config),
    )

# Workout Preview
if st.session_state.preview_screen:
    st.header("Workout Preview", divider=True)
    for i, exercise in enumerate(st.session_state.exercises, 1):
        st.markdown(f"#### {i}. {exercise['name']}")
        show_exercise_link(exercise)

    timer_info = st.session_state.timer_config
    st.subheader("Time:", divider=True)
    st.markdown(
        f"#### Rounds: {timer_info['rounds']}, Work: {timer_info['work_duration']}s, "
        f"Rest: {timer_info['rest_duration']}s"
    )
    st.button("Start Timer", on_click=run_timer)

    if st.button("Save Workout"):
        st.session_state.save_workout = True

    if st.button("Save Timer Config"):
        st.session_state.save_timer = True

    st.button("Back to Edit", on_click=back_to_edit)


def save_workout(filename):
    file_ops.save_workout(filename, st.session_state.exercises)
    st.session_state.save_workout = False


def save_timer_config(filename):
    file_ops.save_timer_config(filename, st.session_state.timer_config)
    st.session_state.save_timer = False


if st.session_state.save_workout:
    filename = st.text_input("Workout Filename")
    st.button("Save", on_click=lambda: save_workout(filename))

if st.session_state.save_timer:
    filename = st.text_input("Timer Filename")
    st.button("Save", on_click=lambda: save_timer_config(filename))


def update_timer():
    """Update the GUI timer labels and progress bars."""
    # Find the current exercise.
    exercise = st.session_state.exercises[st.session_state.exercise_index]
    # Display current phase and exercise
    st.subheader(f"Round: {st.session_state.round}", divider=True)
    if st.session_state.phase == "WORK":
        st.markdown(
            f"<div style='text-align: center; font-size: 24px;'>🚀 Exercise: {exercise['name']}</div>",
            unsafe_allow_html=True,
        )
        show_exercise_link(exercise)
    elif st.session_state.phase == "REST":
        st.subheader("😌 Rest")

    # Display time remaining.
    mins, secs = divmod(st.session_state.time_remaining, 60)
    st.markdown(
        f"<div style='text-align: center; font-size: 24px;'>{mins:02}:{secs:02}</div>",
        unsafe_allow_html=True,
    )

    # Display progress bars.
    st.progress(
        st.session_state.step_count
        / (
            st.session_state.timer_config["rounds"] * st.session_state.num_exercises * 2
        ),
        text="Workout Progress",
    )


if st.session_state.run_timer:
    if st.session_state.round <= st.session_state.timer_config["rounds"]:
        update_timer()
        if not st.session_state.paused:
            st.session_state.time_remaining -= 1
            st.session_state.time_elapsed += 1

            if st.session_state.time_remaining < 0:
                st.session_state.step_count += 1
                # If we were in a rest phase, go to a work phase and increment the exercise index.
                if st.session_state.phase == "REST":
                    st.session_state.phase = "WORK"
                    st.session_state.time_remaining = st.session_state.timer_config[
                        "work_duration"
                    ]
                    # If we just finished the last exercise, go to the next round.
                    if (
                        st.session_state.exercise_index
                        == st.session_state.num_exercises - 1
                    ):
                        st.session_state.round += 1
                        st.session_state.exercise_index = 0
                    else:
                        st.session_state.exercise_index += 1
                # If we were in a work phase, go to a rest phase.
                elif st.session_state.phase == "WORK":
                    st.session_state.phase = "REST"
                    st.session_state.time_remaining = st.session_state.timer_config[
                        "rest_duration"
                    ]
                # Reset time elapsed.
                st.session_state.time_elapsed = 0
            # Timer controls
            st.button(
                "⏸️ Pause",
                on_click=lambda: setattr(st.session_state, "paused", True),
            )
            # Non-blocking countdown logic
            st_autorefresh(interval=1000, limit=None)
        else:
            st.button(
                "▶️ Resume",
                on_click=lambda: setattr(st.session_state, "paused", False),
            )
    else:
        # Workout complete
        st.progress(1.0, text="Workout Progress")
        st.success("🎉 Workout Complete!")
