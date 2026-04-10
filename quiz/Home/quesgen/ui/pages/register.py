import streamlit as st
from quesgen.settings.app_config import Page
from quiz_db import create_connection  
import mysql.connector
from mysql.connector import IntegrityError
from datetime import datetime, timezone
import pytz

def register_page():

    st.markdown("<h1 style='text-align: center;'>User Registration</h1>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 2, 1])
    with center:
        name = st.text_input("Full Name")
        degree = st.text_input("Degree")
        stream = st.text_input("Stream")
        email = st.text_input("Email Address")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        st.markdown("### ")
        register_btn = st.button("\U0001F4DDRegister", use_container_width=True)



    if register_btn:
        # Basic validation
        if not all([name, degree, stream, email, username, password, confirm_password]):
            st.error("Please fill in all fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
          try:
            conn = create_connection()
            cursor = conn.cursor()
            ist = pytz.timezone('Asia/Kolkata')
            local_time = datetime.now(ist)
            insert_query = """
                INSERT INTO users (name, degree, stream, email, username, password, registered_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

            cursor.execute(insert_query, (name, degree, stream, email, username, password, local_time))
            conn.commit()
            inserted_id = cursor.lastrowid
            insert_login_log_query = """
                   INSERT INTO login_logs (username, login_time, user_id)
                   VALUES (%s, %s, %s)
            """
            cursor.execute(insert_login_log_query, (username, None, inserted_id))
            conn.commit()
            # Here you would save user info to your DB or file
            st.success(f"User {username} registered successfully!")
            st.session_state.authenticated = True
            st.session_state.userid = inserted_id
            st.session_state.username = username
            st.session_state.page = Page.UPLOAD  
            st.query_params = {"page":"quiz"}
            st.rerun()
            
          except mysql.connector.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    st.error("Email or username already exists.")
                else:
                    st.error(f"MySQL Error: {e}")
          except Exception as e:
                st.error(f"Unexpected error: {e}")
          finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()