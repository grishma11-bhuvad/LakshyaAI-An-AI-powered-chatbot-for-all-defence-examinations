import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import uuid
from datetime import datetime

# =========================================================
# 1. CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()

st.set_page_config(
    page_title="CDS COMMAND | AI Study Assistant",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. PROFESSIONAL UI
# =========================================================

st.markdown("""
<style>
/* App background and layout */
.stApp {
    background: #F5F7FA;
    color: #26374A;
}

.block-container {
    max-width: 1180px;
    padding: 1.8rem 2.2rem 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #10243A;
    border-right: 1px solid #263A50;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCaption {
    color: #C2CEDB;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    background: transparent;
    color: #EAF0F6;
    border: 1px solid #34485D;
    border-radius: 8px;
    min-height: 42px;
    transition: background 0.15s ease;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #213A53;
    border-color: #D9A15D;
    color: #FFFFFF;
}

/* Main typography */
h1, h2, h3 {
    color: #10243A !important;
    letter-spacing: -0.35px;
}

p, li {
    line-height: 1.7;
}

/* Header */
.cds-header {
    background: #10243A;
    color: #FFFFFF;
    padding: 26px 30px;
    border-radius: 12px;
    border-bottom: 4px solid #D99A4E;
    margin-bottom: 30px;
}

.cds-eyebrow {
    color: #E8B36F;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.cds-title {
    color: #FFFFFF;
    font-size: clamp(28px, 3.5vw, 38px);
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 10px;
}

.cds-description {
    color: #D5DFE9;
    font-size: 14px;
    line-height: 1.8;
    max-width: 720px;
}

/* Topic buttons */
.stButton > button {
    background: #FFFFFF;
    color: #17324D;
    border: 1px solid #D9E1E9;
    border-radius: 9px;
    min-height: 46px;
    font-weight: 500;
    transition: background 0.15s ease, border-color 0.15s ease;
}

.stButton > button:hover {
    background: #EEF3F8;
    border-color: #59738F;
    color: #10243A;
}

/* Chat messages */

/* ChatGPT-style conversation layout */

/* Common message layout */
[data-testid="stChatMessage"] {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    max-width: 85%;
    padding: 15px 18px;
    border-radius: 16px;
    margin-bottom: 18px;
}

/* User message - right side */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse;
    margin-left: auto;
    margin-right: 0;
    background: #173A5E;
    border: 1px solid #244D73;
    color: #FFFFFF;
}

/* User message */
[class*="st-key-user_bubble"] {
    background-color: #173A5E;
    color: white;
    padding: 12px 18px;
    border-radius: 16px;
    margin-bottom: 15px;
}

[class*="st-key-user_bubble"] p,
[class*="st-key-user_bubble"] li {
    color: white !important;
}

/* AI message */
[class*="st-key-ai_bubble"] {
    background-color: #FFFFFF;
    color: #26374A;
    padding: 12px 18px;
    border: 1px solid #DCE3EA;
    border-radius: 16px;
    margin-bottom: 15px;
}

[class*="st-key-ai_bubble"] p,
[class*="st-key-ai_bubble"] li {
    color: #26374A !important;
}

/* Message content */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    line-height: 1.7;
    overflow-wrap: anywhere;
}

/* Mobile layout */
@media (max-width: 700px) {
    [data-testid="stChatMessage"] {
        max-width: 95%;
        padding: 12px;
    }
}

}

/* Chat input */
[data-testid="stChatInput"] {
    background: #FFFFFF;
}

/* Make welcome actions feel like study cards */
div.stButton > button {
    white-space: normal;
    line-height: 1.35;
}

/* Chat conversation heading */
.cds-chat-label {
    color: #52657A;
    font-size: 13px;
    margin-bottom: 8px;
}

/* Divider */
hr {
    border-color: #DCE3EA;
}

/* Small status label */
.cds-status {
    display: inline-block;
    color: #276749;
    background: #E8F5EC;
    border: 1px solid #C8E6D0;
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 12px;
}

/* Footer */
.cds-footer {
    border-top: 1px solid #DCE3EA;
    margin-top: 38px;
    padding-top: 18px;
    color: #748194;
    font-size: 12px;
    line-height: 1.8;
    text-align: center;
}

/* Mobile and small screens */
@media (max-width: 700px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    .cds-header {
        padding: 21px 19px;
    }

    .cds-title {
        font-size: 27px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. SYSTEM PROMPT
# =========================================================


# =========================================================
# 3. SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
IDENTITY AND ROLE
You are CDS COMMAND AI, an intelligent and supportive mentor
for students preparing for the Combined Defence Services (CDS)
examination in India.

Your purpose is to guide aspirants through learning, practice,
revision and improvement using generative AI and prompt engineering.

PRIMARY GOAL
Help students understand concepts, practise questions, improve
English, revise General Knowledge and prepare effectively for CDS.

SUBJECTS
- English grammar, vocabulary, idioms and comprehension
- Indian Polity and Constitution
- Indian and World History
- Geography
- General Science
- Economy and basic current affairs
- Defence awareness and CDS preparation strategy
- Mathematics when requested

TECHNIQUE 1: ROLE PROMPTING
Act as a knowledgeable, patient and encouraging CDS mentor.
Explain concepts accurately and guide students towards independent
understanding.
Never claim to be an official UPSC representative.

TECHNIQUE 2: CLEAR INSTRUCTION PROMPTING
1. Answer the user's actual question first.
2. Follow the requested topic, format and level of detail.
3. Use simple, clear English by default.
4. Explain unfamiliar terms before using them.
5. Use examples, headings, tables and bullet points when helpful.
6. Respond in Marathi when the user requests it.
7. Do not add unnecessary information to simple answers.

TECHNIQUE 3: CONTEXTUAL AND ADAPTIVE PROMPTING
1. Keep the CDS examination context in mind when relevant.
2. Use the subject, difficulty and learning goal provided by the user.
3. Adapt explanations to the user's requested knowledge level.
4. Start with basic concepts when the user says they are a beginner.
5. Provide more depth when the user asks for a detailed explanation.
6. Use conversation history to understand follow-up questions.
7. Never assume personal details or abilities without evidence.

TECHNIQUE 4: FEW-SHOT PROMPTING
Use the following examples as patterns for suitable responses.
Adapt them to the user's actual question rather than copying them
when they are not relevant.

Example A: Concept explanation

Input:
"Explain an idiom in simple English."

Expected output:
Idiom: Once in a blue moon
Meaning: Something that happens very rarely.
Example: I visit that place once in a blue moon.

Example B: Interactive MCQ

Input:
"Give me one CDS Polity MCQ and wait for my answer."

Expected output:
Question: Which body conducts the CDS examination in India?

A. Staff Selection Commission
B. Union Public Service Commission
C. National Testing Agency
D. University Grants Commission

Choose A, B, C or D.

Do not reveal the answer until the student attempts the question.

These examples demonstrate response patterns. Always check the
accuracy of generated facts and questions.

TECHNIQUE 5: STRUCTURED OUTPUT FORMATTING
Choose an appropriate format for each task.

For concept explanations:
- Definition
- Simple explanation
- Example
- CDS relevance, when useful

For comparison questions:
- Explain the main difference.
- Use a comparison table when appropriate.

For MCQs:
- State the question and four options labelled A, B, C and D.
- In interactive mode, wait for the student's answer.
- After the attempt, identify the correct answer and explain why.
- Explain relevant concepts or rules where useful.

For study plans:
- Organise tasks into clear, achievable steps.
- Follow the time and constraints specified by the user.

For English practice:
- Present the question first.
- Wait for the user's attempt in interactive mode.
- Explain the correction and relevant grammar rule afterward.

Do not force every answer into the same format.

TECHNIQUE 6: STEP-BY-STEP TEACHING
For calculations and difficult concepts:
1. Identify what the question asks.
2. Explain the relevant concept or formula.
3. Show the essential calculation or solution steps.
4. Present the final answer clearly.
5. Explain common mistakes when useful.

Keep explanations logical and understandable. Do not present
unsupported claims as verified facts.

TECHNIQUE 7: PROMPT CHAINING FOR LEARNING
When the user requests a complete learning session, organise it
into the following sequence:

Stage 1: Explain the selected topic.
Stage 2: Provide an example or application.
Stage 3: Generate relevant practice questions.
Stage 4: Evaluate the student's submitted answers.
Stage 5: Explain mistakes and recommend revision.

Use the result of each stage to guide the next stage.
Do not automatically begin a quiz when the user only requests
an explanation. Follow the user's instructions and proceed
through the sequence when requested.

MCQ AND PRACTICE RULES
1. Follow the requested subject, difficulty and question count.
2. Create original CDS-style questions.
3. Ensure each question has one defensible correct answer.
4. In interactive mode, ask one question at a time and wait.
5. For complete practice sets, provide the answer key afterward,
   unless the user requests another arrangement.
6. Never reveal an interactive answer before an attempt unless asked.
7. Never describe generated questions as official UPSC questions.
8. Never invent official marking rules.
9. Explain why an answer is correct or incorrect.

ACCURACY AND RELIABILITY
1. Never invent official exam dates, eligibility rules or cut-offs.
2. Clearly acknowledge uncertainty when necessary.
3. Do not claim to have checked live sources unless you have.
4. Recommend checking the latest official UPSC notification for
   examination dates, eligibility and official requirements.
5. Never guarantee selection or examination success.

FOLLOW-UP QUESTIONS
Use relevant conversation history to understand the user's intent.
Ask one brief clarifying question when essential information is
missing. Otherwise, answer directly.

COMMUNICATION STYLE
Be patient, respectful, supportive and motivating.
Prioritise understanding over memorisation.
Keep answers concise or detailed according to the user's request.
Use Marathi when requested and simple English by default.

LIMITATIONS
You are an AI study assistant, not an official UPSC representative.
Your responses may contain errors. Encourage verification of
important examination information using official sources.
"""


# =========================================================
# 4. GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=API_KEY) if API_KEY else None

# =========================================================
# 5. AI RESPONSE FUNCTION
# =========================================================

def get_ai_response(chat_history):

    if client is None:
        return (
            "Gemini API key not found. Please check GEMINI_API_KEY "
            "in your .env file and restart the application."
        )

    contents = []

    # Send recent conversation history.
    for message in chat_history[-20:]:
        role = message.get("role", "")
        content = message.get("content", "").strip()

        if not content:
            continue

        gemini_role = "model" if role == "assistant" else "user"

        # The first Gemini message must be from the user.
        if not contents and gemini_role != "user":
            continue

        contents.append(
            types.Content(
                role=gemini_role,
                parts=[types.Part.from_text(text=content)]
            )
        )

    if not contents:
        return "Please enter a question to begin."

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.4,
                    max_output_tokens=2048,
                ),
            )

            answer = response.text

            if answer:
                return answer

            return "I couldn't generate a response. Please try again."

        except Exception as error:
            error_message = str(error).lower()

            temporary_error = any(
                term in error_message
                for term in [
                    "503",
                    "unavailable",
                    "high demand",
                    "500",
                    "internal server error",
                    "504",
                ]
            )

            if temporary_error and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            if any(
                term in error_message
                for term in ["429", "resource_exhausted", "quota"]
            ):
                return (
                    "The Gemini usage limit may have been reached. "
                    "Please check your API quota and try again later."
                )

            if any(
                term in error_message
                for term in [
                    "api_key_invalid",
                    "invalid api key",
                    "permission_denied",
                    "401",
                    "403",
                ]
            ):
                return (
                    "There is an API key or access problem. Check your "
                    ".env file and confirm that your selected model "
                    "is available to your account."
                )

            if temporary_error:
                return (
                    "Gemini is temporarily unavailable after retries. "
                    "Please wait a little and try again."
                )

            print(f"Gemini API error: {error}")

            return (
                "The request failed. Please check the terminal for "
                "details and verify your API configuration."
            )

    return "Please try again in a little while."


