import streamlit as st

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []  # assistant messages store evidence md too

    if "chat_history_by_scope" not in st.session_state:
        st.session_state.chat_history_by_scope = {}

    if "index_by_file" not in st.session_state:
        st.session_state.index_by_file = {}

    if "uploaded_filenames" not in st.session_state:
        st.session_state.uploaded_filenames = []

    # widget/UI keys
    if "selected_files_ui" not in st.session_state:
        st.session_state.selected_files_ui = []
    if "selected_files" not in st.session_state:
        st.session_state.selected_files = []
    if "use_all_files_ui" not in st.session_state:
        st.session_state.use_all_files_ui = False

    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None