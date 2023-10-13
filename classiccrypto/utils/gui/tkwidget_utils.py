import tkinter as tk
from tkinter import END


def get_text_from_widget(widget: tk.Text) -> str:
    return widget.get("1.0", END).rstrip()


def set_text_in_widget(widget: tk.Text, text: str):
    widget.delete("1.0", END)
    widget.insert("1.0", text)
