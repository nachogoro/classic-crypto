import tkinter as tk
from tkinter import ttk

import matplotlib

import frequency_analysis
from frequency_analysis import Language

matplotlib.use('TkAgg')


class CaesarApp(tk.Tk):
    def alphabet(self):
        return [c.upper() for c in frequency_analysis.alphabet_for_language(self.selected_language)]
    def update_ui(self):
        pass

    def browse_file(self):
        pass

    def on_select_language(self, value):
        pass

    def on_enter_key_pressed(self, event):
        pass

    def create_table(self, parent, row1: list, row2: list):
        for r in range(2):
            for c in range(len(row1)):
                text = row1[c] if r == 0 else row2[c]
                label = tk.Label(parent, text=text, font=('Courier', 26), relief="solid", padx=5, pady=5)
                label.grid(row=r, column=c, sticky="nsew")

        # Set column and row weights so they behave nicely when resizing
        for c in range(len(row1)):
            parent.grid_columnconfigure(c, weight=1)
        for r in range(2):
            parent.grid_rowconfigure(r, weight=1)

    def __init__(self):
        super().__init__()

        self.selected_language = Language.ESP
        self.cipher_key = 0

        # UI components
        self.clear_text_widget = None
        self.encrypted_text_widget = None

        self.title("Caesar cypher")
        self.geometry('800x800')

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=17)

        ########################
        # Place the language selection buttons
        lang_frame = tk.Frame(self)
        lang_frame.grid(row=0, column=2)
        lang_label = tk.Label(lang_frame, text="Clear text language: ")
        lang_label.grid(row=0, column=0)

        # Variable to hold the selected value
        lang_var = tk.StringVar(value=Language.to_string(self.selected_language))

        # Create radiobuttons
        es_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ESP), variable=lang_var,
                                  value=Language.to_string(Language.ESP),
                                  command=lambda: self.on_select_language(lang_var.get()))
        es_radio.grid(row=0, column=1)

        en_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ENG), variable=lang_var,
                                  value=Language.to_string(Language.ENG),
                                  command=lambda: self.on_select_language(lang_var.get()))
        en_radio.grid(row=0, column=2, padx=(0, 10))

        # Add separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.grid(row=0, column=0, columnspan=3, sticky="swe", padx=10)

        ########################
        # Add key entry file
        key_frame = tk.Frame(self)
        key_frame.grid(row=0, column=0)
        guide_label = tk.Label(key_frame, text="Caesar key:")
        guide_label.pack(padx=5, side='left')

        # Use a StringVar to track and display the selected key
        self.cipher_key = tk.StringVar()
        cipher_entry = tk.Entry(key_frame, textvariable=self.cipher_key, width=3)
        cipher_entry.pack(padx=5, side='left')
        cipher_entry.bind('<Return>', self.on_enter_key_pressed)

        # Add table
        table_frame = tk.Frame(self)
        table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.create_table(table_frame,
                          row1=self.alphabet(),
                          row2=self.alphabet())

        # Add text widgets
        text_input_frame = tk.Frame(self, bg='red')
        text_input_frame.grid(row=2, column=0, sticky='nswe')
        text_input_frame.rowconfigure(0, weight=4)
        text_input_frame.rowconfigure(1, weight=1)
        
        clear_text_scroll_bar = tk.Scrollbar(text_input_frame)
        cipher_text_scroll_bar = tk.Scrollbar(text_input_frame)


if __name__ == "__main__":
    app = CaesarApp()
    app.wm_attributes('-zoomed', 1)
    app.mainloop()
