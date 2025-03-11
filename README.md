# AI Conversation Simulator

A tool for simulating conversations between an AI assistant and a virtual user for testing and development purposes.

## Overview

This project allows you to:
- Test AI assistant behavior with a simulated user
- Configure both the AI assistant and simulated user personas
- Run automated conversations to evaluate AI performance
- Set conversation parameters like maximum message count
- Save conversation history to JSON files for analysis and review

## How It Works

The simulator uses LangGraph to create a conversation flow between:
1. Your AI assistant (configurable system prompt and model)
2. A simulated user (configurable persona and model)

The conversation continues until either:
- The maximum number of messages is reached
- The simulated user responds with "FINISHED"

All conversations are automatically saved to the `runs` directory with timestamps for easy reference and analysis.

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

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

3. Set up your OpenAI API key
```bash
# Either set it in your environment
export OPENAI_API_KEY=your-api-key

# Or create a .env file
echo "OPENAI_API_KEY=your-api-key" > .env
```

### Configuration

Edit `config_simulate_conversation.py` to customize:
- `SYSTEM_PROMPT`: The system prompt for your AI assistant
- `SYSTEM_MODEL`: The OpenAI model for your AI assistant (default: gpt-4o-mini)
- `SIMULATED_USER_PROMPT`: The persona for the simulated user
- `SIMULATED_USER_MODEL`: The OpenAI model for the simulated user (default: gpt-4o-mini)
- `MAX_MESSAGES`: Maximum number of messages before ending the conversation

### Running a Simulation

```bash
uv run simulate_conversation.py
# or
python simulate_conversation.py
```

## Conversation Storage

All conversations are automatically saved to JSON files in the `runs` directory. Each file includes:
- Complete conversation history with timestamps
- Configuration settings used for the simulation
- Role information (AI assistant vs simulated user)

This makes it easy to:
- Review conversation quality and AI performance
- Compare different system prompts and configurations
- Build datasets for further analysis or training

## Customization

You can modify the `my_chat_bot` function in `simulate_conversation.py` to test different AI assistant implementations.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
