# Self-Learning AI Agent

An AI-powered assistant built with Python and Google's Gemini API that combines with persistent memory to provide context-aware responses across conversations.

The project explores how an AI agent can retrieve information, use previous interactionsas context, and store useful information for future conversations.

## Features

- **AI-Powered Responses:** Uses Google's Gemini API to generate answers to user queries.
- **Web Search:** Retrieves relevant web results using DuckDuckGo Search.
- **Persistent Memory:** Stores short memory notes in local JSON file.
- **Context-Aware Conversations:** Uses saved memories to provide more relevant responses.
- **Terminal Interface:** Interact with the agent directly through the command line.
- **Web Interface:** Chat with the agent through a Streamlit application.
- **Memory Management:** View saved memories in the terminal and clear memory through the web interface.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Google Gemini API | Language model and response generation |
| Google Gen AI SDK | Integration with Gemini |
| DuckDuckGo Search (`ddgs`) | Web information retrieval |
| Streamlit | Interactive web interface |
| python-dotenv | Environment variable management |
| JSON | Persistent memory storage |

## Project Structure

```text
Self-Learning-AI-Agent/
├── agent.py
├── app.py
├── requirements.txt
├── .env                  # Create locally; never commit
├── memory.json           # Generated when memory is saved
├── .streamlit/
│   └── config.toml
├── .gitignore
├── LICENSE
└── README.md
```
## How It Works

The agent follows a simple workflow whenever a user submits a question:

1. **Receive Input:** The agent accepts a question from the user.
2. **Retrieve Memory:** Previously stored information is loaded from 'memory.json'.
3. **Search the Web:** The agent retrieves relevant search results.
4. **Generate a Response:** The question, memory, and search results are sent to Gemini.
5. **Extract Memory:** The response is processed to identify information worth remembering.
6. **Save Information:** The extracted memory is appended to 'memory.json' for future interactions.

This process allows the agent to use information from previous conversations without requiring the language model to be retrained.

> **Important:** This project uses persistent memory for context-based adaptions. It does not modify Gemini's model weights or perform continous model training.

## Getting Started

### Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer recommended
- A Google Gemini API key
- An active internet connection

### 1. Clone the Repository

```bash
git clone https://github.com/arush4213/Self-Learning-AI-Agent.git
cd Self-Learning-AI-Agent
```

### 2. Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the API Key

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Replace the placeholder with your actual key.

**Security note:** Never upload your `.env` file or expose your API key in a public repository.

### 5. Run the Application

**Web interface:**

```bash
streamlit run app.py
```

Open the local URL printed in the terminal, usually:

`http://localhost:8501`

**Terminal interface:**

```bash
python agent.py
```

Type your question to interact with the agent.

Available terminal commands include:

- `memory` to display saved memories.
- `quit` to exit the application.

## Memory System

The agent stores information in a local file named `memory.json`.

The memory system allows the application to:

- Retain selected information across separate interactions.
- Reuse previously saved context when generating answers.
- Maintain a lightweight memory system without requiring a database server.

Memory is stored locally, but the relevant context may be sent to the Gemini API when generating responses. Avoid storing passwords, API keys, or sensitive personal information.

## Current Limitations

This project is an experimental implementation and has several limitations:

- Memory is stored as a simple list of text notes rather than a vector database.
- The agent does not automatically evaluate whether a saved memory is correct or useful.
- Web search results may be incomplete or inaccurate.
- The response parser relies on the model following the expected response format.
- Streamlit chat history is separate from the persistent memory file.
- The agent does not train or fine-tune its underlying language model.

## Future Improvements

Potential improvements include:

- Add source links and citations to web search results.
- Implement semantic memory retrieval using embeddings.
- Add memory editing and deletion for individual entries.
- Improve error handling for API failures and invalid configuration.
- Introduce automated tests for memory persistence and response parsing.
- Add response feedback and memory relevance scoring.
- Improve the user interface and conversation history management.

## Privacy and Security

- API credentials should be stored in environment variables.
- The `.env` file should be excluded from version control.
- Local memory files should be handled carefully because they may contain personal information.
- Important information retrieved from the web should be verified against reliable sources.

## License

This project is licensed under the [MIT License](https://github.com/arush4213/Self-Learning-AI-Agent/blob/main/LICENSE).

## Acknowledgements

Built as a learning project to explore AI agents, large language models, web retrieval, and persistent memory using Python.

---

**Made with Python, Gemini, and a little curiosity about how AI agents can use memory.**