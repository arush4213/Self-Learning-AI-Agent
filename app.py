import streamlit as st
import os
import json
from dotenv import load_dotenv
from google import genai
from ddgs import DDGS

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MEMORY_FILE = "memory.json"
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
def search_web(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        if results:
            output = ""
            for r in results:
                output += f"- {r['title']}: {r['body']}\n"
            return output
        return "No results found."
def think(question, memory):
    memory_context = "\n".join(memory) if memory else "No previous memory."
    search_results = search_web(question)
    prompt = f"""You are a self-learning AI agent.
Your memory from previous interactions:
{memory_context}
Real-time web search results for this question:
{search_results}
Current question: {question}
Think step by step:
1. What do I already know about this from memory?
2. What do the web search results tell me?
3. What is the best answer combining memory and search results?
4. What should I remember for future questions?
Format your response as:
THOUGHT: your thinking process
ANSWER: your final answer
REMEMBER: what to store in memory
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text
def parse_response(response):
    thought, answer, remember = "", "", ""
    current = None
    buffer = []
    for line in response.split("\n"):
        if line.startswith("THOUGHT:"):
            current = "thought"
            buffer = [line.replace("THOUGHT:", "").strip()]
        elif line.startswith("ANSWER:"):
            if current == "thought":
                thought = " ".join(buffer).strip()
            current = "answer"
            buffer = [line.replace("ANSWER:", "").strip()]
        elif line.startswith("REMEMBER:"):
            if current == "answer":
                answer = " ".join(buffer).strip()
            current = "remember"
            buffer = [line.replace("REMEMBER:", "").strip()]
        else:
            if current:
                buffer.append(line.strip())
    if current == "remember":
        remember = " ".join(buffer).strip()
    return thought, answer, remember

st.set_page_config(
    page_title="AI Agent",
    page_icon="🧠",
    layout="centered"
)
st.markdown("""
<style>
    .stApp { background-color: #212121; }
    .stChatInput input {
        border-radius: 12px;
        border: 1px solid #3f3f3f;
        background-color: #2f2f2f;
        color: #ececec;
        font-size: 15px;
        padding: 12px 16px;
    }
    .stSidebar { background-color: #171717; border-right: 1px solid #2f2f2f; }
    .stButton button {
        background-color: #2f2f2f;
        border: 1px solid #3f3f3f;
        border-radius: 8px;
        color: #ececec;
        font-size: 13px;
    }
    .stButton button:hover { background-color: #3f3f3f; }
    div[data-testid="stChatMessageContent"] p { font-size: 15px; line-height: 1.6; color: #ececec; }
    .stExpander { border: 1px solid #3f3f3f; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("### Memory")
    st.markdown("---")
    if "memory" not in st.session_state:
        st.session_state.memory = load_memory()
    if st.session_state.memory:
        for i, m in enumerate(st.session_state.memory, 1):
            st.markdown(f"<small>{i}. {m}</small>", unsafe_allow_html=True)
    else:
        st.markdown("<small style='color: #999'>No memory yet.</small>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Clear Memory"):
        st.session_state.memory = []
        save_memory([])
        st.rerun()

st.markdown("### AI Agent")
st.markdown("<p style='color: #666; font-size: 13px; margin-top: -12px;'>Self-learning · Web search · Persistent memory</p>", unsafe_allow_html=True)
st.markdown("---")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
if prompt := st.chat_input("Message AI Agent..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = think(prompt, st.session_state.memory)
            thought, answer, remember = parse_response(response)
            with st.expander("Thought process"):
                st.write(thought)
            st.write(answer)
            if remember:
                st.session_state.memory.append(f"Q: {prompt} -> {remember}")
                save_memory(st.session_state.memory)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.rerun()