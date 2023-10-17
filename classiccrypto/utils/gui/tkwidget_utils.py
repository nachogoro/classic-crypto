import sys
import tkinter as tk
from tkinter import END


def _on_right_click(event, context_menu):
    """
    Displays context menu on right-click event.

    :param event: tk.Event object, contains information about the event such as the mouse pointer's x and y coordinates.
    :param context_menu: tk.Menu object, the context menu to be displayed when right-click event is triggered.
    """
    # Show context menu
    context_menu.post(event.x_root, event.y_root)


def add_context_menu(widget: tk.Text):
    """
    Adds a context menu to a Tkinter Text widget.

    :param tk.Text widget: object to add context menu to.
    """
    context_menu = tk.Menu(widget, tearoff=0)
    context_menu.add_command(label="Copy", command=lambda: widget.event_generate('<<Copy>>'))
    context_menu.add_command(label="Paste", command=lambda: widget.event_generate('<<Paste>>'))
    context_menu.add_command(label="Delete", command=lambda: widget.event_generate('<<Clear>>'))
    context_menu.add_command(label="Select All", command=lambda: widget.tag_add(tk.SEL, "1.0", tk.END))

    widget.bind("<Button-3>", lambda event: _on_right_click(event, context_menu))
    widget.bind("<Button-1>", lambda event: context_menu.unpost())
    widget.bind("<FocusOut>", lambda event: context_menu.unpost())


def get_text_from_widget(widget: tk.Text) -> str:
    """
    Retrieve the textual content from a Tkinter Text widget.

    This function fetches all the text from a Tkinter Text widget starting
    from the first character until the end, and trims trailing whitespace.

    :param tk.Text widget: The Tkinter Text widget from which text is retrieved.

    :return: The text retrieved from the Text widget.
    :rtype: str
    """
    return widget.get("1.0", END).rstrip()


def set_text_in_widget(widget: tk.Text, text: str):
    """
    Replace the current text in a Tkinter Text widget with new text.

    This function removes all current text in the widget and inserts
    the new specified text starting from the first character position.

    :param tk.Text widget: The Tkinter Text widget where text is set.
    :param str text: The new text to set in the Text widget.
    """
    widget.delete("1.0", END)
    widget.insert("1.0", text)


def maximize_window(window: tk.Tk):
    """
    Maximizes the given window
    """
    if sys.platform == "linux":
        window.wm_attributes('-zoomed', True)
    else:
        window.wm_attributes('zoomed')
