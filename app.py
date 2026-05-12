import streamlit as st
import google.generativeai as genai
import json
import re

# ── Configure Gemini API ─────────────────────────────────────────────────────
genai.configure(api_key="AIzaSyBIwzml_icqCyFwFSaJQlJi2la9BdTm9RM")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="🧠",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 700px; }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
    }

    .correct-answer {
        background-color: #EAF3DE;
        border-left: 4px solid #3B6D11;
        padding: 10px 14px;
        border-radius: 6px;
        margin: 6px 0;
        color: #27500A;
        font-size: 15px;
    }

    .wrong-answer {
        background-color: #FCEBEB;
        border-left: 4px solid #A32D2D;
        padding: 10px 14px;
        border-radius: 6px;
        margin: 6px 0;
        color: #791F1F;
        font-size: 15px;
    }

    .neutral-answer {
        background-color: #F1EFE8;
        border-left: 4px solid #888780;
        padding: 10px 14px;
        border-radius: 6px;
        margin: 6px 0;
        color: #444441;
        font-size: 15px;
    }

    .score-box {
        background-color: #E6F1FB;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ── Generate Questions using Gemini ─────────────────────────────────────────
def generate_questions(topic: str, num: int, difficulty: str) -> list:

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
Generate exactly {num} multiple choice questions about "{topic}" at {difficulty} difficulty level.

Return ONLY a valid JSON array.

Format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0
  }}
]

Rules:
- Exactly 4 options
- Only one correct answer
- answer should be the 0-based index
- No markdown
- No explanation
"""

    response = model.generate_content(prompt)

    raw = response.text

    clean = re.sub(r"```json|```", "", raw).strip()

    return json.loads(clean)

# ── Session State ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "questions": [],
        "answers": {},
        "current": 0,
        "submitted": False,
        "quiz_started": False,
        "topic_label": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Setup Screen ─────────────────────────────────────────────────────────────
def show_setup():

    st.title("🧠 AI Quiz Generator")

    st.markdown("Generate quizzes instantly using Gemini AI.")

    st.divider()

    topic = st.text_input(
        "Topic",
        placeholder="e.g. Java, DBMS, Python, Photosynthesis..."
    )

    col1, col2 = st.columns(2)

    with col1:
        num = st.selectbox(
            "Number of Questions",
            [3, 5, 8, 10],
            index=1
        )

    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1
        )

    if st.button("Generate Quiz ✨", type="primary"):

        if not topic.strip():
            st.error("Please enter a topic.")

        else:
            with st.spinner("Generating quiz..."):

                try:
                    qs = generate_questions(
                        topic.strip(),
                        num,
                        difficulty.lower()
                    )

                    st.session_state.questions = qs
                    st.session_state.answers = {}
                    st.session_state.current = 0
                    st.session_state.submitted = False
                    st.session_state.quiz_started = True
                    st.session_state.topic_label = topic.strip()

                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

# ── Quiz Screen ──────────────────────────────────────────────────────────────
def show_quiz():

    questions = st.session_state.questions
    current = st.session_state.current
    answers = st.session_state.answers

    labels = ["A", "B", "C", "D"]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"**Topic:** {st.session_state.topic_label}")

    with col2:
        st.markdown(f"**{current + 1} / {len(questions)}**")

    st.progress((current + 1) / len(questions))

    st.divider()

    q = questions[current]

    st.markdown(f"### Q{current + 1}. {q['question']}")

    selected = answers.get(current)

    choice = st.radio(
        "Choose an answer:",
        options=list(range(4)),
        format_func=lambda i: f"{labels[i]}. {q['options'][i]}",
        index=selected if selected is not None else None,
        key=f"q_{current}"
    )

    if choice is not None:
        st.session_state.answers[current] = choice

    st.divider()

    col_prev, col_mid, col_next = st.columns([1, 2, 1])

    with col_prev:
        if current > 0:
            if st.button("← Previous"):
                st.session_state.current -= 1
                st.rerun()

    with col_next:
        if current < len(questions) - 1:
            if st.button("Next →"):
                st.session_state.current += 1
                st.rerun()

    all_answered = all(
        i in st.session_state.answers
        for i in range(len(questions))
    )

    if all_answered:
        with col_mid:
            if st.button("Submit Quiz 🎯", type="primary"):
                st.session_state.submitted = True
                st.rerun()

# ── Results Screen ───────────────────────────────────────────────────────────
def show_results():

    questions = st.session_state.questions
    answers = st.session_state.answers

    labels = ["A", "B", "C", "D"]

    score = sum(
        1
        for i, q in enumerate(questions)
        if answers.get(i) == q["answer"]
    )

    pct = round((score / len(questions)) * 100)

    emoji = "🎉" if pct >= 80 else "👍" if pct >= 50 else "📚"

    msg = (
        "Great job!"
        if pct >= 80
        else "Good effort!"
        if pct >= 50
        else "Keep practicing!"
    )

    st.markdown(f"""
    <div class="score-box">
        <h2>{emoji} {score} / {len(questions)}</h2>
        <h3>{pct}%</h3>
        <p>{msg}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Review Answers")

    for i, q in enumerate(questions):

        user_ans = answers.get(i)

        correct = user_ans == q["answer"]

        icon = "✅" if correct else "❌"

        with st.expander(f"{icon} Q{i+1}: {q['question']}"):

            for j, opt in enumerate(q["options"]):

                if j == q["answer"] and j == user_ans:

                    st.markdown(
                        f'<div class="correct-answer">✓ {labels[j]}. {opt} (Correct)</div>',
                        unsafe_allow_html=True
                    )

                elif j == q["answer"]:

                    st.markdown(
                        f'<div class="correct-answer">✓ {labels[j]}. {opt} (Correct Answer)</div>',
                        unsafe_allow_html=True
                    )

                elif j == user_ans:

                    st.markdown(
                        f'<div class="wrong-answer">✗ {labels[j]}. {opt} (Your Answer)</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f'<div class="neutral-answer">{labels[j]}. {opt}</div>',
                        unsafe_allow_html=True
                    )

    st.divider()

    if st.button("Try Another Topic 🔄", type="primary"):

        for key in [
            "questions",
            "answers",
            "current",
            "submitted",
            "quiz_started",
            "topic_label"
        ]:
            del st.session_state[key]

        st.rerun()

# ── Router ───────────────────────────────────────────────────────────────────
if not st.session_state.quiz_started:
    show_setup()

elif st.session_state.submitted:
    show_results()

else:
    show_quiz()