import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")


class Main:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Default model

        self.json_data = json.loads("config.json")

        self.conversation = [
            {"role": "system", "content": self.json_data["prompts"["system_prompt"]]}
        ]


    def set_model(self, model):
        self.model = model

    def get_response(self, message, max_tokens=150):
        if message == "/dump":
            formatted_response = json.dumps(self.conversation, indent=2)
        else:
            self.conversation.append({"role": "user", "content": message})
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                max_tokens=max_tokens,
                tools=[{"type": "file_search"}]
            )
            formatted_response = response.choices[0].message.content
            self.conversation.append({"role": "assistant", "content": formatted_response})
        return formatted_response
