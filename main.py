
import os
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

openai_api_key = os.getenv('OPENAI_API_KEY')

def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(text + "\n")

def query_index(query):
    loader = TextLoader('data.txt')
    index = VectorstoreIndexCreator().from_loaders([loader])
    results = index.query(query, llm=ChatOpenAI(api_key=openai_api_key))
    return results

def insert_new_data_gui():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        append_to_file('data.txt', text)
        result_label.config(text="Text appended to data.txt successfully.")
        text_entry.delete("1.0", tk.END)
    else:
        result_label.config(text="Please enter some text to insert.")

def query_index_gui():
    query = text_entry.get("1.0", tk.END).strip()
    if query:
        results = query_index(query)
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, results)
        result_text.config(state=tk.DISABLED)
    else:
        result_label.config(text="Please enter a query.")

root = tk.Tk()
root.title("Langchain Text")
background_image = Image.open("l.JPG")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = tk.Frame(root, bg='light blue')
frame.pack(padx=10, pady=10)

text_entry = scrolledtext.ScrolledText(frame, height=5, bg='white', fg='black')
text_entry.pack()

insert_button = tk.Button(frame, text="Insert Data", command=insert_new_data_gui, bg='grey', fg='white')
insert_button.pack(pady=5)

query_button = tk.Button(frame, text="Query Index", command=query_index_gui, bg='grey', fg='white')
query_button.pack(pady=5)

result_label = tk.Label(frame, text="", bg='light blue', fg='black')
result_label.pack(pady=5)

result_text = scrolledtext.ScrolledText(frame, height=10, state=tk.DISABLED, bg='white', fg='black')
result_text.pack()

root.mainloop()
