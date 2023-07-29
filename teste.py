import difflib
import json
import sqlite3
import tkinter as tk
from tkinter import scrolledtext

DATABASE_FILE = "chatbot_database.db"
DATA_FILE = "chatbot_data.json"

def create_database():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       sender TEXT NOT NULL,
                       content TEXT NOT NULL)''')
    connection.commit()
    connection.close()

def insert_message(sender, content):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (sender, content) VALUES (?, ?)", (sender, content))
    connection.commit()
    connection.close()



def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


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
            return "Desculpe, não entendi. Pode reformular a pergunta?"



def send_message(event=None):
    user_input = user_entry.get()
    if user_input.strip():
        insert_message("Usuário", user_input)  # Inserir mensagem do usuário no banco de dados
        response = chatbot_response(user_input, responses)  # Pass the responses dictionary here
        insert_message("Chatbot", response)  # Inserir resposta do chatbot no banco de dados

        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "Você: " + user_input + "\n")
        chatbox.insert(tk.END, "Chatbot: " + response + "\n")
        chatbox.config(state=tk.DISABLED)
        user_entry.delete(0, tk.END)

def clear_chat():
    chatbox.config(state=tk.NORMAL)
    chatbox.delete(1.0, tk.END)
    chatbox.config(state=tk.DISABLED)

def main():
    create_database()
    global responses, chatbox, user_entry  # Declare global variables
    responses = load_data()

    root = tk.Tk()
    root.title("Bot Interface")

    chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    chatbox.config(state=tk.DISABLED)
    chatbox.pack()

    user_entry = tk.Entry(root, width=50)
    user_entry.pack()
    user_entry.focus_set()

    # Call the send_message function when the Return key is pressed
    user_entry.bind("<Return>", send_message)

    clear_button = tk.Button(root, text="Limpar Chat", command=clear_chat)
    send_button = tk.Button(root, text="Enviar", command=send_message)

    clear_button.pack(side=tk.LEFT, padx=100)
    send_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()