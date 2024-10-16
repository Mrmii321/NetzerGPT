from AI import ai

def main():
    main = Main()

    print("NetzerGPT (type 'exit' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        max_tokens = 150  # Default max tokens
        response = main.get_response(user_input, max_tokens=max_tokens)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