# =========================================================
# 6. SESSION STATE AND CHAT HISTORY
# =========================================================

HISTORY_FILE = "chat_history.json"

def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_chat_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                st.session_state.chat_sessions,
                file,
                ensure_ascii=False,
                indent=2
            )
    except OSError:
        st.warning("Chat history could not be saved.")

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = load_chat_history()

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "profile_name" not in st.session_state:
    st.session_state.profile_name = "Aspirant"


def create_new_chat():
    st.session_state.messages = []
    st.session_state.active_chat_id = None
    st.session_state.pending_prompt = None


def select_prompt(prompt):
    st.session_state.pending_prompt = prompt


def open_chat(chat_id):
    st.session_state.active_chat_id = chat_id
    st.session_state.messages = (
        st.session_state.chat_sessions[chat_id]["messages"].copy()
    )
    st.session_state.pending_prompt = None


def save_current_chat():
    if not st.session_state.messages:
        return

    chat_id = st.session_state.active_chat_id

    if not chat_id:
        chat_id = str(uuid.uuid4())
        st.session_state.active_chat_id = chat_id

    first_user_message = next(
        (
            message["content"]
            for message in st.session_state.messages
            if message["role"] == "user"
        ),
        "New Conversation"
    )

    title = first_user_message[:35]
    if len(first_user_message) > 35:
        title += "..."

    st.session_state.chat_sessions[chat_id] = {
        "title": title,
        "messages": st.session_state.messages.copy(),
        "updated_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
    }

    save_chat_history()

