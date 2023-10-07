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
        self.columnconfigure(2, weight=5) # For some reason, if I use weight=5 it isn't as wide as column 1
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=17)

        ########################
        # Place the language selection buttons
        lang_frame = tk.Frame(self)
        lang_frame.grid(row=0, column=2)
        lang_label = tk.Label(lang_frame, text="Clear text language: ")
        lang_label.pack(side='left')

        # Variable to hold the selected value
        lang_var = tk.StringVar(value=Language.to_string(self.selected_language))

        # Create radiobuttons
        es_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ESP), variable=lang_var,
                                  value=Language.to_string(Language.ESP),
                                  command=lambda: self.on_select_language(lang_var.get()))
        es_radio.pack(side='left')

        en_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ENG), variable=lang_var,
                                  value=Language.to_string(Language.ENG),
                                  command=lambda: self.on_select_language(lang_var.get()))
        en_radio.pack(side='left')

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

        clear_text_frame = tk.Frame(self)
        clear_text_frame.grid(row=2, column=0, sticky='nsew')
        clear_text_frame.grid_rowconfigure(0, weight=5)
        clear_text_frame.grid_rowconfigure(1, weight=85)
        clear_text_frame.grid_rowconfigure(2, weight=10)
        clear_text_frame.grid_columnconfigure(0, weight=90)  # Take as much space as possible
        clear_text_frame.grid_columnconfigure(1, weight=1)

        # Create a Text widget with a Scrollbar
        clear_text_label = tk.Label(clear_text_frame, text='Clear text')
        clear_text_label.grid(row=0, column=0, columnspan=2)
        clear_text = tk.Text(clear_text_frame, wrap=tk.WORD)
        clear_text.grid(row=1, column=0, padx=(20, 0), sticky="nsew")

        clear_scrollbar = tk.Scrollbar(clear_text_frame, command=clear_text.yview)
        clear_scrollbar.grid(row=1, column=1, sticky="ns")
        clear_text.config(yscrollcommand=clear_scrollbar.set)

        # Create a 'Save' button and place it to the left of the second row
        clear_save_button = tk.Button(clear_text_frame, text="Save to file")
        clear_save_button.grid(row=2, column=0, columnspan=2, sticky="w")

        translation_frame = tk.Frame(self)
        translation_frame.grid(row=2, column=1, sticky='nswe')

        # Buttons
        encrypt_button = tk.Button(translation_frame, text=">")
        encrypt_button.grid(row=1, column=1)

        decrypt_button = tk.Button(translation_frame, text="<")
        decrypt_button.grid(row=2, column=1)

        # Configure translation_frame rows and columns for centering
        translation_frame.grid_rowconfigure(0, weight=1)  # Top padding
        translation_frame.grid_rowconfigure(1, weight=0)  # Buttons (no extra space)
        translation_frame.grid_rowconfigure(2, weight=0)  # Buttons (no extra space)
        translation_frame.grid_rowconfigure(3, weight=1)  # Bottom padding

        translation_frame.grid_columnconfigure(0, weight=1)  # Left padding
        translation_frame.grid_columnconfigure(1, weight=0)  # Buttons (no extra space)
        translation_frame.grid_columnconfigure(2, weight=1)  # Right padding

        cipher_text_frame = tk.Frame(self)
        cipher_text_frame.grid(row=2, column=2, sticky='nswe')

        cipher_text_frame = tk.Frame(self)
        cipher_text_frame.grid(row=2, column=2, sticky='nsew')
        cipher_text_frame.grid_rowconfigure(0, weight=5)
        cipher_text_frame.grid_rowconfigure(1, weight=85)
        cipher_text_frame.grid_rowconfigure(2, weight=10)
        cipher_text_frame.grid_columnconfigure(0, weight=90)  # Take as much space as possible
        cipher_text_frame.grid_columnconfigure(1, weight=1)

        # Create a Text widget with a Scrollbar
        cipher_text_label = tk.Label(cipher_text_frame, text='Encrypted text')
        cipher_text_label.grid(row=0, column=0, columnspan=2)
        cipher_text = tk.Text(cipher_text_frame, wrap=tk.WORD)
        cipher_text.grid(row=1, column=0, sticky="nsew")

        cipher_scrollbar = tk.Scrollbar(cipher_text_frame, command=cipher_text.yview)
        cipher_scrollbar.grid(row=1, column=1, padx=(0, 20), sticky="ns")
        cipher_text.config(yscrollcommand=cipher_scrollbar.set)

        # Create a 'Save' button and place it to the left of the second row
        cipher_save_button = tk.Button(cipher_text_frame, text="Save to file")
        cipher_save_button.grid(row=2, column=0, columnspan=2, sticky="w")


if __name__ == "__main__":
    app = CaesarApp()
    app.wm_attributes('-zoomed', 1)
    app.mainloop()
