import streamlit as st
from quiz_db import create_connection
from datetime import datetime, timezone
from quesgen.settings.app_config import AppSettings, Page
import pytz
import pandas as pd

def admin_dashboard():
    st.title("Admin Dashboard")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["User Details", "User Activity", "Quiz_Not_Fine_Tuned", "Quiz_Fine_Tuned", "Fine_Tuned_retake", "Score_of_Non_Fine_turned", "Feedback_and_score_fine_turned_and_retake"])

    with tab1:
        show_user_details()

    with tab2:
        show_user_activity()
    with tab3:
        show_quiz_details()
    with tab4:
        show_quiz_fine()
    with tab5:
         show_quiz_retake()
    with tab6:
         show_score_non_fine_turned()
    with tab7:
         show_feedback_score()

def show_score_non_fine_turned():
     conn = create_connection()
     cursor = conn.cursor(dictionary=True)
     query = """
     SELECT 
       user_id,
       username,
       quiz_id,
       quiz_type,
       score
     FROM score_details
     """
     
     cursor.execute(query)
     result = cursor.fetchall()
     
     if result:
        df = pd.DataFrame(result, columns = ["user_id", "username", "quiz_id", "quiz_type", "score"])
        df.insert(0, "S.No", range(1, len(df)+1))
        df = df.reset_index(drop=True)
        st.dataframe(df)
     
     cursor.close()
     conn.close()

def show_feedback_score():

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT
       f.username,
       f.quiz_id,
       f.user_id,
       f.score AS Fine_Tuned_Score,
       f.overall_feedback_msg AS Feedback,
       f.remember_perc AS REMEMBER,
       f.understand_perc AS UNDERSTAND,
       f.apply_perc AS APPLY,
       f.analyze_perc AS ANALYZE_LEVEL,
       f.evaluate_perc AS EVALUATE,
       f.create_perc AS CREATE_LEVEL,
       s.score AS Fine_Tuned_Retake_score,
       s.remember_perc AS REMEMBER_RETAKE,
       s.understand_perc AS UNDERSTAND_RETAKE,
       s.apply_perc AS APPLY_RETAKE,
       s.analyze_perc AS ANALYZE_RETAKE,
       s.evaluate_perc AS EVALUATE_RETAKE,
       s.create_perc AS CREATE_RETAKE
    FROM feedback f
    LEFT JOIN score_retake s
    ON s.quiz_id = f.quiz_id AND s.user_id = f.user_id
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
       df = pd.DataFrame(result)
       #df.columns = ["Name", "Quiz_id", "User_id","Fine_Tuned_score"," Feedback","REMEMBER","UNDERSTAND","APPLY", "ANALYZE","EVALUATE","CREATE","Fine_Tuned_Retake_score", "REMEMBER_RETAKE","UNDERSTAND_RETAKE","APPLY_RETAKE","ANALYZE_RETAKE","EVALUATE_RETAKE","CREATE_RETAKE"]
       df.insert(0, "S.No", range(1, len(df) +1))
       df = df.reset_index(drop=True)
       st.dataframe(df)
    
    cursor.close()
    conn.close()
    
    
def show_user_details():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # 3. Execute SQL query to get user details
        cursor.execute("SELECT name, email, registered_at FROM users")
        rows = cursor.fetchall()
        if rows:
            # 6. Convert the rows to a pandas DataFrame for easy display
            df = pd.DataFrame(rows, columns=["Name", "Email", "Registered At"])
            df.insert(0, "S.No", range(1, len(df) +1))
            df = df.reset_index(drop=True)
            st.dataframe(df)
        else:
            st.info("No user records found.")

    finally:
        cursor.close()
        conn.close()