# =========================================================
# 7. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="padding: 5px 0 18px;">
        <div style="
            font-size: 22px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: 0.4px;">
            CDS COMMAND
        </div>
        <div style="
            font-size: 10px;
            letter-spacing: 1.5px;
            color: #BAC8D7;
            margin-top: 5px;">
            YOUR PREPARATION SPACE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.button(
        "＋ New Chat",
        key="new_chat_top",
        use_container_width=True,
        on_click=create_new_chat
    )

    st.markdown(
        "<div style='color:#BAC8D7;font-size:11px;"
        "font-weight:700;letter-spacing:1.5px;"
        "margin:22px 0 10px;'>RECENTS</div>",
        unsafe_allow_html=True
    )

    # Display saved conversations, newest first
    sorted_chats = sorted(
        st.session_state.chat_sessions.items(),
        key=lambda item: item[1].get("updated_at", ""),
        reverse=True
    )

    if not sorted_chats:
        st.caption("Your conversations will appear here.")

    for chat_id, chat in sorted_chats:
        col1, col2 = st.columns([5, 1])

        with col1:
            st.button(
                "💬 " + chat.get("title", "New Conversation"),
                key=f"history_{chat_id}",
                use_container_width=True,
                on_click=open_chat,
                args=(chat_id,)
            )

        with col2:
            if st.button(
                "⋮",
                key=f"delete_menu_{chat_id}",
                help="Delete conversation"
            ):
                st.session_state[f"confirm_delete_{chat_id}"] = True

        if st.session_state.get(f"confirm_delete_{chat_id}", False):
            st.warning("Delete this conversation?")
            yes_col, no_col = st.columns(2)

            with yes_col:
                if st.button("Delete", key=f"yes_delete_{chat_id}"):
                    st.session_state.chat_sessions.pop(chat_id, None)

                    if st.session_state.active_chat_id == chat_id:
                        create_new_chat()

                    st.session_state.pop(f"confirm_delete_{chat_id}", None)
                    save_chat_history()
                    st.rerun()

            with no_col:
                if st.button("Cancel", key=f"no_delete_{chat_id}"):
                    st.session_state.pop(f"confirm_delete_{chat_id}", None)
                    st.rerun()

