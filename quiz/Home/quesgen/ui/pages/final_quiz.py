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


#model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('paraphrase-mpnet-base-v2')

  
def save_questions(quiz_id, userid, username, questions, answer, correct_or_not, difficulty_level, start_time, end_time, question_no,cosine_similarity):
    conn =  create_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO quiz_details_retake (quiz_id,user_id, username, questions, answer,correct_or_not, difficulty_level, start_time, end_time, question_no, cosine_similarity)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(query, (
        quiz_id,
        userid,
        username,
        questions,
        answer,
        correct_or_not,
        difficulty_level,
        start_time,
        end_time,
        question_no,
        cosine_similarity
    ))

    conn.commit()
    cursor.close()
    conn.close()


def insert_time(username,userid):
    conn = create_connection()
    cursor = conn.cursor()
    
    ist = pytz.timezone('Asia/kolkata')
    ist_time = datetime.now(ist)
    
    insert_sql = """
    INSERT INTO login_logs (username, login_time, user_id, quiz_started_time,quiz_type)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_sql, (username, ist_time, userid, ist_time,"fine_tuned_retake"))
    conn.commit()
    cursor.close()
    conn.close()
    

def insert_end(end_time, userid):
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
        SET quiz_end_time = %s
        WHERE session_id = %s
        """
        cursor.execute(update_sql,(end_time,session_id))
        conn.commit()
    else:
        print("no login session found for user")
    cursor.close()
    conn.close()
    
    
def session_quiz(quiz_id,userid, username):
    conn = create_connection()
    cursor =  conn.cursor()
    query = """
        INSERT INTO retake_session (quiz_id,user_id, username)
        VALUES (%s, %s, %s)
        """
    cursor.execute(query, (
        quiz_id,
        userid,
        username,
    ))
    conn.commit()
    cursor.close()
    conn.close()
#def fetch_quizid(userid):
    #conn = create_connection()
    #cursor = conn.cursor()
    #query = """
        #SELECT quiz_id 
        #FROM quiz_sessions_fine
        #WHERE user_id = %s
        #ORDER BY quiz_id DESC
        #LIMIT 1
        #"""
    #cursor.execute(query, (userid,))
    #result = cursor.fetchone()
    #cursor.close()
    
    #if result:
        #return result[0]
    #else:
        #return None
    
