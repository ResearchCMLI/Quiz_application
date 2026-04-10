from datetime import datetime

import streamlit as st

from quesgen.settings.app_config import Page, initialize_session_state


def report_page():
    if not st.session_state.quiz_completed or not st.session_state.answers:
        st.markdown(
            """
        <div class="material-error">
            <h4 style="margin: 0 0 8px 0;">❌ Quiz Not Completed</h4>
            <p style="margin: 0;">No quiz results available to display.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    st.markdown('<h2 class="material-page-title">📊 Quiz Report</h2>', unsafe_allow_html=True)

    # Calculate statistics
    total_points = sum([ans["question"]["points"] for ans in st.session_state.answers])
    earned_points = sum([ans["evaluation"]["points_earned"] for ans in st.session_state.answers])
    avg_score = sum([ans["evaluation"]["score"] for ans in st.session_state.answers]) / len(st.session_state.answers)
    percentage = (earned_points / total_points) * 100

    # Save to history only once
    if not st.session_state.current_quiz_saved:
        quiz_result = {
            "quiz_id": f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "difficulty": st.session_state.difficulty,
            "num_questions": len(st.session_state.answers),
            "selected_files": st.session_state.selected_files,
            "total_points": total_points,
            "earned_points": earned_points,
            "percentage": percentage,
            "avg_score": avg_score,
            "answers": st.session_state.answers,
        }
        st.session_state.quiz_history.append(quiz_result)
        st.session_state.current_quiz_saved = True

    # Metrics display
    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("📝", "Questions", len(st.session_state.answers), "#1976d2"),
        (
            "🎯",
            "Score",
            f"{percentage:.1f}%",
            "#4caf50" if percentage >= 70 else "#ff9800" if percentage >= 50 else "#f44336",
        ),
        ("⭐", "Avg Rating", f"{avg_score:.1f}/10", "#1976d2"),
        ("💎", "Points", f"{earned_points}/{total_points}", "#1976d2"),
    ]

    for i, (icon, label, value, color) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(
                f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">{icon}</div>
                <div class="metric-value" style="color: {color};">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Grade display
    if percentage >= 90:
        grade, comment, color = "A+", "Outstanding performance! Excellent understanding demonstrated.", "#4caf50"
    elif percentage >= 80:
        grade, comment, color = "A", "Great job! Strong grasp of the concepts.", "#66bb6a"
    elif percentage >= 70:
        grade, comment, color = "B", "Good work! Room for improvement in some areas.", "#ff9800"
    elif percentage >= 60:
        grade, comment, color = "C", "Satisfactory. Consider reviewing the material again.", "#ff7043"
    else:
        grade, comment, color = "D", "Needs improvement. Additional study recommended.", "#f44336"

    st.markdown(
        f"""
    <div style="background: {color}; color: white; padding: 48px 32px; border-radius: 16px; 
                text-align: center; margin: 48px 0; box-shadow: var(--md-shadow-3);">
        <div style="font-size: 4rem; font-weight: 300; margin-bottom: 16px;">{grade}</div>
        <div style="font-size: 1.25rem; font-weight: 400; opacity: 0.95;">{comment}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Detailed breakdown
    st.markdown('<h3 class="material-section-title">📋 Detailed Breakdown</h3>', unsafe_allow_html=True)

    for i, answer_data in enumerate(st.session_state.answers):
        question = answer_data["question"]
        evaluation = answer_data["evaluation"]

        score_color = "#4caf50" if evaluation["score"] >= 7 else "#ff9800" if evaluation["score"] >= 5 else "#f44336"

        with st.expander(f"Question {i+1}: {question['topic']} (Score: {evaluation['score']}/10)", expanded=False):
            st.markdown(f"**Question:** {question['question']}")
            st.markdown(f"**Your Answer:** {answer_data['answer']}")

            col_feedback, col_points = st.columns([3, 1])
            with col_feedback:
                st.markdown(f"**Feedback:** {evaluation['feedback']}")
            with col_points:
                st.markdown(
                    f"""
                <div style="text-align: center; background: {score_color}; color: white; 
                        padding: 12px; border-radius: 8px; font-weight: 600;">
                    {evaluation['points_earned']}/{question['points']} Points
                </div>
                """,
                    unsafe_allow_html=True,
                )

    # Action buttons
    col1, col2, col3 = st.columns(3)

    actions = [
        ("🔄", "TAKE ANOTHER QUIZ", Page.CONFIGURE),
        ("📊", "VIEW HISTORY", Page.HISTORY),
        ("🚪", "LOGOUT", Page.LOGOUT),
    ]

    for i, (icon, label, action) in enumerate(actions):
        with [col1, col2, col3][i]:
            if st.button(f"{icon} {label}", use_container_width=True, key=f"action_{action}"):
                if action == Page.LOGOUT:
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    initialize_session_state()
                elif action == Page.CONFIGURE:
                    # Reset quiz state
                    st.session_state.quiz_started = False
                    st.session_state.quiz_completed = False
                    st.session_state.current_question = 0
                    st.session_state.questions = []
                    st.session_state.answers = []
                    st.session_state.current_quiz_saved = False
                    st.session_state.page = Page.CONFIGURE
                else:
                    st.session_state.page = action
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
