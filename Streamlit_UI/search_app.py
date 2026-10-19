"""API-backed search demo. Run: streamlit run Streamlit_UI/search_app.py."""

import os
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

st.set_page_config(page_title="Find a topic", page_icon="🔎", layout="wide")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from Streamlit_UI.search_client import ApiError, EducationApi

load_dotenv(PROJECT_ROOT / ".env")


def setting(name, default=""):
    try:
        return str(st.secrets.get(name, os.getenv(name, default)))
    except (FileNotFoundError, KeyError):
        return os.getenv(name, default)


try:
    api = EducationApi(setting("EDUCATION_API_BASE_URL", "http://127.0.0.1:8000"), setting("EDUCATION_API_KEY"))
except ApiError as error:
    st.error(str(error))
    st.info("Configure EDUCATION_API_BASE_URL and EDUCATION_API_KEY for the main education API.")
    st.stop()

st.title("Find something to learn")
st.caption("Search existing topics and questions. Search is free of LLM calls; teaching starts only when you choose an action.")
st.caption("Connected to the education API. Tutors and model calls run on the backend.")
with st.form("search"):
    query = st.text_input("Topic, subject or request", max_chars=300,
                          placeholder="photosynthesis · maths · give five random topics")
    first, second = st.columns(2)
    subject = first.selectbox("Subject", ["auto", "science", "math"],
                              format_func=lambda x: {"auto": "All / infer from search", "science": "Science", "math": "Maths"}[x])
    mode = second.selectbox("Learning option", ["auto", "tutor", "whiteboard", "doubt"],
                             format_func=lambda x: {"auto": "All / infer from search", "tutor": "Tutor", "whiteboard": "Whiteboard", "doubt": "Ask a doubt"}[x])
    submitted = st.form_submit_button("Search", type="primary")
surprise = st.button("Surprise me — 5 topics")
if submitted or surprise:
    try:
        with st.spinner("Finding content..."):
            response = api.search("" if surprise else query, subject, mode, surprise)
        st.session_state.search_response = response
        st.session_state.search_query = "" if surprise else query
    except ApiError as error:
        st.error(str(error))  # Retain previous results and lesson on errors.

response = st.session_state.get("search_response")
if response is not None:
    st.caption(f"{response['total_matches']} matches · {response['subject']} · {response['mode']} · {response['selection']}")
    if not response["results"]:
        st.info("No matching content. Try another topic, or ask a general doubt below.")
    for result in response["results"]:
        with st.container(border=True):
            st.subheader(result["title"])
            info = [result["subject"].title(), result["content_type"].replace("_", " ")]
            if result.get("book_part"):
                info.append(f"Part {result['book_part']}")
            if result.get("chapter"):
                info.append(f"Chapter {result['chapter']}")
            st.caption(" · ".join(info))
            st.write(result["description"])
            actions = sorted(result["actions"], key=lambda a: a["type"] != response["mode"])
            for column, action in zip(st.columns(len(actions)), actions):
                label = ("Whiteboard" if action["type"] == "whiteboard" else
                         "Ask a doubt" if action["type"] == "doubt" else
                         "Solve with tutor" if action.get("problem_id") else "Learn with tutor")
                if column.button(label, key=result["id"] + ":" + action["type"]):
                    if action["type"] == "doubt":
                        st.session_state.doubt_target = result
                        st.session_state.doubt_answer = None
                    else:
                        try:
                            with st.spinner("Starting lesson..."):
                                lesson = api.start(action, result["title"])
                            st.session_state.search_lesson = lesson
                            st.session_state.lesson_messages = [("assistant", lesson["turn"]["message"])]
                            st.session_state.last_search_autoplay = None
                            st.session_state.doubt_target = None
                        except ApiError as error:
                            st.error(str(error))
    if st.button("Ask a general doubt"):
        st.session_state.doubt_target = {"id": "general", "title": "General doubt", "description": ""}
        st.session_state.doubt_answer = None

target = st.session_state.get("doubt_target")
if target:
    st.divider()
    st.subheader("Ask a doubt — " + target["title"])
    with st.form("doubt_form"):
        question = st.text_area("What would you like to understand?", max_chars=4000,
                                key="question:" + target["id"])
        ask = st.form_submit_button("Explain my doubt")
    if ask:
        if not question.strip():
            st.warning("Enter your question first.")
        else:
            try:
                context = "" if target["id"] == "general" else target["title"] + "\n" + target["description"]
                with st.spinner("Explaining..."):
                    st.session_state.doubt_answer = api.doubt(question.strip(), context)
            except ApiError as error:
                st.error(str(error))
    if st.session_state.get("doubt_answer"):
        st.write(st.session_state.doubt_answer)

lesson = st.session_state.get("search_lesson")
if lesson and not target:
    st.divider()
    st.subheader(lesson["title"])
    turn = lesson["turn"]
    st.caption(f"{lesson['kind'].title()} · {turn['current_state']}")
    chat, board = st.columns(2) if lesson["kind"] == "whiteboard" else (st.container(), None)
    with chat:
        for role, message in st.session_state.lesson_messages:
            with st.chat_message(role):
                st.write(message)
        if turn["metadata"].get("show_simulation"):
            st.info("This search demo supports text chat only. Use the main tutor UI for interactive simulations.")
        message = st.chat_input("Reply to the tutor...", disabled=turn["current_state"].upper() in {"DONE", "END"}, max_chars=4000)
        if message:
            try:
                with st.spinner("Tutor is responding..."):
                    next_turn = api.continue_lesson(lesson, message)
                st.session_state.lesson_messages.extend([("user", message), ("assistant", next_turn["message"])])
                lesson["turn"] = next_turn
                st.session_state.search_lesson = lesson
                st.rerun()
            except ApiError as error:
                st.error(str(error))
    if board is not None:
        with board:
            # Reuse the existing safe renderer, cumulative board and browser TTS.
            try:
                # Only visual rendering is local; no agent is invoked here.
                poc_root = PROJECT_ROOT.parent / "Whiteboard_Tutor_Education_POC"
                if (poc_root / "whiteboard_tutor").is_dir() and str(poc_root) not in sys.path:
                    sys.path.append(str(poc_root))
                from whiteboard_tutor.board.models import WhiteboardPatch, WhiteboardState
                from whiteboard_tutor.board.renderer import render_whiteboard_html

                state = WhiteboardState.model_validate(turn["whiteboard_state"])
                patch = WhiteboardPatch.model_validate(turn["whiteboard_patch"])
                revision_key = (lesson["thread_id"], state.revision)
                autoplay = st.session_state.get("last_search_autoplay") != revision_key
                components.html(render_whiteboard_html(state, patch, turn["message"], autoplay), height=720, scrolling=True)
                st.session_state.last_search_autoplay = revision_key
            except (ImportError, ValueError, KeyError, OSError):
                st.warning("Whiteboard visuals require the matching whiteboard_tutor package and SVG assets on this host. Tutor chat remains available.")
