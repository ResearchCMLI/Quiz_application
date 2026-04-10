import streamlit as st

from quesgen.settings.app_config import Page
from quesgen.ui.sidebar import render_sidebar


def upload_page():
    
    st.markdown(
    """
    <h1 style='text-align: center; color: black;'>
        AI based Quiz Generation Platform
    </h1>
    """,
    unsafe_allow_html=True
   )

    if st.session_state.get("show_login_sucess"):
        st.success("Sucessfully logged in")
        st.session_state.pop("show_login_sucess")
   
    render_sidebar()

    #col1, col2 = st.columns([2, 1])

    #with col1:
        

       
            

   

    st.markdown("</div>", unsafe_allow_html=True)