# Fetch random questions with level/topic based on user input count
def fetch_questions(quiz_id, user_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT question_no,questions,difficulty_level
        FROM quiz_details_fine
        WHERE quiz_id = %s
        AND id = %s
        ORDER BY question_no ASC
    """
    cursor.execute(query, (quiz_id, user_id))
    results = cursor.fetchall()
    conn.close()
    return results

def similarity_check(static_answer,user_answer):
    vec_static = model.encode([static_answer])
    vec_user = model.encode([user_answer])
    similarity_score = cosine_similarity(vec_static, vec_user)[0][0]
    if similarity_score>0.80:
        return similarity_score,1
    else:
        return similarity_score,0

def score_details(user_id,username,quiz_id,quiz_type,score):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
         INSERT INTO score_retake (user_id,username,quiz_id,quiz_type,score) VALUES (%s,%s,%s,%s,%s)
         """
    cursor.execute(query,(user_id,username,quiz_id,quiz_type,score))
    conn.commit()
    cursor.close()
    conn.close()

def get_static_answer(question_text):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
            SELECT answer
            FROM questions_fine_tuned
            WHERE question_text = %s
            LIMIT 1
      """
    cursor.execute(query, (question_text,))
    result =  cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
       return result[0]
    else:
       None

def final_quiz():
    #st_autorefresh(interval=1000, key="quiz_timer_refresh")
    st.markdown(
    """
    <h1 style='text-align: center; color: black;'>
        AI based Quiz Generation Platform
    </h1>
    """,
    unsafe_allow_html=True
   )
    MAX_WORDS = 250
    if not st.session_state.get("quiz_submitted",False):
        render_sidebar()
    ist = pytz.timezone('Asia/Kolkata')
    
    #st.markdown(f"Username:`{st.session_state.username}`")
    #st.markdown(f"Time Limit:`{st.session_state.time_limit} minutes`")
    #st.markdown(f"id:`{st.session_state.userid}`")
    #st.markdown(f"id:`{st.session_state.number_of_questions}`")
    
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
        #idx = 0;
    if "score_saved" not in st.session_state:
        st.session_state.score_saved = False
    if st.session_state.quiz_submitted:
       #st.success("Quiz submitted successfully!")
       total_score = sum(st.session_state.correct_flags) 
       #st.write(st.session_state.correct_flags)
       st.success(f"Quiz submitted successfully! Your total score is: {total_score} / {len(st.session_state.questions)}")
       if not st.session_state.score_saved:
              score_details(st.session_state.userid,st.session_state.username,st.session_state.quiz_id,"fine_tuned_retake",total_score)
              st.session_state.score_saved = True
              st.session_state.page = Page.RETAKE_SCORE
              st.rerun()
       #for i, q in enumerate(st.session_state.questions):
            #st.markdown(f"**Q{i+1}:** {q['questions']}")
            #st.write(f"Your answer: {st.session_state.answers[i]}")
            #st.write(f"Level: {q['difficulty_level']}")
            #st.markdown("---")
       
       #if st.button("Back to Home"):
          #st.session_state.quiz_submitted = False
          #st.session_state.current_index = 0
          #st.session_state.score_saved = False
          #st.session_state.page = "home"
          #st.rerun()
       st.stop()
    if "quiz_started" not in st.session_state or not st.session_state.quiz_started:
        st.session_state.quiz_started = True
        session_quiz(st.session_state.quiz_id,st.session_state.userid,st.session_state.username)
        if "retake_logged" not in st.session_state:
            insert_time(st.session_state.username,st.session_state.userid)
            st.session_state.retake_logged = True
        #st.session_state.quiz_id = fetch_quizid(st.session_state.userid)
        st.session_state.questions = fetch_questions(st.session_state.quiz_id,st.session_state.userid)
        total_questions = len(st.session_state.questions)
        st.session_state.current_index = 0
        st.session_state.answers = [""] * total_questions
        if "question_saved_flags" not in st.session_state:
            st.session_state.question_saved_flags = [False] * total_questions
        if "next_clicked_flags" not in st.session_state:
            st.session_state.next_clicked_flags = [False] * total_questions
        if "correct_flags" not in st.session_state:
            st.session_state.correct_flags = [0] * total_questions
        st.session_state.question_start_times = [None] * total_questions
        st.session_state.question_end_times = [None] * total_questions
        st.session_state.start_time = datetime.now()
        ist = timezone('Asia/Kolkata')
        st.session_state.local_time = st.session_state.start_time.astimezone(ist)
        #insert_time(st.session_state.username,st.session_state.userid)
        if int(st.session_state.time_limit) > 0:
           st.session_state.end_time = st.session_state.start_time + timedelta(minutes=int(st.session_state.time_limit))
    if st.session_state.get("quiz_started", False) and not st.session_state.get("quiz_submitted", False):
        #st_autorefresh(interval=1000, key="quiz_timer_refresh")
        col1, col2, col3 = st.columns([2, 4, 2])
        if "end_time" in st.session_state and int(st.session_state.time_limit) > 0:
           now = datetime.now()
           remaining_time = st.session_state.end_time - now
 
           if remaining_time.total_seconds() < 0:
              with col3:
                   st.warning("Time's up! Submitting quiz...")
                   st.session_state.quiz_started = False
                   st.session_state.quiz_submitted = True
                   st.rerun()
           else:
               with col3:
                    mins, secs = divmod(int(remaining_time.total_seconds()), 60)
                   # st.info(f"Time Remaining: {mins:02d}:{secs:02d}")
        else:
             with col3:
                 st.info("Unlimited time mode")
    time_limit_minutes = int(st.session_state.time_limit)
    if time_limit_minutes ==0:
       st.info("Unlimited time mode")
    else:
       now = datetime.now()
       remaining_time = (st.session_state.end_time - now).total_seconds()
       remaining_seconds = max(int(remaining_time),0)

       timer_html =f"""
<div id="timer" style="font-size:24px; font-weight:bold;"></div>
<script>
    var timeLimit = {remaining_seconds};  // seconds
    function startTimer(duration, display) {{
        var timer = duration, minutes, seconds;
        var interval = setInterval(function () {{
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = "Time Remaining: " + minutes + ":" + seconds;

            if (--timer < 0) {{
                clearInterval(interval);
                display.textContent = "Time's up!";
                // Optionally send event to Streamlit here
            }}
        }}, 1000);
    }}

    window.onload = function () {{
        var display = document.getElementById("timer");
        startTimer(timeLimit, display);
    }};
</script>
"""

       st.components.v1.html(timer_html, height=50)    

    total_questions = len(st.session_state.questions)
    idx = st.session_state.current_index
    q = st.session_state.questions[idx]
    #static_answer = get_static_answer(q['questions'])
    #st.markdown(f"**Question {idx + 1} of {len(st.session_state.questions)}**")
    #st.write(f"Topic: {q['topic']}")
    #st.write(f"Level: {q['difficulty_level']}")
    #st.write(q["question_text"])
    st.markdown(f"""
          <div style='text-align:center; font-size:24px; font-weight:bold;'>
               Question {idx +1} of {len(st.session_state.questions)}
          <div>
          <div style='text-align:center; font-size:18px; margin-top:5px;'>
               Level: {q['difficulty_level']}
          </div>
          <div style='text-align:center; font-size:22px; margin:20px 0;'>
               {q["questions"]}
          </div>
     """, unsafe_allow_html=True)
     
    if st.session_state.question_start_times[idx] is None:
       st.session_state.question_start_times[idx] = datetime.now()
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
         st.markdown("""
               <style>
               div[data-testid="stTextInput"]> div > input{
                   height:60px;
                   font-size:20px;
                   text-align:center;
               }
               div[data-testid="stTextArea"] textarea {
                  height : 150px;
                  font-size:22px;
                  text-align:center;
                  border: 3px solid #4CAF50;
                  border-radius: 10px;
                  background-color: #f9f9f9;
               }
               div[data-testid="stTextArea"] small,
               div[data-baseweb="textarea"] small {
                  visibility: hidden !important;
                  display: none !important;
               }
               label[for^="answer_input_"]}
                    display:block;
                    text-align:center;
                    font-size:38px;
                    margin-bottom:10px;
               }
               </style>
         """, unsafe_allow_html=True)
         #ans = st.text_input("your answer:", value=st.session_state.answers[idx], key=f"answer_input_{idx}")
         ans = st.text_area("your answer:", value=st.session_state.answers[idx],height=150, key=f"answer_input_{idx}")
    warn =st.empty()
    word_count = len(ans.split())
    if word_count > MAX_WORDS:
       trimmed_ans =" ".join(ans.split()[:MAX_WORDS])
       st.session_state.answers[idx] = trimmed_ans
       st.warning(f" Limit reached only the first {MAX_WORDS} words were kept")
       time.sleep(3)
       warn.empty()
    else:
        st.session_state.answers[idx] = ans
    def next_question():
        idx = st.session_state.current_index
        q = st.session_state.questions[idx]
        question_text = q['questions']
        difficulty_level = q['difficulty_level']
        
        static_answer = get_static_answer(question_text)
        if static_answer is None:
           static_answer= ""
        user_answer = st.session_state.answers[idx]
        score, match = similarity_check(static_answer,user_answer)
        
        start_time_utc=st.session_state.question_start_times[idx]
        end_time_utc=st.session_state.question_end_times[idx]
        st.session_state.correct_flags[idx] = int(match)
        if not st.session_state.question_saved_flags[idx]:
              st.session_state.question_end_times[idx] = datetime.now()
              end_time_utc = st.session_state.question_end_times[idx]
              #q = st.session_state.questions[idx]
              save_questions(
                   quiz_id=st.session_state.quiz_id,
                   userid=st.session_state.userid,
                   username=st.session_state.username,
                   questions=q['questions'],
                   answer=st.session_state.answers[idx],
                   correct_or_not=bool(match),
                   difficulty_level=q['difficulty_level'],
                   start_time=start_time_utc.astimezone(ist),
                   end_time=end_time_utc.astimezone(ist),
                   question_no=idx + 1,
                   cosine_similarity = float(score)
              )
              st.session_state.question_saved_flags[idx] = True
        if idx < len(st.session_state.questions) - 1:
           st.session_state.current_index += 1
           st.session_state.next_clicked = False 
           #st.rerun()

    col1, col2, col3 = st.columns([2,4,2])
 
    with col3:
       if st.session_state.current_index < len(st.session_state.questions) -1:
             st.markdown("""
                 <style>
                     div[data-testid="stButton"]{
                         display:flex;
                         justify-content:center;
                     }
                     div[data-testid="stButton"] > button {
                         font-size: 18px;
                         padding: 10px 24 px;
                         border-radius: 8px;
                         color:white;
                         font-weight:bold;
                     }
                 </style>
              """,unsafe_allow_html=True)
             st.button("Next", on_click=next_question)
             st.markdown("</div>", unsafe_allow_html=True)
     # if st.button("Next") and idx < total_questions -1 :
         #if not st.session_state.question_saved_flags[idx]:
            #st.session_state.question_end_times[idx] = datetime.now()
            #start_q = st.session_state.question_start_times[idx]
            #end_q = st.session_state.question_end_times[idx]
            #save_questions(
                 #quiz_id=st.session_state.quiz_id,
                 #userid=st.session_state.userid,
                 #username=st.session_state.username,
                 #questions=q['question_text'],
                 #answer=st.session_state.answers[idx],
                 #correct_or_not=False,
                 #topic=q['topic'],
                 #difficulty_level=q['difficulty_level'],
                 #start_time = start_q,
                 #end_time = end_q,
                 #question_no=idx + 1
             #)
            #st.session_state.question_saved_flags[idx] = True
         #st.session_state.current_index += 1
         #st.rerun()
        
    if idx == total_questions - 1:
       with col2:
         if st.button("Submit Quiz"):
            st.session_state.question_end_times[idx] = datetime.now()
            end_time_ist = datetime.now(ist)
            st.session_state.question_end_times[idx] = end_time_ist
            st.session_state.quiz_started = False  # or some other flag to show results
            st.session_state.quiz_submitted = True
            idx_cur = st.session_state.current_index
            st.session_state.question_end_times[idx_cur] =  datetime.now(ist)
            insert_end(st.session_state.question_end_times[idx_cur],st.session_state.userid)
            total = len(st.session_state.questions)
            for i, q in enumerate(st.session_state.questions):
              if st.session_state.question_saved_flags[i]:
                continue  # Already saved
              question_no = i +1
              question_text = q['questions']
              difficulty_level = q['difficulty_level']
              start_q = st.session_state.question_start_times[i]
              start_q_ist = start_q.astimezone(ist)
              end_q = st.session_state.question_end_times[i]
              if end_q is None:
                 end_q = datetime.now()
              static_answer = get_static_answer(question_text)
              user_answer = st.session_state.answers[i]
              score,match = similarity_check(static_answer,user_answer)
              st.session_state.correct_flags[i] = int(match)

              st.write(f"Saving question {i+1}/{len(st.session_state.questions)}: {question_text} ? answer: {user_answer}")
              save_questions(
                 quiz_id=st.session_state.quiz_id,
                 userid=st.session_state.userid,
                 username=st.session_state.username,
                 questions=question_text,
                 answer=user_answer,
                 correct_or_not=bool(match),
                 difficulty_level=difficulty_level,
                 start_time=start_q_ist,
                 end_time=end_q,
                 question_no=question_no,
                 cosine_similarity=float(score)
             )
            st.success("answers saved successfully!")
            #time.sleep(1)
            st.rerun()
 