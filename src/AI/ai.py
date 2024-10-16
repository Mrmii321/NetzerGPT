import os
import json
from openai import OpenAI
from openai import AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override  # Import override

load_dotenv(".env")


class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()  # Call the superclass initializer
        self.formatted_response = ""

    @override  # Use the override decorator
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
        self.formatted_response += delta.value

    # Implement other methods if needed


class Main:
    """
    The main class for the AI.

    Attributes:
        client (method)
        model (str)
    """
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"  # Corrected model name

        # Load configuration
        with open(r"C:\Users\noahf\OneDrive\Desktop\Development\Python\NetzerGPT\config.json", "r") as file:
            self.json_data = json.load(file)

        # Use your existing Assistant ID or create a new assistant
        self.assistant_id = "asst_djxKX8cZQZHPVNtqbb9GBGE1"  # Replace with your Assistant ID

        # Create a new thread (conversation)
        self.thread = self.client.beta.threads.create()

    def set_model(self, model):
        self.model = model

    def get_response(self, message, max_tokens=150):
        """
        Creates the ai-generated message and streams it.

        
        """
        try:
            if message == "/dump":
                # Fetch all messages in the thread
                messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
                formatted_response = json.dumps([msg.to_dict() for msg in messages], indent=2)
            else:
                # Add user message to the thread
                self.client.beta.threads.messages.create(
                    thread_id=self.thread.id,
                    role="user",
                    content=message
                )

                # Create an EventHandler instance
                event_handler = EventHandler()

                # Start streaming the assistant's response using event_handler
                with self.client.beta.threads.runs.stream(
                    thread_id=self.thread.id,
                    assistant_id=self.assistant_id,
                    instructions=self.json_data["prompts"]["system_prompt"],
                    event_handler=event_handler,
                ) as stream:
                    stream.until_done()

                # Get the full response from the event_handler
                formatted_response = event_handler.formatted_response

            return formatted_response

        except Exception as e:
            return f"An error occurred: {str(e)}"
