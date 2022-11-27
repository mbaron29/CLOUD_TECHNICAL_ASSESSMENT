import streamlit as st
import pandas as pd
import random as rd

st.set_page_config(page_title="WEWYSE AWS TRAINING", page_icon="📚")
st.markdown("# 📚 WELCOME TO WEWYSE AWS TRAINING !")

@st.experimental_memo
def get_sample_question(data, nb_of_questions):
    return rd.sample(range(1, len(data)), nb_of_questions)

# get raw data
data = pd.read_excel("AWS_QUESTIONS.xlsx")

# ask the user how many questions he wants
n = st.number_input('How many questions do you want ?', step=1, min_value=1, max_value=len(data)-1)
st.write('You asked for ', n, ' questions.')

# get n questions
questions = get_sample_question(data, nb_of_questions=n)

# button to restart test
if st.sidebar.button("Restart test ? "):
    st.experimental_memo.clear()
    st.experimental_rerun()

submitted_answers = []
explanations = []

for i, question in enumerate(questions):

    # question number
    st.write("Question ", i + 1, " / ", n)

    # writing the question
    st.write(data["Question"][question])

    # writing options
    dico = {str(x) + " : " + str(data[x][question]): x for x in ['A', 'B', 'C', 'D'] if str(data[x][question]) != "nan"}
    options = [str(x) + " : " + str(data[x][question]) for x in ['A', 'B', 'C', 'D'] if str(data[x][question]) != "nan"]
    answer = st.radio('What is your answer ? ', options)
    if answer is not None:
        submitted_answers.append(dico[answer])
    explanation = st.empty()
    explanations.append(explanation)
    st.write("-----------------------------------")

submitted = st.sidebar.button(label="Submit answers")


if submitted:
    score = 0
    for i, answer in enumerate(submitted_answers):
        if data["Correct Answer"][questions[i]] == answer:
            score += 1
            with explanations[i].container():
                st.write("Correct !")
                st.write(data["Explanation"][questions[i]])
        else:
            with explanations[i].container():
                st.write("Wrong !")
                st.write("The correct answer was ", data["Correct Answer"][questions[i]])
                st.write(data["Explanation"][questions[i]])
    st.sidebar.write("Final score : ", score, " / ", n)
    st.sidebar.write("Accuracy percentage : ", round((score / n)*100, 3), " %")
