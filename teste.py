import difflib
import sqlite3
import tkinter as tk
import json
from tkinter import scrolledtext, messagebox
from tkinter import simpledialog

# Define o arquivo do banco de dados SQLite
DATABASE_FILE = "chatbot_db.sqlite"
dados_json = "chatbot_data.json"


def criar_tabela():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perguntas_respostas (
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def load_data():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT pergunta, resposta FROM perguntas_respostas")
        data = {pergunta: resposta for pergunta, resposta in cursor.fetchall()}
        conn.close()
    except (sqlite3.Error, FileNotFoundError):
        data = {}

    return data


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
        response = chatbot_response(user_input, responses)
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "Você: " + user_input + "\n", "user")
        chatbox.insert(tk.END, "Chatbot: " + response + "\n", "bot")
        chatbox.insert(tk.END, "-" * 50 + "\n", "separator")  # Add a separator line
        chatbox.config(state=tk.DISABLED)
        user_entry.delete(0, tk.END)


def clear_chat():
    chatbox.config(state=tk.NORMAL)
    chatbox.delete(1.0, tk.END)
    chatbox.config(state=tk.DISABLED)


def inserir_dados(pergunta, resposta):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (?, ?)", (pergunta, resposta))
    conn.commit()
    conn.close()


def inserir_dados_interface():
    pergunta = simpledialog.askstring("Inserir Pergunta", "Digite a pergunta:")
    if pergunta:
        resposta = simpledialog.askstring("Inserir Resposta", "Digite a resposta:")
        if resposta:
            inserir_dados(pergunta, resposta)
            tk.messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")


def inserir_json_dados(arquivo_json):
    with open(arquivo_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    for pergunta, resposta in data.items():
        inserir_dados(pergunta, resposta)


def main():
    criar_tabela()
    # inserir_json_dados(dados_json) # inserir dados a partir do json
    global responses, chatbox, user_entry  # Declare global variables
    responses = load_data()

    root = tk.Tk()
    root.title("Bot Interface")

    chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    chatbox.config(state=tk.DISABLED)
    chatbox.pack()
    chatbox.tag_configure("user", foreground="blue", )
    chatbox.tag_configure("bot", foreground="red")
    chatbox.tag_configure("separator", foreground="gray")

    user_entry = tk.Entry(root, width=50)
    user_entry.pack(pady=10)
    user_entry.focus_set()

    # Call the send_message function when the Return key is pressed
    user_entry.bind("<Return>", send_message)

    clear_button = tk.Button(root, text="Limpar Chat", command=clear_chat)
    send_button = tk.Button(root, text="Enviar", command=send_message)

    clear_button.pack(side=tk.LEFT, padx=10, pady=10)
    send_button.pack(side=tk.LEFT, padx=100, pady=10)

    # Botão para inserir dados
    insert_button = tk.Button(root, text="Inserir Dados", command=inserir_dados_interface)
    insert_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
