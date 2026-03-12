import os
#import re
import streamlit as st

from app_config import CACHE_DIR, STREAM_DELAY, EVIDENCE_EXCERPT_CHARS, TOP_K_PER_FILE, MAX_CONTEXT_CHUNKS
from state import init_session_state
from ui import render_sidebar_settings, render_top_controls, render_scope_controls
from embeddings_utils import build_embeddings, build_llm
from indexing import build_or_load_indexes
from retrieval_0 import scope_key, retrieve_docs_for_files, build_context_text
from prompting import history_pairs_to_text, build_prompt, extract_citation_indices
from render import stream_markdown_preserve_whitespace, build_evidence_md,md_formatting #, build_sources_md


def main():

    #original: load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
    # ENV / KEYS
    GOOGLE_API_KEY = 'AIzaSyDCdV-XI5PsWhu-cOnN3BUIGsCh2ogbfL0' # "YOUR_GOOGLE_API_KEY"  # Replace with your actual Gemini API key
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    # 


    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    st.set_page_config(page_title="Chat with Your PDFs (Gemini)")
    st.title("Chat with Your PDFs (Gemini)")

    init_session_state()

    # Models
    embeddings = build_embeddings()
    llm = build_llm()

    # Sidebar settings

    use_history, history_turns, show_only_cited_evidence, show_only_cited_sources = render_sidebar_settings()

    # Top controls
    clear_chat, rebuild_memory_only = render_top_controls(CACHE_DIR)
    if clear_chat:
        st.session_state.messages = []
        st.session_state.chat_history_by_scope = {}
    if rebuild_memory_only:
        st.session_state.index_by_file = {}

    # Upload
    uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=["pdf"])
    if not uploaded_files:
        st.info("Please upload PDF files to begin.")
        st.stop()

    st.session_state.uploaded_filenames = [f.name for f in uploaded_files]
    all_files = st.session_state.uploaded_filenames

    # Scope UI
    render_scope_controls(all_files)

    # Build / load indexes
    build_or_load_indexes(
        uploaded_files=uploaded_files,
        embeddings=embeddings,
        cache_root=CACHE_DIR,
        index_by_file=st.session_state.index_by_file,
    )

    # Render prior chat
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(md_formatting(msg["content"]))
            
            
            if msg["role"] == "assistant":
                ev_all = msg.get("evidence_all_md")
                ev_cited = msg.get("evidence_cited_md")
                if ev_all or ev_cited:
                    with st.expander("Evidence (show your work)", expanded=False):
                        ev = ev_cited if show_only_cited_evidence else (ev_all or ev_cited)
                        st.markdown(md_formatting(ev), unsafe_allow_html=True)

    # Ask
    user_input = st.chat_input("Ask a question about your PDFs...")
    if user_input:
        st.session_state.pending_question = user_input

    if not st.session_state.pending_question:
        st.stop()

    if not st.session_state.selected_files:
        st.warning("Which document(s) should I use?")
        st.info("Please choose PDFs in the left sidebar under **Documents to Search**.")
        st.stop()

    question = st.session_state.pending_question
    st.session_state.pending_question = None
    effective_files = st.session_state.selected_files

    st.caption(f"Search scope: {', '.join(effective_files)}")

    # store/display user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        #st.markdown(question)
        #st.markdown(re.sub(r"`([^`]+)`", r"\1",question))

        st.text(question)
        

    # history per scope
    sk = scope_key(effective_files)
    st.session_state.chat_history_by_scope.setdefault(sk, [])
    history_pairs = st.session_state.chat_history_by_scope[sk]
    history_text = history_pairs_to_text(history_pairs, history_turns)

    # retrieve
    retrieved_docs = retrieve_docs_for_files(
        index_by_file=st.session_state.index_by_file,
        files=effective_files,
        question=question,
        top_k_per_file=TOP_K_PER_FILE,
        max_context_chunks=MAX_CONTEXT_CHUNKS,
    )
    context_text = build_context_text(retrieved_docs)
    prompt = build_prompt(question, context_text, history_text, use_history)

    # LLM
    with st.spinner("Thinking..."):
        resp = llm.invoke(prompt)
        answer_text = getattr(resp, "content", str(resp))


    cited_set = set(extract_citation_indices(answer_text))
    #st.write("cited_set:", sorted(cited_set)) #debug

    #show_only_cited = st.sidebar.toggle("Evidence: show only cited chunks", value=True)
    # render sources/evidence
    #sources_md = build_sources_md(retrieved_docs)
    #---


    sources_md = ""
    if retrieved_docs:
        sources_md += "\n\n---\n### Sources\n\n"
        for i, d in enumerate(retrieved_docs, 1):
            if show_only_cited_sources and cited_set and i not in cited_set:
                continue
            src = d.metadata.get("source", "Unknown File")
            page0 = d.metadata.get("page", 0)
            section = d.metadata.get("section", "Unknown Section")
            sources_md += (
                f"[{i}] **{src}**  \n"
                f"Page: {page0 + 1}  \n"
                f"Section: {section}\n\n"
            )

    #----

    
    evidence_all_md, evidence_cited_md = build_evidence_md(retrieved_docs, cited_set, EVIDENCE_EXCERPT_CHARS)

    # display + save
    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed = stream_markdown_preserve_whitespace(placeholder, answer_text, delay=STREAM_DELAY)
        final_output = streamed + sources_md
        placeholder.markdown(md_formatting(final_output))

        with st.expander("Evidence (show your work)", expanded=False):
            st.markdown(md_formatting(evidence_cited_md if show_only_cited_evidence else evidence_all_md), unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": final_output,
        "evidence_all_md": evidence_all_md,
        "evidence_cited_md": evidence_cited_md,
    })
    st.session_state.chat_history_by_scope[sk].append((question, answer_text))

if __name__ == "__main__":
    main()