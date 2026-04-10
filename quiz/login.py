import streamlit as st

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "front"

if "users" not in st.session_state:
    # Simple in-memory user "database"
    st.session_state.users = {}

def front_page():
    st.title("🎓 Quiz Platform")
    st.write("Welcome to the Quiz Platform. Please login or register to continue.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            st.session_state.page = "login"
            st.experimental_rerun()

    with col2:
        if st.button("Register"):
            st.session_state.page = "register"
            st.experimental_rerun()

def login_page():
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.session_state.users
        if username in users and users[username]["password"] == password:
            st.success(f"Welcome back, {users[username]['name']}!")
            st.session_state.page = "dashboard"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Back to Home"):
        st.session_state.page = "front"
        st.experimental_rerun()

def register_page():
    st.header("👤 Register")

    name = st.text_input("Name")
    degree = st.text_input("Degree")
    stream = st.text_input("Stream")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not (name and degree and stream and email and username and password):
            st.error("Please fill in all fields")
        elif username in st.session_state.users:
            st.error("Username already exists")
        else:
            # Save user data
            st.session_state.users[username] = {
                "name": name,
                "degree": degree,
                "stream": stream,
                "email": email,
                "password": password,
            }
            st.success("Registration successful! You can now log in.")
            st.session_state.page = "login"
            st.experimental_rerun()

    if st.button("Back to Home"):
        st.session_state.page = "front"
        st.experimental_rerun()

def dashboard_page():
    st.header("🏠 Dashboard")
    st.write(f"Welcome {st.session_state.users[st.session_state.get('username', '')]['name']}!")

    if st.button("Logout"):
        st.session_state.page = "front"
        st.experimental_rerun()

# Main app logic
if st.session_state.page == "front":
    front_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "dashboard":
    dashboard_page()

