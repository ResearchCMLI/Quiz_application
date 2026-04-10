import streamlit as st

#from quesgen.settings.app_config import Page
#from quesgen.ui.sidebar import render_sidebar
class AppSettings:
    app_name = "Quiz Platform"
    description = "Please login to continue."

class Page:
    UPLOAD = "UPLOAD"



def upload_page():
    st.markdown('<h2 class="material-page-title">📁 Document Upload</h2>', unsafe_allow_html=True)

    #render_sidebar()

    col1, col2 = st.columns([2, 1])

    with col1:
        # Upload section only
        st.markdown('<h3 class="material-section-title">📤 Upload PDF Documents</h3>', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload PDF documents from which questions will be generated",
            key=f"file_uploader_{st.session_state.uploader_key}",
        )

        # File processing logic
        if uploaded_files:
            current_files = list(st.session_state.uploaded_files)
            current_file_names = [f.name for f in current_files]

            new_files_added = False
            for file in uploaded_files:
                if file.name not in current_file_names:
                    current_files.append(file)
                    new_files_added = True

            if new_files_added:
                st.session_state.uploaded_files = current_files
                st.success(
                    f"✅ {len([f for f in uploaded_files if f.name not in current_file_names])} new file(s) added!"
                )

        # Quick summary
        if st.session_state.uploaded_files:
            total_size = sum([file.size for file in st.session_state.uploaded_files])
            total_size_mb = total_size / (1024 * 1024)

            st.markdown(
                f"""
            <div class="material-success" style="margin: 24px 0;">
                <h4 style="margin: 0 0 8px 0;">✅ Files Ready</h4>
                <p style="margin: 0; font-size: 1.1rem;">
                    <strong>{len(st.session_state.uploaded_files)} files</strong> • 
                    <strong>{total_size_mb:.1f} MB total</strong>
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Action buttons
            col_manage, col_configure = st.columns(2)
            with col_manage:
                if st.button("📂 MANAGE FILES", use_container_width=True):
                    st.session_state.page = Page.MANAGE_FILES
                    st.rerun()

            with col_configure:
                if st.button("🎯 CONFIGURE QUIZ", use_container_width=True, type="primary"):
                    st.session_state.page = Page.CONFIGURE
                    st.rerun()

    with col2:
        # Instructions
        st.markdown(
            """
        <div class="instructions-card">
            <h4>📋 Instructions</h4>
            <ol style="line-height: 1.8;">
                <li><strong>Upload PDFs:</strong> Select one or more PDF files</li>
                <li><strong>Manage Files:</strong> Review and delete files if needed</li>
                <li><strong>Configure:</strong> Choose files and settings</li>
                <li><strong>Take Quiz:</strong> Answer generated questions</li>
                <li><strong>Review:</strong> Get detailed feedback</li>
            </ol>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Statistics
        if st.session_state.uploaded_files:
            st.markdown(
                f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">📊</div>
                <div class="metric-value">{len(st.session_state.uploaded_files)}</div>
                <div class="metric-label">Files Uploaded</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Tips
        st.markdown(
            """
        <div class="tips-card">
            <h4>💡 Tips</h4>
            <ul style="line-height: 1.6;">
                <li><strong>Max file size:</strong> 200MB per file</li>
                <li><strong>Supported format:</strong> PDF only</li>
                <li><strong>Multiple files:</strong> Upload several PDFs at once</li>
                <li><strong>File management:</strong> Use the manage files page</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
if __name__ == "__main__":
    upload_page()
