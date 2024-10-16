# NetzerGPT

NetzerGPT is a conversational AI assistant built using the OpenAI API. This project consists of two main components: the main program that manages user interaction, and the AI module that handles the backend API interactions with OpenAI.

## Features

- Text-based conversational assistant.
- Real-time response streaming.
- Customizable configuration for OpenAI API and model settings.

## Project Structure

- `main.py`: The main entry point for the application. This script initializes an instance of the AI assistant and manages the user interface.
- `ai.py`: Contains the core AI logic, including OpenAI API calls, assistant event handling, and configuration setup.

## Installation

1. Clone the repository:

   ```sh
   git clone <repository_url>
   ```

2. Install required dependencies:

   ```sh
   pip install openai python-dotenv
   ```

3. Copy the `.env.example` file to `.env` and add your OpenAI API key:

   ```sh
   cp .env.example .env
   ```

   Then, edit `.env` to include your API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application with:

```sh
run.bat
```

Once the program starts, you can type your questions, and NetzerGPT will respond accordingly. To exit the application, type `exit`.

### Commands

- `/dump`: Fetches all messages in the current conversation thread.

## Configuration

NetzerGPT uses a configuration file (`config.json`) to manage settings for the AI assistant. Only the system prompt is included in this file. Changing this setting could interfere with the AI's performance, as modifications may affect its behaviour, responses, or accuracy.

## Requirements

- Python 3.7+
- OpenAI Python SDK
- `.env` file for API credentials