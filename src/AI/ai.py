# AI/ai.py
import os
import json
from openai import OpenAI
from openai import AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override

load_dotenv(".env")


class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.formatted_response = ""

    @override
    def on_text_created(self, text) -> None:
        print(f"\nNetzerGPT > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        self.formatted_response += delta.value
        print(delta.value, end="", flush=True)


class Main:
    """
    Main class for interacting with the AI.
    """

    def __init__(self):
        """
        Initialize the Main class, load configuration, and set up OpenAI client.
        """
        print("Initializing Main class...")
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = self.json_data["IDs"]["model"]  # Model ID
        print(f"Model set to: {self.model}")

        # Load configuration from a JSON file
        config_path = r"C:\Users\noahf\OneDrive\Desktop\Development\Python\NetzerGPT\config.json"
        with open(config_path, "r") as file:
            self.json_data = json.load(file)
        print("Configuration loaded from config.json")

        self.assistant_id = self.json_data["IDs"]["assistant"]  # Assistant ID
        self.thread = self.client.beta.threads.create()
        print(f"Thread created with ID: {self.thread.id}")

    def get_response(self, message: str, max_tokens: int = 150) -> str:
        """
        Generates a response from the AI based on the provided message.
        """
        try:
            if message == "/dump":
                # Fetch all messages in the thread
                messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
                formatted_response = json.dumps(
                    [msg.to_dict() for msg in messages], indent=2
                )
                return formatted_response
            else:
                # Create the message and start streaming the assistant's response
                self.client.beta.threads.messages.create(
                    thread_id=self.thread.id, role="user", content=message
                )
                event_handler = EventHandler()

                # Streaming assistant's response
                with self.client.beta.threads.runs.stream(
                    thread_id=self.thread.id,
                    assistant_id=self.assistant_id,
                    instructions=" ".join(self.json_data["prompts"]["system_prompt"]),
                    event_handler=event_handler,
                ) as stream:
                    stream.until_done()

                response = event_handler.formatted_response
                formatted_response, _ = self.process_response(response)
                return formatted_response

        except Exception as e:
            return f"An error occurred: {e}"

    def process_response(self, response):
        """
        Process the assistant's response to replace annotations with inline source citations.
        """
        message_content = response
        annotations = []

        citations = []
        for index, annotation in enumerate(annotations):
            message_content = message_content.replace(annotation['text'], "")
        return message_content, citations
