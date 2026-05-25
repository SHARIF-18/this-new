import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(page_title="AI Aptitude Teacher")

# Title
st.title("🤖 AI Aptitude Teacher")
st.write("Practice aptitude questions with explanations and formulas.")

# Load Questions File
questions_file = "aptitude_questions.csv"

if os.path.exists(questions_file):
    questions_df = pd.read_csv(questions_file)
else:
    st.error("Questions file not found!")
    st.stop()

# Progress File
progress_file = "student_progress.csv"

if not os.path.exists(progress_file):

    progress_df = pd.DataFrame(columns=[
        "Question_ID",
        "Selected_Answer",
        "Correct_Answer",
        "Result"
    ])

    progress_df.to_csv(progress_file, index=False)

# Session State Initialization
if 'score' not in st.session_state:
    st.session_state.score = 0

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'answered' not in st.session_state:
    st.session_state.answered = False

# Total Questions
total_questions = len(questions_df)

# Quiz Completed
if st.session_state.question_index >= total_questions:

    st.success("🎉 Quiz Completed!")

    st.write(
        f"Final Score: {st.session_state.score}/{total_questions}"
    )

    percentage = (
        st.session_state.score / total_questions
    ) * 100

    st.write(f"Percentage: {percentage:.2f}%")

    if percentage >= 80:
        st.success("Excellent Performance!")

    elif percentage >= 50:
        st.info("Good Job! Keep Practicing.")

    else:
        st.warning("Need More Practice.")

    # Restart Button
    if st.button("Restart Quiz"):

        st.session_state.score = 0
        st.session_state.question_index = 0
        st.session_state.answered = False

        st.rerun()

    st.stop()

# Current Question
current_question = questions_df.iloc[
    st.session_state.question_index
]

# Display Question
st.subheader(
    f"Question {st.session_state.question_index + 1}"
)

st.write(current_question['question'])

# Options
options = [
    current_question['option_a'],
    current_question['option_b'],
    current_question['option_c'],
    current_question['option_d']
]

# Select Option
selected_option = st.radio(
    "Choose your answer:",
    options
)

# Submit Answer
if st.button("Submit Answer"):

    correct_answer = current_question['correct_answer']

    # Correct Answer
    if selected_option == correct_answer:

        st.success("✅ Correct Answer")

        st.session_state.score += 1

        result = "Correct"

    # Wrong Answer
    else:

        st.error("❌ Wrong Answer")

        result = "Wrong"

    # Show Explanation
    st.write(f"Correct Answer: {correct_answer}")

    st.info(
        f"Explanation: {current_question['explanation']}"
    )

    st.warning(
        f"Formula: {current_question['formula']}"
    )

    # Save Progress
    progress_data = {
        "Question_ID": current_question['id'],
        "Selected_Answer": selected_option,
        "Correct_Answer": correct_answer,
        "Result": result
    }

    progress_df = pd.read_csv(progress_file)

    progress_df = pd.concat([
        progress_df,
        pd.DataFrame([progress_data])
    ], ignore_index=True)

    progress_df.to_csv(progress_file, index=False)

    # Answer Submitted
    st.session_state.answered = True

# Next Question Button
if st.session_state.answered:

    if st.button("Next Question"):

        st.session_state.question_index += 1

        st.session_state.answered = False

        st.rerun()

# Sidebar
st.sidebar.title("📊 Student Progress")

st.sidebar.write(
    f"Score: {st.session_state.score}"
)

st.sidebar.write(
    f"Completed: {st.session_state.question_index}/{total_questions}"
)