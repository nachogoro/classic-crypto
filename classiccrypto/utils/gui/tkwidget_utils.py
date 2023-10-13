import tkinter as tk
from tkinter import END


def get_text_from_widget(widget: tk.Text) -> str:
    """
    Retrieve the textual content from a Tkinter Text widget.

    This function fetches all the text from a Tkinter Text widget starting
    from the first character until the end, and trims trailing whitespace.

    Args:
        widget (tk.Text): The Tkinter Text widget from which text is retrieved.

    Returns:
        str: The text retrieved from the Text widget.
    """
    return widget.get("1.0", END).rstrip()


def set_text_in_widget(widget: tk.Text, text: str):
    """
    Replace the current text in a Tkinter Text widget with new text.

    This function removes all current text in the widget and inserts
    the new specified text starting from the first character position.

    Args:
        widget (tk.Text): The Tkinter Text widget where text is set.
        text (str): The new text to set in the Text widget.

    Returns:
        None
    """
    widget.delete("1.0", END)
    widget.insert("1.0", text)
