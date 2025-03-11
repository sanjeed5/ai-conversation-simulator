import json
import datetime
import os
from pathlib import Path


def save_conversation_to_file(conversation_data):
    """
    Save the conversation data to a JSON file in the 'runs' folder.
    
    Args:
        conversation_data (dict): Dictionary containing the configuration and conversation data
    """
    # Create runs directory if it doesn't exist
    runs_dir = Path("runs")
    runs_dir.mkdir(exist_ok=True)
    
    # Generate a unique filename based on timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_run_{timestamp}.json"
    filepath = runs_dir / filename
    
    # Save the data to the file
    with open(filepath, "w") as f:
        json.dump(conversation_data, f, indent=2)
    
    print(f"Conversation saved to {filepath}") 