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
def search_Web(query):
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
    search_results = search_Web(question)
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

st.set_page_config(page_title="Self-Learning AI Agent")
st.title("Self-Learning AI Agent")
st.caption("Powered by Gemini + Web Search + Persistant Memory")
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
with st.sidebar:
    st.header("Agent Memory")
    if st.session_state.memory:
        for i, m in enumerate(st.session_state.memory, 1):
            st.write(f"{i}. {m}")
    else:
        st.write("No memory yet.")
    if st.button("Clear Memory"):
        st.session_state.memory = []
        save_memory([])
        st.rerun()
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
if prompt := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = think(prompt, st.session_state.memory)
            thought, answer, remember = parse_response(response)
            with st.expander("Thought Process"):
                st.write(thought)
            st.write(answer)
            if remember:
                st.session_state.memory.append(f"G: {prompt} -> {remember}")
                save_memory(st.session_state.memory)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.rerun()