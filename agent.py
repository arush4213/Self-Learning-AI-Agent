import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
def run_agent(question):
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=question
    )
    return response.text
result = run_agent("Whta is neuromorphic computing?")
print(result)