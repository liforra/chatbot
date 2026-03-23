# IT Support Chatbot Ralf

A simple IT support chatbot created for educational purposes in Lernfeld 6.

## What it does

This chatbot:
- Communicates only in plain text (no markdown formatting)
- Uses the Groq API with AI model openai/gpt-oss-120b
- Follows standard IT support procedures:
  - Greets users professionally
  - Asks questions to understand problems
  - Shows empathy with frustrated users
  - Communicates solutions clearly
  - Closes conversations properly
- Designed for users with limited technical knowledge
- Uses ANSI escape codes for terminal text formatting

## Setup

### Recommended: Using UV (fastest)
1. Install [UV](https://docs.astral.sh/uv/) if you don't have it:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:
   ```
   git clone https://github.com/liforra/s-chatbot.git
   cd s-chatbot
   ```

3. Install dependencies with UV:
   ```
   uv sync
   ```

4. Create a config.toml file with your Groq API key:
   ```toml
   [keys]
   groq = "your-api-key-here"
   
   [log]
   level = "info"
   file = "chatbot.log"
   
   [model]
   name = "openai/gpt-oss-120b"
   ```

5. Run the chatbot:
   ```
   uv run python main.py
   ```

### Alternative: Using pip
1. Clone the repository:
   ```
   git clone https://github.com/liforra/s-chatbot.git
   cd s-chatbot
   ```

2. Install dependencies:
   ```
   pip install -e .
   ```

3. Create a config.toml file with your Groq API key:
   ```toml
   [keys]
   groq = "your-api-key-here"
   
   [log]
   level = "info"
   file = "chatbot.log"
   
   [model]
   name = "openai/gpt-oss-120b"
   ```

4. Run the chatbot:
   ```
   python main.py
   ```

## How it works

1. Reads configuration settings
2. Sets up logging system
3. Initializes Groq API client (if API key available)
4. Loads support protocol from system.md
5. Processes user input and generates appropriate IT support responses

## Created for

This project was developed as part of Lernfeld 6 coursework at ITECH BS14, Klasse CDP.