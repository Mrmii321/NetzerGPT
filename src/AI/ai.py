import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")


class Main:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"  # Adjusting to a default model

        # Loading configuration file
        with open("config.json") as f:
            self.json_data = json.load(f)

        # Load assistant prompts from config file
        self.conversation = [
            {"role": "system", "content": self.json_data["prompts"]["system_prompt"]}
        ]

    def set_model(self, model):
        self.model = model

    def get_response(self, message, max_tokens=150):
        if message == "/dump":
            formatted_response = json.dumps(self.conversation, indent=2)
        else:
            # Add user message to conversation
            self.conversation.append({"role": "user", "content": message})
            
            # Assistant ID (replace with your actual Assistant ID)
            ASSISTANT_ID = "<your-assistant-id>"  # Add your Assistant ID

            # Create a thread and run the assistant
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id, 
                role="user", 
                content=message
            )

            run = self.client.beta.threads.runs.create(
                thread_id=thread.id, 
                assistant_id=ASSISTANT_ID
            )

            # Retrieve assistant's response
            response_messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            formatted_response = response_messages['data'][0]['content'][0]['text']['value']

            # Append assistant response to conversation
            self.conversation.append({"role": "assistant", "content": formatted_response})

        return formatted_response