import random
import streamlit as st
from quesgen.settings.app_config import Difficulty, Page, QuizTimer
from quesgen.settings.mock import MOCK_QUESTIONS
from quesgen.ui.sidebar import render_sidebar
from quiz_db import create_connection  
import mysql.connector
from mysql.connector import IntegrityError
import json
import datetime



def session_quiz(userid, username):
    conn = create_connection()
    cursor =  conn.cursor()
    query = """
        INSERT INTO quiz_sessions_fine (user_id, username)
        VALUES (%s, %s)
        """
    cursor.execute(query, (
        userid,
        username,
    ))
    conn.commit()
    cursor.close()
    conn.close()
    
    
def fetch_quizid(userid):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        SELECT quiz_id 
        FROM quiz_sessions_fine
        WHERE user_id = %s
        ORDER BY quiz_id DESC
        LIMIT 1
        """
    cursor.execute(query, (userid,))
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        return result[0]
    else:
        return None
        
        

def save_quiz_config(user_id, username, number_of_questions, time_limit, quiz_id):
    conn = create_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO quiz_configuration_fine (user_id, username, number_of_questions, time_limit, quiz_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        user_id,
        username,
        number_of_questions,
        time_limit,
        quiz_id,
       
    ))

    conn.commit()
    cursor.close()
    conn.close()


def quiz_type(userid):
    conn = create_connection()
    cursor = conn.cursor()
    
    select_sql = """
    SELECT session_id
    FROM login_logs
    WHERE user_id = %s
    ORDER BY login_time DESC
    LIMIT 1
    """
    cursor.execute(select_sql,(userid,))
    result = cursor.fetchone()
    if result:
        session_id = result[0]
        update_sql = """
        UPDATE login_logs
        SET quiz_type = %s
        WHERE session_id = %s
        """
        cursor.execute(update_sql, ("Fine Tuned", session_id))
        conn.commit()
    else:
        print("no login session found for user")
    cursor.close()
    conn.close()

# Main configuration page
def configure_fine():
    st.markdown("<h3 class='material-section-title'>Configure Quiz T5 Fine Turned</h3>", unsafe_allow_html=True)
    render_sidebar()
    #username = st.text_input("Enter your username")
    user_id = st.session_state.userid
    username = st.session_state.username
    start_time = datetime.datetime.now()
    number_of_questions = st.slider(
        "Number of Questions",
        min_value=5,
        max_value=20,
        value=st.session_state.get("num_questions", 5),
        help="Choose how many questions to generate",
    )
    st.session_state.number_of_questions = number_of_questions
    
    #difficulty = st.selectbox(
        #"Difficulty Level",
        #[d.value for d in Difficulty],
        #index=[d.value for d in Difficulty].index(
            #st.session_state.get("difficulty", Difficulty.EASY.value)
        #),
        #help="Select the difficulty level for questions",
    #)
    #st.session_state.difficulty = difficulty

    time_limit = st.selectbox(
        "select time to complete the quiz( in minutes)(select 0 for unlimited time mode)",
        [timer.value for timer in QuizTimer],
        help="Set time limit per question",
    )

    if st.button("Start Quiz"):
            # ? Save to DB
            session_quiz(st.session_state.userid,st.session_state.username)
            st.session_state.quiz_id = fetch_quizid(st.session_state.userid)
            save_quiz_config(user_id,username, number_of_questions, time_limit,st.session_state.quiz_id)
            quiz_type(user_id)
            # ?? Store in session state
            st.session_state.username = username
            st.session_state.number_of_questions = number_of_questions
            st.session_state.time_limit = time_limit
            st.session_state.quiz_type = "Fine Tuned"

            # ?? Redirect
            st.success("Quiz configuration saved. Redirecting...")
            st.session_state.page = Page.QUIZ_FINE
            st.rerun()
