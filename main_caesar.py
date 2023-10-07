import tkinter as tk
from tkinter import ttk, END
from tkinter.filedialog import asksaveasfile

import matplotlib

import frequency_analysis
from frequency_analysis import Language

matplotlib.use('TkAgg')


def shift_list(l: list, step: int) -> list:
    result = list(l)
    for index, elem in enumerate(l):
        result[index] = l[(index + step) % len(l)]
    return result


def get_text_from_widget(widget: tk.Text) -> str:
    return widget.get("1.0", END)


def set_text_in_widget(widget: tk.Text, text: str):
    widget.delete("1.0", END)
    widget.insert("1.0", text)


class CaesarApp(tk.Tk):
    default_font = ("Helvetica", 18)

    def alphabet(self):
        return [c.upper() for c in frequency_analysis.alphabet_for_language(self.selected_language)]

    def update_ui(self):
        self.create_table(self.table_frame,
                          row1=self.alphabet(),
                          row2=shift_list(self.alphabet(), self.cipher_key))

        if self.last_action_encrypt:
            self.encrypt_text()
        else:
            self.decrypt_text()

    def save_as_file(self, text: str, default_name: str = "Untitled.txt"):
        with asksaveasfile(initialfile=default_name,
                           defaultextension=".txt",
                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]) as dst:
            dst.write(text)

    def on_select_language(self, value):
        self.selected_language = Language.from_string(value)
        self.update_ui()

    def on_enter_pressed(self, event=None):
        self.update_cipher_key()
        self.update_ui()

    def update_cipher_key(self):
        try:
            self.cipher_key = int(self.cipher_key_text.get())
        except:
            self.cipher_key = 0

    def create_table(self, parent, row1: list, row2: list):
        for widget in parent.winfo_children():
            widget.destroy()

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

    def translate(self, message: str, src_alphabet: list, dst_alphabet: list) -> str:
        result = []
        for c in message:
            capitalized = c.upper()
            try:
                translated = dst_alphabet[src_alphabet.index(capitalized)]
            except:
                translated = c
            result += (translated.upper() if c.isupper() else translated.lower())

        return ''.join(result)

    def encrypt_text(self):
        self.last_action_encrypt = True
        self.update_cipher_key()

        encryption_result = self.translate(
            get_text_from_widget(self.clear_text_widget),
            self.alphabet(),
            shift_list(self.alphabet(), self.cipher_key)
        )

        set_text_in_widget(self.cipher_text_widget, encryption_result)

    def decrypt_text(self):
        self.last_action_encrypt = False
        self.update_cipher_key()

        decryption_result = self.translate(
            get_text_from_widget(self.cipher_text_widget),
            shift_list(self.alphabet(), self.cipher_key),
            self.alphabet()
        )

        set_text_in_widget(self.clear_text_widget, decryption_result)

    def __init__(self):
        super().__init__()

        self.selected_language = Language.ESP
        self.cipher_key = 0
        self.last_action_encrypt = True

        # UI components
        self.clear_text_widget = None
        self.cipher_text_widget = None
        self.cipher_key_text = None

        self.title("Caesar cypher")
        self.geometry('800x800')

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=17)

        ########################
        # Place the language selection buttons
        lang_frame = tk.Frame(self)
        lang_frame.grid(row=0, column=2)
        lang_label = tk.Label(lang_frame, text="Clear text language: ", font=self.default_font)
        lang_label.pack(side='left')

        # Variable to hold the selected value
        lang_var = tk.StringVar(value=Language.to_string(self.selected_language))

        # Create radiobuttons
        es_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ESP), variable=lang_var,
                                  value=Language.to_string(Language.ESP),
                                  font=self.default_font,
                                  command=lambda: self.on_select_language(lang_var.get()))
        es_radio.pack(side='left')

        en_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ENG), variable=lang_var,
                                  value=Language.to_string(Language.ENG),
                                  font=self.default_font,
                                  command=lambda: self.on_select_language(lang_var.get()))
        en_radio.pack(side='left')

        # Add separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.grid(row=0, column=0, columnspan=3, sticky="swe", padx=10)

        ########################
        # Add key entry file
        key_frame = tk.Frame(self)
        key_frame.grid(row=0, column=0)
        guide_label = tk.Label(key_frame, text="Caesar key:", font=self.default_font)
        guide_label.pack(padx=5, side='left')

        # Use a StringVar to track and display the selected key
        self.cipher_key_text = tk.StringVar()
        self.cipher_key_text.set("0")
        cipher_key_entry = tk.Entry(key_frame, textvariable=self.cipher_key_text, width=3, font=self.default_font)
        cipher_key_entry.pack(padx=5, side='left')
        cipher_key_entry.bind('<Return>', self.on_enter_pressed)

        # Add table
        self.table_frame = tk.Frame(self)
        self.table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

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
        self.clear_text_widget = tk.Text(clear_text_frame, width=27, wrap=tk.WORD, font=self.default_font)
        self.clear_text_widget.grid(row=1, column=0, padx=(20, 0), sticky="nsew")

        clear_scrollbar = tk.Scrollbar(clear_text_frame, command=self.clear_text_widget.yview)
        clear_scrollbar.grid(row=1, column=1, sticky="ns")
        self.clear_text_widget.config(yscrollcommand=clear_scrollbar.set)

        # Create a 'Save' button and place it to the left of the second row
        clear_save_button = tk.Button(clear_text_frame,
                                      text="Save to file",
                                      command=lambda: self.save_as_file(get_text_from_widget(self.clear_text_widget),
                                                                        "caesar-in-clear.txt"))
        clear_save_button.grid(row=2, column=0, columnspan=2, sticky="e")

        translation_frame = tk.Frame(self)
        translation_frame.grid(row=2, column=1, sticky='nswe')

        # Buttons
        encrypt_button = tk.Button(translation_frame, text=">", command=self.encrypt_text)
        encrypt_button.grid(row=1, column=1)

        decrypt_button = tk.Button(translation_frame, text="<", command=self.decrypt_text)
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
        cipher_text_frame.grid(row=2, column=2, sticky='nsew')
        cipher_text_frame.grid_rowconfigure(0, weight=5)
        cipher_text_frame.grid_rowconfigure(1, weight=85)
        cipher_text_frame.grid_rowconfigure(2, weight=10)
        cipher_text_frame.grid_columnconfigure(0, weight=90)  # Take as much space as possible
        cipher_text_frame.grid_columnconfigure(1, weight=1)

        # Create a Text widget with a Scrollbar
        cipher_text_label = tk.Label(cipher_text_frame, text='Encrypted text')
        cipher_text_label.grid(row=0, column=0, columnspan=2)
        self.cipher_text_widget = tk.Text(cipher_text_frame, wrap=tk.WORD, width=27, font=("Helvetica", 20))
        self.cipher_text_widget.grid(row=1, column=0, sticky="nsew")

        cipher_scrollbar = tk.Scrollbar(cipher_text_frame, command=self.cipher_text_widget.yview)
        cipher_scrollbar.grid(row=1, column=1, padx=(0, 20), sticky="ns")
        self.cipher_text_widget.config(yscrollcommand=cipher_scrollbar.set)

        # Create a 'Save' button and place it to the left of the second row
        cipher_save_button = tk.Button(cipher_text_frame,
                                       text="Save to file",
                                       command=lambda: self.save_as_file(get_text_from_widget(self.cipher_text_widget),
                                                                         "caesar-encrypted.txt"))
        cipher_save_button.grid(row=2, column=0, columnspan=2, sticky="w")

        self.update_ui()


if __name__ == "__main__":
    app = CaesarApp()
    app.wm_attributes('-zoomed', 1)
    app.mainloop()