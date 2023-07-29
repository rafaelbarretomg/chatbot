import difflib
import json

DATA_FILE = "chatbot_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "hello": "Hello! How can I assist you?",
            "how are you": "I'm just a computer program, but thanks for asking!",
            "what is your name": "I'm a chatbot created by OpenAI.",
            "bye": "Goodbye! Have a great day!",
        }
    return data

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_closest_match(user_input, responses):
    closest_match = difflib.get_close_matches(user_input, responses.keys(), n=1, cutoff=0.5)
    if closest_match:
        return responses[closest_match[0]]
    return None

def chatbot_response(user_input, responses):
    user_input = user_input.lower()

    if user_input in responses:
        return responses[user_input]
    else:
        closest_response = get_closest_match(user_input, responses)
        if closest_response:
            return closest_response
        else:
            return "I'm sorry, I don't understand that. Can you please ask something else?"

def main():
    responses = load_data()

    print("Chatbot: Hello! I'm a simple chatbot. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")

        # Allow the user to add new data
        if user_input.lower() == "add":
            new_question = input("Enter a new question: ").lower()
            new_response = input("Enter the response for the question: ")
            responses[new_question] = new_response
            save_data(responses)
            print("New data added successfully!")
            continue

        if user_input.lower() == "bye":
            print("Chatbot: Goodbye! Have a great day!")
            break

        response = chatbot_response(user_input, responses)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
