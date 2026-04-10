import streamlit as st
from quiz_db import create_connection
import mysql.connector
from mysql.connector import IntegrityError
from datetime import datetime, timezone
from quesgen.settings.app_config import AppSettings, Page
import pytz

def login_page():
    st.markdown(
        '<h1 class="material-headline">{}</h1>'.format(AppSettings.app_name),
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="material-subtitle">{}</p>'.format(AppSettings.description),
        unsafe_allow_html=True,
    )
    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            '<h3 style="text-align: center; margin-bottom: 2rem; color: #1976d2;">🔐 User Authentication</h3>',
            unsafe_allow_html=True,
        )

        # Login form
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 LOGIN", use_container_width=True, type="primary", key="login_submit"):
                if username and password:
                    try:
                       conn = create_connection()
                       cursor = conn.cursor()
                       query = "SELECT * FROM users WHERE username = %s AND password = %s"
                       cursor.execute(query,(username,password))
                       user = cursor.fetchone()
                       
                       if user:
                            last_login = user[8]
                            user_id = user[0]
                            is_admin = user[9]
                            ist = pytz.timezone('Asia/Kolkata')
                            local_time = datetime.now(ist)
                            cursor.execute("UPDATE users SET last_login = %s WHERE username = %s", (local_time, username,))
                            cursor.execute("INSERT INTO login_logs (username, login_time, user_id) VALUES (%s, %s, %s)",(username, local_time, user_id))
                            conn.commit()
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.userid = user_id
                            st.session_state.is_admin = is_admin
                            st.success("Login sucessful!")
                            if is_admin:
                               st.write("Page.ADMIN_DASHBOARD:" , Page.ADMIN_DASHBOARD)
                               st.session_state.page = Page.ADMIN_DASHBOARD
                            else:
                               st.session_state.page = Page.UPLOAD
                            st.session_state.show_login_sucess = True
                            st.rerun()
                       else:
                            st.error("Invalid credentials")
                            
                    except Exception as e:
                        st.error(f"Database error: {e}")
                    finally:
                        if 'cursor' in locals():
                            cursor.close()
                        if 'conn' in locals():
                            conn.close()
                else:
                   st.error("Please enter both username and password")
                       

        with col_b:
            if st.button("👤 REGISTER", use_container_width=True, key="register_btn"):
                #st.info("🚧 Registration feature coming soon!")
                st.session_state.page = Page.REGISTER

       
