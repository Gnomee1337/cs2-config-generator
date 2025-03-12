import tkinter as tk


def write_to_text_widget(widget, message):
    widget.insert(tk.END, message)
    widget.see(tk.END)
