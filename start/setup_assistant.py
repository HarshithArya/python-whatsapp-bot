#!/usr/bin/env python3
"""
Setup script to create and configure your OpenAI assistant for WhatsApp integration.
Run this script once to set up your assistant and get the assistant ID.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def setup_assistant():
    """Create a new OpenAI assistant and return its ID"""
    
    # Check if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to your .env file")
        return None
    
    client = OpenAI(api_key=api_key)
    
    # Get assistant configuration from environment
    assistant_name = os.getenv("ASSISTANT_NAME", "WhatsApp AI Assistant")
    assistant_instructions = os.getenv("ASSISTANT_INSTRUCTIONS", 
        "You're a helpful WhatsApp assistant. Be friendly, concise, and helpful in your responses.")
    
    print(f"🤖 Creating assistant: {assistant_name}")
    print(f"📝 Instructions: {assistant_instructions}")
    
    # Check if user wants to upload a knowledge base file
    upload_file = input("\n📁 Do you want to upload a knowledge base file? (y/n): ").lower().strip()
    file_id = None
    
    if upload_file == 'y':
        file_path = input("📂 Enter the path to your file (e.g., data/faq.pdf): ").strip()
        if os.path.exists(file_path):
            try:
                print(f"📤 Uploading file: {file_path}")
                file = client.files.create(file=open(file_path, "rb"), purpose="assistants")
                file_id = file.id
                print(f"✅ File uploaded successfully! File ID: {file_id}")
            except Exception as e:
                print(f"❌ Error uploading file: {e}")
                return None
        else:
            print(f"❌ File not found: {file_path}")
            return None
    
    # Create the assistant
    try:
        tools = [{"type": "retrieval"}] if file_id else []
        file_ids = [file_id] if file_id else []
        
        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=assistant_instructions,
            tools=tools,
            model="gpt-4-1106-preview",
            file_ids=file_ids,
        )
        
        print(f"\n✅ Assistant created successfully!")
        print(f"🆔 Assistant ID: {assistant.id}")
        print(f"📋 Name: {assistant.name}")
        print(f"🤖 Model: {assistant.model}")
        print(f"🛠️ Tools: {[tool['type'] for tool in assistant.tools]}")
        
        return assistant.id
        
    except Exception as e:
        print(f"❌ Error creating assistant: {e}")
        return None

def main():
    print("🚀 OpenAI Assistant Setup for WhatsApp Bot")
    print("=" * 50)
    
    assistant_id = setup_assistant()
    
    if assistant_id:
        print(f"\n📝 Next steps:")
        print(f"1. Add this assistant ID to your .env file:")
        print(f"   OPENAI_ASSISTANT_ID=\"{assistant_id}\"")
        print(f"2. Make sure your WhatsApp Business API is configured")
        print(f"3. Run your Flask app with: python run.py")
        print(f"4. Test by sending a message to your WhatsApp number")
    else:
        print("\n❌ Setup failed. Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 