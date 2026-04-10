import streamlit as st

from quesgen.settings.app_config import (
    AppSettings,
    HtmlContent,
    Page,
    initialize_session_state,
)
from quesgen.ui.pages.configure import configure_page
from quesgen.ui.pages.history import history_page
from quesgen.ui.pages.login import login_page
from quesgen.ui.pages.manage_files import manage_files_page
from quesgen.ui.pages.quiz import quiz_page
from quesgen.ui.pages.report import report_page
from quesgen.ui.pages.upload import upload_page
from quesgen.ui.pages.register import register_page
from quesgen.ui.pages.admin_dashboard import admin_dashboard
from quesgen.ui.pages.configure_fine import configure_fine
from quesgen.ui.pages.quiz_fine import quiz_fine
from quesgen.ui.pages.final import final
from quesgen.ui.pages.final_quiz import final_quiz
from quesgen.ui.pages.retake_score import retake_score

st.set_page_config(
    page_title=AppSettings.app_name,
    page_icon="./static/Images/icon.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    HtmlContent.get_content("style"),
    unsafe_allow_html=True,
)

def main():
    initialize_session_state()
    if not st.session_state.authenticated:
        if st.session_state.page == Page.REGISTER:
            register_page()
        else:
            login_page()
    else:
        if st.session_state.page == Page.UPLOAD:
            upload_page()
        elif st.session_state.page == Page.MANAGE_FILES:
            manage_files_page()
        elif st.session_state.page == Page.CONFIGURE:
            configure_page()
        elif st.session_state.page == Page.QUIZ:
            quiz_page()
        elif st.session_state.page == Page.REPORT:
            report_page()
        elif st.session_state.page == Page.HISTORY:
            history_page()
        elif st.session_state.page == Page.ADMIN_DASHBOARD:
            admin_dashboard()
        elif st.session_state.page == Page.CONFIGURE_FINE:
            configure_fine()
        elif st.session_state.page == Page.QUIZ_FINE:
            quiz_fine()
        elif st.session_state.page == Page.FINAL:
            final()
        elif st.session_state.page == Page.FINAL_QUIZ:
            final_quiz()
        elif st.session_state.page == Page.RETAKE_SCORE:
            retake_score()
        else:
            login_page()


if __name__ == "__main__":
    main()

