import streamlit as st

from quesgen.settings.app_config import AppSettings, Page


def login_page():
    st.markdown(
        '<h1 class="material-headline">🎓 {}</h1>'.format(AppSettings.app_name),
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
                    if username == "admin" and password == "password":
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.page = Page.UPLOAD
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials! Try admin/password")
                else:
                    st.error("⚠️ Please enter both username and password")

        with col_b:
            if st.button("👤 REGISTER", use_container_width=True, key="register_btn"):
                st.info("🚧 Registration feature coming soon!")

        # Demo credentials
        st.markdown(
            """
        <div class="material-success" style="margin-top: 2rem;">
            <h4 style="margin: 0 0 12px 0;">🎮 Demo Credentials</h4>
            <p style="margin: 0; font-family: monospace; font-size: 0.9rem;">
                <strong>Username:</strong> admin<br>
                <strong>Password:</strong> password
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

