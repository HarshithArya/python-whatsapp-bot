from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "WhatsApp AI Assistant")
ASSISTANT_INSTRUCTIONS = os.getenv("ASSISTANT_INSTRUCTIONS", "You're a helpful WhatsApp assistant. Be friendly, concise, and helpful in your responses.")

# Initialize client only if API key is available
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    logging.warning("OPENAI_API_KEY not found. OpenAI features will be disabled.")


def upload_file(path):
    if not client:
        raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY.")
    # Upload a file with an "assistants" purpose
    file = client.files.create(
        file=open(path, "rb"), purpose="assistants"
    )
    return file


def create_assistant(file=None):
    """
    Create a new assistant with optional file attachment
    """
    if not client:
        raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY.")
    
    file_ids = [file.id] if file else []
    
    assistant = client.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_INSTRUCTIONS,
        tools=[{"type": "retrieval"}] if file else [],
        model="gpt-4-1106-preview",
        file_ids=file_ids,
    )
    return assistant


# Use context manager to ensure the shelf file is closed properly
def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id


def run_assistant(thread, name):
    if not client:
        raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY.")
    
    if not OPENAI_ASSISTANT_ID:
        raise ValueError("OPENAI_ASSISTANT_ID environment variable is required")
    
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    # https://platform.openai.com/docs/assistants/how-it-works/runs-and-run-steps#:~:text=under%20failed_at.-,Polling%20for%20updates,-In%20order%20to
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        # Handle failed runs
        if run.status == "failed":
            logging.error(f"Assistant run failed: {run.last_error}")
            raise Exception(f"Assistant run failed: {run.last_error}")

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    logging.info(f"Generated message: {new_message}")
    return new_message


def generate_response(message_body, wa_id, name):
    if not client:
        return "I'm sorry, but the AI service is not configured. Please set up your OpenAI API key to enable AI responses."
    
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        logging.info(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread
    else:
        logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread, name)

    return new_message
