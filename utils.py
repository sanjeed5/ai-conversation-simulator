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
    
    # Generate a unique filename based on timestamp and thread ID
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    thread_id = conversation_data.get("thread_id", "no_thread")
    filename = f"conversation_run_{timestamp}_thread_{thread_id}.json"
    filepath = runs_dir / filename
    
    # Save the data to the file with ensure_ascii=False to properly handle Unicode
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(conversation_data, f, indent=2, ensure_ascii=False)
    
    print(f"Conversation saved to {filepath} with thread ID: {thread_id}") 