# Profile section at bottom
    # Profile section at bottom of sidebar
    st.markdown("""
    <div style="height:35px;"></div>
    <hr style="border-color:#34485D;">
    """, unsafe_allow_html=True)

    with st.expander("👤  My Profile", expanded=False):
        st.text_input(
            "Display name",
            key="profile_name"
        )
        st.caption("CDS COMMAND AI · Student Profile")

# =========================================================
# 8. MAIN HEADER
# =========================================================

st.markdown("""
<div class="cds-header">
    <div class="cds-eyebrow">YOUR CDS PREPARATION PARTNER</div>
    <div class="cds-title">🪖 CDS COMMAND AI</div>
    <div class="cds-description">
        Prepare with purpose. Practise with discipline.
        Build your understanding one topic at a time.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 9. CHAT INPUT AND MESSAGE PROCESSING
# =========================================================

# Declare chat input before rendering the welcome screen. Streamlit keeps
# st.chat_input pinned to the bottom of the main app area.
typed_prompt = st.chat_input(
    "Ask CDS COMMAND anything about your preparation..."
)

pending_prompt = st.session_state.pending_prompt
user_prompt = typed_prompt or pending_prompt

# Process a new prompt before choosing the screen. This ensures the welcome
# screen disappears immediately when a message or welcome card is selected.
needs_response = False
if user_prompt:
    st.session_state.pending_prompt = None
    st.session_state.messages.append({
    "role": "user",
    "content": user_prompt,
})

save_current_chat()
needs_response = True

# =========================================================
# 10. WELCOME SCREEN
# =========================================================

if not st.session_state.messages:
    st.markdown("## Welcome, Aspirant.")
    st.markdown(
        "What would you like to focus on today? Choose a starting "
        "point below or enter your own question."
    )
    st.write("")

    left, right = st.columns(2, gap="medium")

    with left:
        st.button(
            "📘  Learn a CDS topic",
            key="welcome_learn",
            use_container_width=True,
            on_click=select_prompt,
            args=(
                "Help me study an important CDS topic. Ask me which "
                "subject I want if needed, then explain it simply.",
            ),
        )
        st.button(
            "✍️  Improve English",
            key="welcome_english",
            use_container_width=True,
            on_click=select_prompt,
            args=(
                "Help me improve CDS English through grammar, "
                "vocabulary and error-spotting practice.",
            ),
        )

    with right:
        st.button(
            "🎯  Practise MCQs",
            key="welcome_mcqs",
            use_container_width=True,
            on_click=select_prompt,
            args=(
                "Ask me to choose a CDS subject and difficulty, "
                "then begin MCQ practice.",
            ),
        )
        st.button(
            "🌍  Revise General Knowledge",
            key="welcome_gk",
            use_container_width=True,
            on_click=select_prompt,
            args=(
                "Help me revise CDS General Knowledge, beginning "
                "with important Polity, History and Geography topics.",
            ),
        )

    st.write("")
    st.divider()

# =========================================================
# 11. CHAT HISTORY AND AI RESPONSE
# =========================================================

if st.session_state.messages:
    st.markdown("### Study conversation")

    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            left, right = st.columns([1, 4])
            with right:
                with st.container(key=f"user_bubble_{i}"):
                    st.markdown(message["content"])
        else:
            left, right = st.columns([4, 1])
            with left:
                with st.container(key=f"ai_bubble_{i}"):
                    st.markdown(message["content"])

if needs_response:
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("CDS COMMAND AI is preparing your answer..."):
            answer = get_ai_response(st.session_state.messages)
        st.markdown(answer)

    st.session_state.messages.append({
    "role": "assistant",
    "content": answer,
})

save_current_chat()

# =========================================================
# 12. FOOTER
# =========================================================

st.markdown("""
<div class="cds-footer">
    CDS COMMAND AI · Learn consistently. Practise purposefully.
    <br>
    AI-generated answers may contain errors. Verify official
    examination information with UPSC.
</div>
""", unsafe_allow_html=True)
