# main.py
from AI.ai import Main  # Import the Main class from AI.py

def main():
    assistant = Main()  # Initialize the Main class instance

    print("*******************************\nNetzerGPT (type 'exit' to quit)\n*******************************")

    while True:
        user_input = input("\nYou > ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        max_tokens = 100  # Default max tokens
        response = assistant.get_response(user_input, max_tokens=max_tokens)  # Get response from assistant

if __name__ == "__main__":
    main()
