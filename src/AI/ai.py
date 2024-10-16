import os
import json
from openai import OpenAI
from openai import AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override  # Import override

load_dotenv(".env")


class EventHandler(AssistantEventHandler):
    """
    Handles events for the OpenAI assistant responses.
    
    Inherits from AssistantEventHandler to manage response streaming.
    
    Attributes:
        formatted_response (str): Holds the full response from the assistant.
    """

    def __init__(self):
        """
        Initializes the EventHandler and sets up the formatted_response.
        """
        super().__init__()  # Call the superclass initializer
        self.formatted_response = ""

    @override  # Use the override decorator
    def on_text_created(self, text) -> None:
        """
        Event triggered when the assistant creates text.
        
        Args:
            text (str): The text created by the assistant.
        """
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """
        Event triggered for each delta of text generated by the assistant.
        
        Args:
            delta (object): The delta object containing the text change.
            snapshot (object): The snapshot of the current state of the conversation.
        """
        print(delta.value, end="", flush=True)
        self.formatted_response += delta.value

    # Additional methods can be implemented if needed


class Main:
    """
    The main class for interacting with the AI.

    Attributes:
        client (OpenAI): The OpenAI client for API interaction.
        model (str): The model identifier for the AI.
        json_data (dict): The configuration loaded from a JSON file.
        assistant_id (str): The ID of the assistant to interact with.
        thread (object): The conversation thread created for interaction.
    """
    
    def __init__(self):
        """
        Initializes the Main class, sets up the OpenAI client, and loads configuration.
        """
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

    def set_model(self, model: str):
        """
        Updates the model used by the AI.
        
        Args:
            model (str): The new model identifier to set.
        """
        self.model = model

    def get_response(self, message: str, max_tokens: int = 150) -> str:
        """
        Generates a response from the AI based on the provided message.

        If the message is "/dump", it fetches all messages in the thread.
        Otherwise, it sends the user message to the assistant and streams the response.
        
        Args:
            message (str): The user message to send to the assistant.
            max_tokens (int): The maximum number of tokens for the response (default is 150).

        Returns:
            str: The formatted response from the assistant or an error message.
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