def show_user_activity():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Get all distinct usernames for the dropdown
        cursor.execute("SELECT DISTINCT username FROM login_logs")
        usernames = [row[0] for row in cursor.fetchall()]

        if not usernames:
            st.info("No login activity found.")
            return

        usernames.insert(0, "All users")
        selected_user = st.selectbox("Select a user to view login activity:", usernames)

        if selected_user == "All users":
           query = """
                SELECT l.user_id, l.username, u.registered_at, l.login_time, l.quiz_type, l.quiz_started_time, l.quiz_end_time
                FROM login_logs l
                LEFT JOIN users u
                   ON l.user_id = u.id
                ORDER BY login_time DESC
            """
           params = ()
            
        else:
             query = """
                  SELECT l.user_id, l.username, u.registered_at,l.login_time, l.quiz_type, l.quiz_started_time, l.quiz_end_time
                  FROM login_logs l
                  LEFT JOIN users u
                     ON l.user_id = u.id
                  WHERE l.username = %s 
                  ORDER BY login_time DESC
             """
             params = (selected_user,)
             
        cursor.execute(query, params) 
        logs = cursor.fetchall()

        if logs:
            df = pd.DataFrame(logs, columns=["user_id" , "Username", "Registered_at","Login Time", "quiz_type", "quiz_started_time","quiz_end_time"])
            df.insert(0, "S.No", range(1, len(df) +1))
            df = df.reset_index(drop=True)
            st.dataframe(df)
        else:
            st.info("No activity found for the selected user.")

    finally:
        cursor.close()
        conn.close()
        
        
def show_quiz_details():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT q1.quiz_id, q1.id AS user_id, q1.username, q1.question_no, q1.questions, q1.answer, q1.correct_or_not,q1.cosine_similarity, q1.topic, q1.difficulty_level, q1.start_time, q1.end_time
        from quiz_details q1
        INNER JOIN (
              SELECT quiz_id, question_no, MAX(end_time) AS max_end_time
              FROM quiz_details
              GROUP BY quiz_id, question_no
        ) q2
        ON q1.quiz_id = q2.quiz_id AND q1.question_no = q2.question_no AND q1.end_time = q2.max_end_time;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        df =pd.DataFrame(rows, columns=["Quiz_id","User id", "Username", "Question Number", "Questions", "Answer", "correct_or_not","cosine_similarity","Topic", "Difficulty_level", "Start_time", "End_time"])
        df.insert(0, "S.No", range(1, len(df)+1))
        st.dataframe(df)
    finally:
        cursor.close()
        conn.close()
        
        
        
def show_quiz_fine():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT q1.quiz_id, q1.id AS user_id, q1.username, q1.question_no, q1.questions, q1.answer, q1.correct_or_not,q1.cosine_similarity,q1.difficulty_level, q1.start_time, q1.end_time
        from quiz_details_fine q1
        INNER JOIN (
              SELECT quiz_id, question_no, MAX(end_time) AS max_end_time
              FROM quiz_details_fine
              GROUP BY quiz_id, question_no
        ) q2
        ON q1.quiz_id = q2.quiz_id AND q1.question_no = q2.question_no AND q1.end_time = q2.max_end_time;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        df =pd.DataFrame(rows, columns=["Quiz_id","User id", "Username", "Question Number", "Questions", "Answer", "correct_or_not","cosine_similarity","bloom_level", "Start_time", "End_time"])
        df.insert(0, "S.No", range(1, len(df)+1))
        st.dataframe(df)
    finally:
        cursor.close()
        conn.close()

def show_quiz_retake():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT q1.quiz_id, q1.user_id, q1.username,q1.question_no, q1.questions, q1.answer, q1.correct_or_not,q1.cosine_similarity,q1.difficulty_level, q1.start_time, q1.end_time
        from quiz_details_retake q1
        INNER JOIN (
              SELECT quiz_id, question_no, MAX(end_time) AS max_end_time
              FROM quiz_details_retake
              GROUP BY quiz_id, question_no
        ) q2
        ON q1.quiz_id = q2.quiz_id AND q1.question_no = q2.question_no AND q1.end_time = q2.max_end_time;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        df =pd.DataFrame(rows, columns=["Quiz_id","User id", "Username", "Question Number", "Questions", "Answer", "correct_or_not","cosine_similarity","difficulty_level", "Start_time", "End_time"])
        df.insert(0, "S.No", range(1, len(df)+1))
        st.dataframe(df)
    finally:
        cursor.close()
        conn.close()