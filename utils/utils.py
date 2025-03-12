import tkinter as tk


def write_to_text_widget(widget, message):
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, message)
    widget.config(state=tk.DISABLED)
    widget.see(tk.END)
