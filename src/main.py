from AI.ai import Main  # Import the Main class from AI.py

def main():
    assistant = Main()  # Initialize the Main class instance

    print("NetzerGPT (type 'exit' to quit)\n******")

    while True:
        user_input = input("\nYou > \n")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        max_tokens = 100  # Default max tokens
        response = assistant.get_response(user_input, max_tokens=max_tokens)  # Use the assistant to get a response

if __name__ == "__main__":
    main()
