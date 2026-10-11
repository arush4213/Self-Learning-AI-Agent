import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
memory = []
def think(question, memory):
    memory_context = "\n".join(memory) if memory else "No previous memory."
    prompt = f"""You are a self-learning AI agent.

Your memory from previous interactions:
{memory_context}

Current question: {question}

Think step by step:
1. What do I already know about this from memory?
2. What is the answer to this question?
3. What should I remember for future questions?

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
def run_agent(question):
    print(f"\n{'='*50}")
    print(f"QUESTION: {question}")
    print(f"{'='*50}")
    response = think(question, memory)
    thought, answer, remember = parse_response(response)
    print(f"\nTHOUGHT: {thought}")
    print(f"ANSWER: {answer}")
    print(f"REMEMBER: {remember}")
    if remember:
        memory.append(f"Q: {question} -> {remember}")
    return answer

run_agent("What is neuromorphic computing?")
run_agent("How does it relate to artificial intellignece?")
run_agent("What did we just discuss?")
    