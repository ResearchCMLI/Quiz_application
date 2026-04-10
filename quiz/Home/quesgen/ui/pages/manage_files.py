from datetime import datetime

import streamlit as st

from quesgen.settings.app_config import Page
from quesgen.ui.sidebar import render_sidebar


def manage_files_page():
    st.markdown('<h2 class="material-page-title">📂 File Management</h2>', unsafe_allow_html=True)

    render_sidebar()
    if not st.session_state.uploaded_files:
        st.markdown(
            """
        <div class="material-info" style="text-align: center; padding: 48px 32px;">
            <h3 style="margin: 0 0 16px 0;">📁 No Files Uploaded Yet</h3>
            <p style="margin: 0 0 32px 0; font-size: 1.1rem;">
                Upload some PDF files first to manage them here.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("📁 GO TO UPLOAD", use_container_width=True, type="primary"):
            st.session_state.page = Page.UPLOAD
            st.rerun()
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<h3 class="material-section-title">📋 Uploaded Files</h3>', unsafe_allow_html=True)

        for i, file in enumerate(st.session_state.uploaded_files):
            size_mb = file.size / (1024 * 1024)
            size_display = f"{size_mb:.1f} MB" if size_mb >= 1 else f"{file.size/1024:.1f} KB"

            st.markdown(
                f"""
            <div class="file-item">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.5rem;">📄</span>
                    <div>
                        <div style="font-weight: 500; color: #1976d2; font-size: 1rem;">{file.name}</div>
                        <div style="font-size: 0.875rem; color: #757575;">
                            {size_display} • Added {datetime.now().strftime("%Y-%m-%d")}
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span style="font-size: 0.875rem; color: #4caf50;">✓ Ready</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            col_delete, _ = st.columns([1, 3])
            with col_delete:
                if st.button("🗑️ Remove", key=f"delete_{i}_{file.name}", help=f"Delete {file.name}"):
                    st.session_state.uploaded_files.pop(i)
                    st.session_state.uploader_key += 1
                    st.success(f"✅ {file.name} removed successfully!")
                    st.rerun()

        # Bulk actions
        if len(st.session_state.uploaded_files) > 1:
            st.markdown('<h3 class="material-section-title">⚡ Bulk Actions</h3>', unsafe_allow_html=True)

            if st.button("🗑️ CLEAR ALL FILES", use_container_width=True):
                st.session_state.show_clear_files_confirm = True
                st.rerun()

            # Confirmation dialog
            if st.session_state.get("show_clear_files_confirm", False):
                st.markdown(
                    """
                <div class="material-warning">
                    <h4 style="margin: 0 0 8px 0;">⚠️ Confirm Action</h4>
                    <p style="margin: 0;">Are you sure you want to remove all uploaded files?</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ YES, CLEAR ALL", use_container_width=True):
                        st.session_state.uploaded_files = []
                        st.session_state.show_clear_files_confirm = False
                        st.session_state.uploader_key += 1
                        st.success("✅ All files removed successfully!")
                        st.rerun()
                with col_no:
                    if st.button("❌ CANCEL", use_container_width=True):
                        st.session_state.show_clear_files_confirm = False
                        st.rerun()

    with col2:
        # File statistics
        total_size = sum([file.size for file in st.session_state.uploaded_files])
        total_size_mb = total_size / (1024 * 1024)

        st.markdown(
            f"""
        <div class="metric-card">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📊</div>
            <div class="metric-value">{len(st.session_state.uploaded_files)}</div>
            <div class="metric-label">Total Files</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div class="metric-card">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">💾</div>
            <div class="metric-value">{total_size_mb:.1f}</div>
            <div class="metric-label">Total Size (MB)</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # File types breakdown
        file_types = {}
        for file in st.session_state.uploaded_files:
            ext = file.name.split(".")[-1].upper()
            file_types[ext] = file_types.get(ext, 0) + 1

        list_items = ""
        for file_type, count in file_types.items():
            list_items += f"<li><strong>{file_type}:</strong> {count} file{'s' if count > 1 else ''}</li>"

        st.markdown(
            """
        <div class="tips-card">
            <h4>📋 File Types</h4>
            <ul style="line-height: 1.6;">
            {}
            </ul>
        </div>
        """.format(
                list_items
            ),
            unsafe_allow_html=True,
        )

        # Quick actions
        st.markdown('<div style="margin-top: 24px;">', unsafe_allow_html=True)
        if st.button("📁 UPLOAD MORE", use_container_width=True):
            st.session_state.page = Page.UPLOAD
            st.rerun()

        if st.button("🎯 CONFIGURE QUIZ", use_container_width=True, type="primary"):
            st.session_state.page = Page.CONFIGURE
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
