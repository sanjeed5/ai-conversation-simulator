# AI Conversation Simulator

A tool for simulating conversations between an AI assistant and a virtual user for testing and development purposes.

## Overview

This project allows you to:
- Test AI assistant behavior with a simulated user
- Configure both the AI assistant and simulated user personas
- Run automated conversations to evaluate AI performance
- Track conversations with LangSmith threads for observability
- Save conversation history to JSON files for analysis and review

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- LangSmith API key (optional, for thread tracking)

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/ai-conversation-simulator.git
cd ai-conversation-simulator
```

2. Install dependencies

Using uv (recommended for faster installation):
```bash
# Install uv if you don't have it - https://docs.astral.sh/uv/getting-started/installation/

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

Using pip (alternative):
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys
```
OPENAI_API_KEY=your_openai_api_key
# Optional: For LangSmith thread tracking
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_langsmith_project_name
LANGSMITH_TRACING=true
```

## Usage

Run a simulated conversation:

```bash
python simulate_conversation.py
```

The simulation will:
1. Create a conversation between your AI assistant and a simulated user
2. Continue until the maximum message count or until the user says "FINISHED"
3. Save the conversation to a file in the `runs` directory
4. Create a thread in LangSmith for tracking and analysis

## Configuration

Modify `config_simulate_conversation.py` to customize:

- `SYSTEM_PROMPT`: The system prompt for your AI assistant
- `SYSTEM_MODEL`: The OpenAI model for your AI assistant
- `SIMULATED_USER_PROMPT`: The persona for the simulated user
- `SIMULATED_USER_MODEL`: The OpenAI model for the simulated user
- `MAX_MESSAGES`: Maximum number of messages before ending the conversation

## Features

### Conversation Simulation

The simulator uses LangGraph to create a conversation flow between:
1. Your AI assistant (configurable system prompt and model)
2. A simulated user (configurable persona and model)

### Conversation Storage

All conversations are saved to JSON files in the `runs` directory with:
- Complete conversation history
- Configuration settings used for the simulation
- Role information (AI assistant vs simulated user)
- Timestamp and unique identifiers

### Thread Tracking with LangSmith

When LangSmith integration is enabled:
- Each conversation is tracked as a thread in LangSmith
- Thread IDs are included in saved files for reference
- You can view detailed conversation analytics in the LangSmith UI

#### Viewing Threads in LangSmith

1. Go to [LangSmith](https://smith.langchain.com/)
2. Navigate to your project
3. Click on the "Threads" tab to see all your conversation threads
4. Click on a thread to see the detailed conversation history

## Customization

You can modify the `my_chat_bot` function in `simulate_conversation.py` to test different AI assistant implementations.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
