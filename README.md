# AI Conversation Simulator

A tool for simulating conversations between an AI assistant and a virtual user for testing and development purposes.

## Overview

This project allows you to:
- Test AI assistant behavior with a simulated user
- Configure both the AI assistant and simulated user personas
- Run automated conversations to evaluate AI performance
- Set conversation parameters like maximum message count

## How It Works

The simulator uses LangGraph to create a conversation flow between:
1. Your AI assistant (configurable system prompt and model)
2. A simulated user (configurable persona and model)

The conversation continues until either:
- The maximum number of messages is reached
- The simulated user responds with "FINISHED"

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
```bash
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
python simulate_conversation.py
```

## Customization

You can modify the `my_chat_bot` function in `simulate_conversation.py` to test different AI assistant implementations.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
