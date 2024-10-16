import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv(".env")


class Main:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo"  # Default model
        self.assistant_id = "your_assistant_id"  # Use your existing Assistant ID

        # Load configuration
        with open("config.json", "r") as file:
            self.json_data = json.load(file)

        # Create a new thread (conversation)
        self.thread = self.client.beta.threads.create()

        # Add initial system prompt to the conversation
        self.conversation = [{"role": "system", "content": self.json_data["prompts"]["system_prompt"]}]

    def set_model(self, model):
        self.model = model

    def get_response(self, message, max_tokens=150):
        if message == "/dump":
            formatted_response = json.dumps(self.conversation, indent=2)
        else:
            # Add user message to the conversation
            self.conversation.append({"role": "user", "content": message})

            # Add the message to the thread
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id, 
                role="user", 
                content=message
            )

            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id, 
                assistant_id=self.assistant_id
            )

            # Poll for completion
            while run.status != "completed":
                run = self.client.beta.threads.runs.retrieve(run_id=run.id)
                time.sleep(2)

            # Retrieve the assistant's response
            response = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            formatted_response = response.data[-1].content[0].text.value

            # Add the assistant's response to the conversation
            self.conversation.append({"role": "assistant", "content": formatted_response})

        return formatted_response
