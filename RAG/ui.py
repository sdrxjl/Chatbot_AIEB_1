import streamlit as st
from pathlib import Path
from cache_utils import clear_cache_dir

'''def render_sidebar_settings():
    st.sidebar.header("QA Settings")
    use_history = st.sidebar.toggle("Use chat history (multi-turn)", value=True)
    history_turns = st.sidebar.slider("History turns", 0, 12, 6, disabled=not use_history)
    show_only_cited = st.sidebar.toggle("Evidence: show only cited chunks", value=True)
    st.sidebar.divider()
    st.sidebar.header("Scope")
    return use_history, history_turns, show_only_cited
'''

def render_sidebar_settings():
    st.sidebar.header("QA Settings")

    use_history = st.sidebar.toggle("Use chat history (multi-turn)", value=True)
    history_turns = st.sidebar.slider("History turns", 0, 12, 6, disabled=not use_history)

    show_only_cited_evidence = st.sidebar.toggle("Evidence: show only cited chunks", value=True)
    show_only_cited_sources = st.sidebar.toggle("Sources: show only cited", value=True)

    '''st.sidebar.divider()
    st.sidebar.header("Scope")'''

    return use_history, history_turns, show_only_cited_evidence, show_only_cited_sources

'''def render_top_controls(cache_dir: Path):
    col1, col2, col3 = st.columns(3)
    with col1:
        clear_chat = st.button("🧹 Clear Chat")
    with col2:
        rebuild_memory_only = st.button("🧠 Rebuild Index (memory only)")
    with col3:
        clear_disk = st.button("🗑️ Clear Disk Cache")
        if clear_disk:
            clear_cache_dir(cache_dir)
            st.success("Disk cache cleared.")
    return clear_chat, rebuild_memory_only
'''


def render_top_controls(cache_dir: Path):

    st.sidebar.divider()
    st.sidebar.header("Maintenance")

    clear_chat = st.sidebar.button(
        "Clear Chat",
        use_container_width=True,
        help="Remove the current conversation history."
    )

    rebuild_memory_only = st.sidebar.button(
        "Reload Index from Cache",
        use_container_width=True,
        help="Reload FAISS indexes from local cache without rebuilding embeddings."
    )

    clear_disk = st.sidebar.button(
        "Delete Local FAISS Cache",
        use_container_width=True,
        help="Delete saved FAISS indexes and metadata files. They will rebuild next time."
    )

    if clear_disk:
        clear_cache_dir(cache_dir)
        st.sidebar.success("Disk cache cleared.")

    return clear_chat, rebuild_memory_only

'''
def render_scope_controls(all_files):
    # callbacks (must run before widgets)
    def _select_all_scope():
        st.session_state.use_all_files_ui = True
        st.session_state.selected_files_ui = list(all_files)

    def _clear_scope():
        st.session_state.use_all_files_ui = False
        st.session_state.selected_files_ui = []

    c1, c2 = st.sidebar.columns(2)
    with c1:
        st.sidebar.button("All", on_click=_select_all_scope, key="scope_all_btn")
    with c2:
        st.sidebar.button("Clear", on_click=_clear_scope, key="scope_clear_btn")

    st.sidebar.checkbox("Use all documents", key="use_all_files_ui")

    if st.session_state.use_all_files_ui:
        st.session_state.selected_files_ui = list(all_files)

    st.sidebar.multiselect(
        "Documents in scope",
        options=all_files,
        key="selected_files_ui",
    )

    st.session_state.selected_files = list(st.session_state.selected_files_ui)

    if st.session_state.selected_files:
        st.sidebar.caption(f"Using {len(st.session_state.selected_files)} file(s)")
    else:
        st.sidebar.warning("No document selected")

'''

def render_scope_controls(all_files):
    # Single control: checkbox
    st.sidebar.divider()

    st.sidebar.header("Documents to Search")

    use_all = st.sidebar.checkbox("Use all documents", key="use_all_files_ui")

    if use_all:
        # lock selection to all files
        st.session_state.selected_files_ui = list(all_files)
        st.sidebar.multiselect(
            "Documents in scope",
            options=all_files,
            key="selected_files_ui",
            disabled=True,
        )
    else:
        st.sidebar.multiselect(
            "Documents in scope",
            options=all_files,
            key="selected_files_ui",
        )

    st.session_state.selected_files = list(st.session_state.selected_files_ui)

    if st.session_state.selected_files:
        st.sidebar.caption(f"Using {len(st.session_state.selected_files)} file(s)")
    else:
        st.sidebar.warning("No document selected")