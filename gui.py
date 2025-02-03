import json
import tkinter as tk
from tkinter import ttk


def find_characters_by_rhyme(un_bu):
    for entry in un_ceh_data['韻母']:
        if entry['韻'] == un_bu:
            return entry['字']
    return []


def on_input_change(event):
    input_text = entry.get()
    characters = find_characters_by_rhyme(input_text)
    character_list.delete(0, tk.END)
    for char in characters:
        character_list.insert(tk.END, char)

# 加載韻書數據
with open('韻書.json', 'r', encoding='utf-8') as f:
    un_ceh_data = json.load(f)


root = tk.Tk()
root.title("閩南話輸入法")

entry = ttk.Entry(root, width=20)
entry.bind('<KeyRelease>', on_input_change)
entry.pack(pady=10)

character_list = tk.Listbox(root, width=20, height=10)
character_list.pack(pady=10)

root.mainloop()