import streamlit as st
from quiz_db import create_connection
from quesgen.settings.app_config import Page
from quesgen.settings.mock import evaluate_answer
import time
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import IntegrityError
from streamlit_autorefresh import st_autorefresh
import pytz
from pytz import timezone
from quesgen.ui.sidebar import render_sidebar
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit.components.v1 as components
import pandas as pd

def final():
     quiz_id = st.session_state.quiz_id
     user_id = st.session_state.userid
     username = st.session_state.username
     
     st.markdown(f""" 
           <div style="text-align:center;">
           <h2>
            Quiz Summary
           </h2>
           </div>
           """,
           unsafe_allow_html=True )
     try :
       conn = create_connection()
       cursor = conn.cursor()
       
       
       query = """
                  SELECT score
                  FROM score_details_fine
                  WHERE quiz_id = %s AND user_id = %s 
             """
       params = (quiz_id,user_id,)
       cursor.execute(query, params) 
       total = cursor.fetchone()
       total_result =total[0]
       
       query = """
                  SELECT number_of_questions
                  FROM quiz_configuration_fine
                  WHERE quiz_id = %s AND user_id = %s
              """
       params = (quiz_id, user_id,)
       cursor.execute(query, params)
       num = cursor.fetchone()
       num_result = num[0]
       
       per =(total_result / num_result) * 100
       
       st.markdown(
             f"""
             <div style="display:flex; justify-content:center; align-items:center; gap:20px;">
             <span style="font-size:28px; font-weight:600;">
             {st.session_state.username}
             </span>
             <span style="font-size:28px;  font-weight:700;"> 
             Your Total Score: {total_result}
             </span>
            </div>
            """,
            unsafe_allow_html = True
             )
       if per >=80:
          feedback_msg ="Good Score Keep it up"
          st.markdown(
           f""" 
           <div style="text-align:center;">
           <h3 style="color:green;">
           Good Score Keep it up
           </h3>
           </div>
           """,
           unsafe_allow_html=True )
           
       elif per<80 and per>=40:
          feedback_msg ="You Must work on the test"
          st.markdown(f"""
          <div style ="text-align:center;">
          <h3 style="color:orange";>
          You Must work on the test
          </h3>
          </div>
          """,
          unsafe_allow_html=True
          )
       elif per<40:
          feedback_msg ="Very poor performance, Need to improve"
          st.markdown(f"""
          <div style ="text-align:center;">
          <h3 style="color:red";>
           Very poor performance, Need to improve.
           </h3>
           </div>
           """,
           unsafe_allow_html=True
           )
     
       query = """
                  SELECT username, question_no, questions, answer, correct_or_not, difficulty_level, start_time, end_time, cosine_similarity
                  FROM quiz_details_fine
                  WHERE quiz_id = %s AND id = %s 
                  ORDER BY question_no
             """
       params = (quiz_id,user_id,)
       cursor.execute(query, params) 
       logs = cursor.fetchall() 
       df = pd.DataFrame(
           logs,
           columns=[
              "username",
              "question_no",
              "question",
              "answer",
              "correct_or_not",
              "difficulty_level",
              "start_time",
              "end_time",
              "cosine_similarity"
              ]
            )
   
       difficulty_summary = (
                df.groupby("difficulty_level")
                   .agg(
                        total_questions=("question_no", "count"),
                        correct_count=("correct_or_not", "sum")
                   )
                   .reset_index()
       )

       difficulty_summary["incorrect_count"] = (
           difficulty_summary["total_questions"] - difficulty_summary["correct_count"]
       )

       difficulty_summary["accuracy"] = (
            difficulty_summary["correct_count"] / difficulty_summary["total_questions"]
       )
       
       st.divider()
       st.markdown(
           f""" 
           <div style="text-align:left;">
           <h3 style="color:black;">
           Difficulty Level Summary
           </h3>
           </div>
           """,
           unsafe_allow_html=True )
       if not difficulty_summary.empty:
            cols = st.columns(len(difficulty_summary))
            for col, (_, row) in zip(cols, difficulty_summary.iterrows()):
               with col:
                  level = row["difficulty_level"]
                  accuracy = row["accuracy"]
                  st.markdown(f"{level.upper()}")
                  st.progress(float(accuracy))
                  st.write(f"{accuracy*100:.1f}%")
                  #if level == "remember":
                     #remember = accuracy*100
                  #elif level == "create":
                     #create = accuracy * 100
                  #elif level == "evaluate":
                     #evaluate = accuracy * 100
                  #elif level == "apply":
                      #applys = accuracy * 100
                  #elif level == "understand":
                      #understand = accuracy * 100
                     
                  if accuracy < 1 and accuracy > 0.5:
                      st.markdown(
                              f""" 
                              <p style="font-size: 10px; color:gray;">
                              Good effort, but additional improvement is needed on this topic
                            </p>
           
                             """,
                   unsafe_allow_html=True )
                   
                  elif accuracy == 1:
                    st.markdown(
                              f""" 
                              <p style="font-size: 10px; color:gray;">
                              Good effort, Keep it up
                              </p>
           
                             """,
                   unsafe_allow_html=True )
                  else:
                    st.markdown(
                              f""" 
                              <p style="font-size: 10px; color:gray;">
                              you have to work on this topic
                              </p>
           
                             """,
                   unsafe_allow_html=True )
       st.divider()
       difficulty_score = {
            "remember":None,
            "understand":None,
            "apply":None,
            "evaluate":None,
            "create":None,
            "analyze":None
       }
       for _,row in difficulty_summary.iterrows():
           level = row["difficulty_level"]
           accuracy = row["accuracy"]*100
           difficulty_score[level] = accuracy
       if "feedback_saved" not in st.session_state:
                  query = """
                         INSERT INTO feedback (quiz_id,user_id, username, score, overall_feedback_msg, remember_perc, understand_perc, apply_perc, evaluate_perc, create_perc, analyze_perc)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                         """
                  cursor.execute(query, (
                         quiz_id,
                         user_id,
                         username,
                         total_result,
                         feedback_msg,
                         difficulty_score["remember"],
                         difficulty_score["understand"],
                         difficulty_score["apply"],
                         difficulty_score["evaluate"],
                         difficulty_score["create"],
                         difficulty_score["analyze"],
                  ))
                  conn.commit()
                  st.session_state.feedback_saved = True
             
       #for _, row in difficulty_summary.iterrows():
             #level = row["difficulty_level"]
             #total = row["total_questions"]
             #correct = row["correct_count"]
             #incorrect = row["incorrect_count"]
             #accuracy = row["accuracy"]
             
             #st.markdown(f"{level.upper()}")
             #st.progress(float(accuracy))
             #st.write(f"Accuracy: {accuracy*100:.1f}%")
             #st. markdown("------")
       
       for _, row in df.iterrows():
             st.markdown(f"### Question {row['question_no']}")
             st.write("**Question:**", row["question"])
             st.write("**Answer:**", row["answer"])
             st.write("**Correct:**", row["correct_or_not"])
             st.write("**Difficulty Level:**", row["difficulty_level"])
             time_taken = (row["end_time"] - row["start_time"]).total_seconds()
             st.markdown("**Feedback:**")
             if row["cosine_similarity"]>0.80:
                st.markdown ("Keep it up")
                if time_taken >=150:
                   st.write ("you took too much time in this question. You have to go over the topics again to master them")
                else:
                   st.write("Wow! You are speedy, speed comes only with knowledge, looks like you understood these concepts well")
             else:
                st.write ("Need to work on it")
                if time_taken >=150:
                   st.write ("you took too much time in this question. You have to go over the topics again to master them")
                else:
                   st.write(" You are speed, But you need to improve the accuracy")
                
             #st.write("**Cosine Similarity:**", row["cosine_similarity"])
             st.divider()
     except Exception as e:
            st.error(f"Database error :{e}")
     finally:
           cursor.close()
           conn.close()
     if st.button("Retake Quiz"):
         for key in [
               "quiz_submitted",
               "quiz_started",
               "score_saved",
               "current_index",
               "answers",
               "correct_flags",
               "question_saved_flags",
               "next_clicked_flags",
               "question_start_times",
               "question_end_times"
         ]:
               if key in st.session_state:
                  del st.session_state[key]
         st.session_state.page = Page.FINAL_QUIZ
     