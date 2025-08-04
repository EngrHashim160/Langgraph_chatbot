# Chatbot using LangGraph-Persistance

A modular chatbot framework built using LangGraph, designed to demonstrate the interaction between a frontend chat interface and a LangChain-based backend. This project serves as a foundational prototype for building AI assistant applications that leverage conversational workflows.

## Features

- LangChain + LangGraph based backend logic
- Simple terminal-based frontend chat interface
- Modular architecture for easy extension
- Environment variable-based configuration
- Extensible with memory and custom tools

## Project Structure

```
Chatbot_Langgraph/
├── chatbot_backend.py     # Core LangGraph workflow logic
├── chatbot_frontend.py    # CLI-based chat interface
├── chatbot.ipynb          # Notebook for interactive testing
├── requirements.txt       # Python dependencies
└── .gitignore             # Git ignored files
```

## Getting Started

### Installation

1. **Clone the repository** (or extract the zip):

```bash
git clone <repo-url>
cd Chatbot_Langgraph
```

2. **Create a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Make sure to set your OpenAI API key in your environment:

```bash
export OPENAI_API_KEY=your-api-key
```

### Running the Chatbot

Launch the frontend interface:

```bash
python chatbot_frontend.py
```

Or test directly with the backend logic in `chatbot.ipynb`.

## Requirements

This project depends on:

- langgraph
- langchain
- langchain_openai
- dotenv
- langchain_groq
- streamlit

## License

This project is open-source and available under the MIT License.
