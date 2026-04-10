import streamlit as st

from quesgen.settings.app_config import Page


def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">👋</div>
            <div style="font-size: 0.875rem; opacity: 0.8; margin-bottom: 4px;">Welcome</div>
            <div style="font-size: 1.25rem; font-weight: 500;">{st.session_state.username}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Navigation buttons
        nav_items = [
            ("⚙️", "Configure Quiz T5" , Page.CONFIGURE), 
            ("⚙️", "Configure Quiz T5 Fineturned" , Page.CONFIGURE_FINE) 
        ]


        for icon, label, page in nav_items:
            if st.button(f"{icon} {label}", use_container_width=True, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()

        st.markdown("---")

        # Quick stats
        if st.session_state.quiz_history:
            total_quizzes = len(st.session_state.quiz_history)
            avg_score = sum([quiz["percentage"] for quiz in st.session_state.quiz_history]) / total_quizzes

            st.markdown(
                f"""
                <div class="instructions-card">
                    <h4>📈 Quick Stats</h4>
                    <ul style="line-height: 1.8;">
                        <li><strong>Total Quizzes:</strong> {total_quizzes}</li>
                        <li><strong>Average Score:</strong> {avg_score:.1f}%</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.page = Page.LOGIN
            st.rerun()
