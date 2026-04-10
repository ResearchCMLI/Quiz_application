import streamlit as st

from quesgen.settings.app_config import Page
from quesgen.ui.sidebar import render_sidebar


def history_page():
    st.markdown('<h2 class="material-page-title">📊 Quiz History</h2>', unsafe_allow_html=True)

    render_sidebar()

    if not st.session_state.quiz_history:
        st.markdown(
            """
        <div class="material-info" style="text-align: center; padding: 48px 32px;">
            <h3 style="margin: 0 0 16px 0;">📝 No Quiz History Available</h3>
            <p style="margin: 0 0 32px 0; font-size: 1.1rem;">
                Take your first quiz to see results here!
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("🎯 START QUIZ", use_container_width=True, type="primary"):
            st.session_state.page = Page.CONFIGURE
            st.rerun()
        return

    # Statistics overview
    total_quizzes = len(st.session_state.quiz_history)
    avg_score = sum([quiz["percentage"] for quiz in st.session_state.quiz_history]) / total_quizzes
    total_questions = sum([quiz["num_questions"] for quiz in st.session_state.quiz_history])
    best_score = max([quiz["percentage"] for quiz in st.session_state.quiz_history])

    col1, col2, col3, col4 = st.columns(4)

    overview_metrics = [
        ("🎯", "Total Quizzes", total_quizzes),
        ("📊", "Avg Score", f"{avg_score:.1f}%"),
        ("❓", "Total Questions", total_questions),
        ("🏆", "Best Score", f"{best_score:.1f}%"),
    ]

    for i, (icon, label, value) in enumerate(overview_metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(
                f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Quiz history list
    st.markdown('<h3 class="material-section-title">📋 Results</h3>', unsafe_allow_html=True)

    sorted_history = sorted(st.session_state.quiz_history, key=lambda x: x["date"], reverse=True)

    for i, quiz in enumerate(sorted_history):
        # Grade calculation
        if quiz["percentage"] >= 90:
            grade, grade_color = "A+", "#4caf50"
        elif quiz["percentage"] >= 80:
            grade, grade_color = "A", "#66bb6a"
        elif quiz["percentage"] >= 70:
            grade, grade_color = "B", "#ff9800"
        elif quiz["percentage"] >= 60:
            grade, grade_color = "C", "#ff7043"
        else:
            grade, grade_color = "D", "#f44336"

        st.markdown(
            f"""
        <div class="history-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #1976d2; font-size: 1.25rem;">Quiz #{len(sorted_history) - i}</h4>
                    <p style="margin: 4px 0 0 0; color: #757575; font-size: 0.95rem;">{quiz['date']}</p>
                </div>
                <div style="text-align: right;">
                    <span class="grade-badge" style="background: {grade_color};">{grade}</span>
                    <div style="margin-top: 8px; font-size: 1.5rem; font-weight: 700; color: {grade_color};">
                        {quiz['percentage']:.1f}%
                    </div>
                </div>
            </div>
            <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; font-size: 0.95rem;">
                <div><strong>Difficulty:</strong> <span style="color: #1976d2;">{quiz['difficulty']}</span></div>
                <div><strong>Questions:</strong> <span style="color: #1976d2;">{quiz['num_questions']}</span></div>
                <div><strong>Points:</strong> <span style="color: #1976d2;">{quiz['earned_points']}/{quiz['total_points']}</span></div>
                <div><strong>Avg Score:</strong> <span style="color: #1976d2;">{quiz['avg_score']:.1f}/10</span></div>
            </div>
            <div style="margin-top: 12px; font-size: 0.9rem;">
                <strong>Files Used:</strong> <span style="color: #757575;">{', '.join(quiz['selected_files']) if quiz['selected_files'] else 'None'}</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Expandable details
        with st.expander(f"📋 View Details - Quiz #{len(sorted_history) - i}", expanded=False):
            st.markdown("### Question-wise Performance:")
            for j, answer in enumerate(quiz["answers"]):
                question = answer["question"]
                evaluation = answer["evaluation"]

                score_color = (
                    "#4caf50" if evaluation["score"] >= 7 else "#ff9800" if evaluation["score"] >= 5 else "#f44336"
                )

                col_q, col_s = st.columns([3, 1])
                with col_q:
                    st.markdown(f"**Q{j+1}:** {question['question'][:100]}...")
                    st.markdown(f"*Topic: {question['topic']}*")

                with col_s:
                    st.markdown(
                        f"""
                    <div style="text-align: center; background: {score_color}; color: white; 
                            padding: 8px; border-radius: 6px; font-weight: 600;">
                        {evaluation['score']}/10
                    </div>
                    <div style="text-align: center; font-size: 0.9rem; margin-top: 4px; color: #757575;">
                        {evaluation['points_earned']}/{question['points']} pts
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                if j < len(quiz["answers"]) - 1:
                    st.markdown("---")

    # Action buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎯 TAKE NEW QUIZ", use_container_width=True, type="primary"):
            st.session_state.page = "configure"
            st.rerun()

    with col2:
        if st.button("🗑️ CLEAR HISTORY", use_container_width=True):
            st.session_state.show_clear_confirm = True
            st.rerun()

    # Confirmation dialog
    if st.session_state.get("show_clear_confirm", False):
        st.markdown(
            """
        <div class="material-warning" style="margin-top: 32px;">
            <h4 style="margin: 0 0 12px 0;">⚠️ Confirm Action</h4>
            <p style="margin: 0;">Are you sure you want to clear all quiz history? This action cannot be undone.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✅ YES, CLEAR ALL", use_container_width=True, type="primary"):
                st.session_state.quiz_history = []
                st.session_state.show_clear_confirm = False
                st.success("✅ Quiz history cleared successfully!")
                st.rerun()
        with col_no:
            if st.button("❌ CANCEL", use_container_width=True):
                st.session_state.show_clear_confirm = False
                st.rerun()
