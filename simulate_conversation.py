import getpass
import os
import json
import datetime
import uuid
from pathlib import Path
from dotenv import load_dotenv
from config_simulate_conversation import (
    SYSTEM_PROMPT,
    SIMULATED_USER_PROMPT,
    SYSTEM_MODEL,
    SIMULATED_USER_MODEL,
    MAX_MESSAGES,
)
from utils import save_conversation_to_file

# Import LangSmith thread functionality
from langsmith import Client
import os

load_dotenv()

# Initialize LangSmith client
client = Client()

def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")


_set_if_undefined("OPENAI_API_KEY")
_set_if_undefined("LANGSMITH_API_KEY")
_set_if_undefined("LANGSMITH_PROJECT")

# Ensure LangSmith tracing is enabled
if not os.environ.get("LANGSMITH_TRACING"):
    os.environ["LANGSMITH_TRACING"] = "true"

from typing import List

import openai


# Agent to be tested
def my_chat_bot(messages: List[dict]) -> dict:
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
    messages = [system_message] + messages
    
    # Get the thread ID from environment
    thread_id = os.environ.get("LANGSMITH_SESSION_ID", "")
    
    # Create completion with metadata for LangSmith
    completion = openai.chat.completions.create(
        messages=messages, 
        model=SYSTEM_MODEL,
        extra_headers={"X-LangSmith-Session-Id": thread_id} if thread_id else {}
    )
    return completion.choices[0].message.model_dump()

# print(my_chat_bot([{"role": "user", "content": "hi!"}]))

# Simulated user agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

system_prompt_template = """{instructions}

When you are finished with the conversation, respond with a single word 'FINISHED'"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
instructions = SIMULATED_USER_PROMPT

prompt = prompt.partial(instructions=instructions)

model = ChatOpenAI(model=SIMULATED_USER_MODEL)

simulated_user = prompt | model

from langchain_core.messages import HumanMessage

messages = [HumanMessage(content="Hi! How can I help you?")]

# Agent simulation -> 2 nodes - 1 for chat chat bot and 1 for simulated user
# we will assume that HumanMessages are messages from the simulated user. This means that we need some logic in the simulated user node to swap AI and Human messages.

from langchain_community.adapters.openai import convert_message_to_dict
from langchain_core.messages import AIMessage


def chat_bot_node(state):
    messages = state["messages"]
    # Convert from LangChain format to the OpenAI format, which our chatbot function expects.
    messages = [convert_message_to_dict(m) for m in messages]
    # Call the chat bot
    chat_bot_response = my_chat_bot(messages)
    # Respond with an AI Message
    return {"messages": [AIMessage(content=chat_bot_response["content"])]}

def _swap_roles(messages):
    new_messages = []
    for m in messages:
        if isinstance(m, AIMessage):
            new_messages.append(HumanMessage(content=m.content))
        else:
            new_messages.append(AIMessage(content=m.content))
    return new_messages


def simulated_user_node(state):
    messages = state["messages"]
    # Swap roles of messages
    new_messages = _swap_roles(messages)
    # Call the simulated user with thread metadata
    response = simulated_user.invoke(
        {"messages": new_messages},
        config={"metadata": {"session_id": os.environ.get("LANGSMITH_SESSION_ID")}}
    )
    # This response is an AI message - we need to flip this to be a human message
    return {"messages": [HumanMessage(content=response.content)]}

def should_continue(state):
    messages = state["messages"]
    if len(messages) > MAX_MESSAGES:
        return "end"
    elif messages[-1].content == "FINISHED":
        return "end"
    else:
        return "continue"
    
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)
graph_builder.add_node("user", simulated_user_node)
graph_builder.add_node("chat_bot", chat_bot_node)
# Every response from  your chat bot will automatically go to the
# simulated user
graph_builder.add_edge("chat_bot", "user")
graph_builder.add_conditional_edges(
    "user",
    should_continue,
    # If the finish criteria are met, we will stop the simulation,
    # otherwise, the virtual user's message will be sent to your chat bot
    {
        "end": END,
        "continue": "chat_bot",
    },
)
# The input will first go to your chat bot
graph_builder.add_edge(START, "chat_bot")
simulation = graph_builder.compile()

# Create a thread for this conversation
thread_id = str(uuid.uuid4())
print(f"Created thread with ID: {thread_id}")

# Set the thread ID in the environment for LangSmith to use
os.environ["LANGSMITH_SESSION_ID"] = thread_id

# Store the conversation for saving to file
conversation_history = []

for chunk in simulation.stream({"messages": []}):
    # Print out all events aside from the final end chunk
    if END not in chunk:
        # Extract and print only the message content
        for node, data in chunk.items():
            for message in data["messages"]:
                print(f"{node}: {message.content}")
                # Store the message in conversation history
                conversation_history.append({
                    "role": node,
                    "content": message.content
                })
        print("----")
    else:
        # Conversation has ended, save to file
        config_data = {
            "system_prompt": SYSTEM_PROMPT,
            "simulated_user_prompt": SIMULATED_USER_PROMPT,
            "system_model": SYSTEM_MODEL,
            "simulated_user_model": SIMULATED_USER_MODEL,
            "max_messages": MAX_MESSAGES,
            "thread_id": thread_id
        }
        
        # Create the data structure to save
        conversation_data = {
            "config": config_data,
            "conversation": conversation_history,
            "thread_id": thread_id
        }
        
        # Save the conversation to a file
        try:
            save_conversation_to_file(conversation_data)
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")

# Ensure conversation is saved even if END block is not executed
if conversation_history:
    config_data = {
        "system_prompt": SYSTEM_PROMPT,
        "simulated_user_prompt": SIMULATED_USER_PROMPT,
        "system_model": SYSTEM_MODEL,
        "simulated_user_model": SIMULATED_USER_MODEL,
        "max_messages": MAX_MESSAGES,
        "thread_id": thread_id
    }
    
    # Create the data structure to save
    conversation_data = {
        "config": config_data,
        "conversation": conversation_history,
        "thread_id": thread_id
    }
    
    # Save the conversation to a file
    try:
        save_conversation_to_file(conversation_data)
    except Exception as e:
        print(f"Error saving conversation at the end of the script: {str(e)}")