import tkinter as tk
from tkinter import scrolledtext
import time

def normalize_text(text):
    # Normalizing text to czech special letters
    text = text.lower()
    text = text.replace("á", "a").replace("č", "c").replace("ď", "d").replace("é", "e").replace("ě", "e")
    text = text.replace("í", "i").replace("ň", "n").replace("ó", "o").replace("ř", "r").replace("š", "s")
    text = text.replace("ť", "t").replace("ú", "u").replace("ů", "u").replace("ý", "y").replace("ž", "z")
    return text

def encode(text, key):
    text = text.replace(" ", " ").lower()
    key = key.lower()

    encoded_text = ""
    key_index = 0
    steps = []

    for char in text:
        if char.isalpha():
            char_ord = ord(char) - ord('a')
            shift = ord(key[key_index]) - ord('a')
            encoded_char_ord = (char_ord + shift) % 26
            encoded_char = chr(encoded_char_ord + ord('a'))
            steps.append(f"Encode: '{char}' : ({char_ord} + {shift} (move to '{key[key_index]}')) %26 = {encoded_char_ord} -> '{encoded_char}'")
            encoded_text += encoded_char
            key_index = (key_index + 1) % len(key)
        else:
            encoded_text += char
            steps.append(f"'{char}' - Not encoded")

    return encoded_text, steps

def decode(encoded_text, key):
    key = key.lower()
    decoded_text = ""
    key_index = 0
    steps = []

    for char in encoded_text:
        if char.isalpha():
            char_ord = ord(char) - ord('a')
            shift = ord(key[key_index]) - ord('a')
            decoded_char_ord = (char_ord - shift + 26) % 26
            decoded_char = chr(decoded_char_ord + ord('a'))
            steps.append(f"Decode: '{char}' : ({char_ord} + {shift} (move to '{key[key_index]}')) %26 = {decoded_char_ord} -> '{decoded_char}'")
            decoded_text += decoded_char
            key_index = (key_index + 1) % len(key)
        else:
            decoded_text += char
            steps.append(f"'{char}' - Not decoded")

    return decoded_text, steps

def process(action):
    start_time = time.time()
    text = text_entry.get("1.0", "end-1c")
    key = key_entry.get()

    text = normalize_text(text)
    key = normalize_text(key)

    steps_display.config(state=tk.NORMAL)
    steps_display.delete("1.0", tk.END)

    if action == "encode":
        result, steps = encode(text, key)
    else:
        result, steps = decode(text, key)

    result_display.config(state=tk.NORMAL)
    result_display.delete("1.0", tk.END)
    result_display.insert(tk.INSERT, result)
    result_display.config(state=tk.DISABLED)

    for step in steps:
        steps_display.insert(tk.INSERT, step + "\n")
    steps_display.config(state=tk.DISABLED)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_display.config(text=f"Time elapsed: {elapsed_time:.4f} seconds")

    #GUI
    window = tk.Tk()
    window.title("Viegenere cypher")
    window.geometry("1000x800")

    text_label = tk.Label(window, text="Entry your text: ")
    text_label.pack()
    text_entry = scrolledtext.ScrolledText(window, height=10, wrap=tk.WORD)
    text_entry.pack()
    key_label = tk.Label(window, text="Entry your key: ")
    key_label.pack()
    key_entry = tk.Entry(window)
    key_entry.pack()

    encode_button = tk.Button(window, text="Encode", command=lambda: process('encode'))
    encode_button.pack()
    decode_button = tk.Button(window, text="Decode", command=lambda: process('decode'))
    decode_button.pack()

    result_display = scrolledtext.ScrolledText(window, height=10, state=tk.DISABLED, wrap=tk.WORD)
    result_display.pack()

    steps_label = tk.Label(window, text="Steps of encode/decode: ")
    steps_label.pack()
    steps_display = scrolledtext.ScrolledText(window, height=10, state=tk.DISABLED, wrap=tk.WORD)
    steps_display.pack()

    elapsed_time_display = tk.Label(window, text="")
    elapsed_time_display.pack()

    window.mainloop()
