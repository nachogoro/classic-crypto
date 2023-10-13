import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import matplotlib

from classiccrypto.utils import Language, gui
from classiccrypto.utils import frequency
from classiccrypto.utils.gui import histogram

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FileAndLanguageHistogramPlotter(tk.Tk):
    def language_histogram(self):
        return frequency.language_histogram(self.selected_language)

    def update_ui(self):
        self.similarity_value_label.config(text=f"{self.similarity_value:.4f}")
        self.slide_value_label.config(text=f"{self.slide_value}")

        gui.histogram.update_histogram_figure(self.language_histogram_fig,
                                              self.language_histogram())

        self.language_histogram_canvas.draw()

        slided_text_histogram = frequency.slide_histogram(self.file_histogram, self.slide_value)
        if not self.file_entry_var.get():
            new_title = "<No file selected>"
        else:
            new_title = f"Frequency of letters in {os.path.basename(self.file_entry_var.get())}"

            if self.slide_value != 0:
                new_title += f" (shifted by {self.slide_value})"

        gui.histogram.update_histogram_figure(self.file_histogram_fig,
                                              histogram=slided_text_histogram,
                                              title=new_title)

        self.file_histogram_canvas.draw()

    def on_new_file_selected(self):
        # Update the file label or entry with the selected file path
        self.file_histogram = frequency.histogram_from_file(self.file_entry_var.get(),
                                                            self.selected_language)
        self.similarity_value = self.compute_similarity()

        self.update_ui()

    def browse_file(self):
        # Open file dialog and get the file path
        filepath = filedialog.askopenfilename(title="Select a file")
        self.file_entry_var.set(filepath)
        self.on_new_file_selected()

    def on_enter_key_pressed(self, event=None):
        self.on_new_file_selected()

    def on_select_language(self, value):
        self.selected_language = Language.from_string(value)

        self.file_histogram = frequency.histogram_from_file(
            self.file_entry_var.get(),
            self.selected_language)

        self.similarity_value = self.compute_similarity()

        self.update_ui()

    def match_histograms(self):
        self.slide_value = frequency.find_step_for_best_match(self.language_histogram(),
                                                              self.file_histogram)
        self.similarity_value = self.compute_similarity()
        self.update_ui()

    def compute_similarity(self):
        return frequency.similarity(
            self.language_histogram(),
            frequency.slide_histogram(self.file_histogram, self.slide_value)
        )

    def __init__(self):
        super().__init__()

        self.selected_language = Language.ESP
        self.file_histogram = frequency.empty_histogram(self.selected_language)
        self.slide_value = 0
        self.similarity_value = self.compute_similarity()

        # UI components
        self.file_entry_var = None
        self.language_histogram_fig = None
        self.language_histogram_canvas = None
        self.file_histogram_fig = None
        self.file_histogram_canvas = None
        self.similarity_value_label = None
        self.slide_value_label = None

        self.title("Frequency analysis")
        self.geometry('800x800')

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=10)

        ########################
        # Place the language selection buttons
        lang_frame = tk.Frame(self)
        lang_frame.grid(row=0, column=1, pady=20, padx=20)
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
        en_radio.grid(row=0, column=2)

        # Add separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.grid(row=0, column=0, columnspan=2, sticky="swe", padx=10, pady=5)

        ########################
        # Add file browser
        file_frame = tk.Frame(self)
        file_frame.grid(row=0, column=0)
        guide_label = tk.Label(file_frame, text="Selected File:")
        guide_label.pack(padx=5, side='left')

        # Use a StringVar to track and display the selected filepath
        self.file_entry_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.file_entry_var, width=50)
        file_entry.pack(padx=5, side='left')
        file_entry.bind('<Return>', self.on_enter_key_pressed)

        # Create a button to open the file dialog
        browse_button = tk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(padx=5, side='left')

        ########################
        # Place histogram
        self.language_histogram_fig = gui.histogram.create_histogram_figure(
            self.language_histogram(),
            "Frequency of letters language-wide",
            "Frequency")

        self.language_histogram_canvas = FigureCanvasTkAgg(self.language_histogram_fig, self)
        self.language_histogram_canvas.get_tk_widget().grid(row=1, column=0, sticky='nswe', padx=5, pady=5)

        self.file_histogram_fig = gui.histogram.create_histogram_figure(
            self.file_histogram,
            "<No file selected>",
            "Frequency")
        self.file_histogram_canvas = FigureCanvasTkAgg(self.file_histogram_fig, self)
        self.file_histogram_canvas.get_tk_widget().grid(row=2, column=0, sticky='nswe', padx=5, pady=5)

        ########################
        # Place similarity and slide buttons
        similarity_frame = tk.Frame(self, padx=10, pady=10)
        similarity_frame.grid(row=1, column=1, rowspan=2)

        similarity_label = tk.Label(similarity_frame, text="Similarity: ")
        similarity_label.grid(row=0, column=0)
        self.similarity_value_label = tk.Label(similarity_frame, text="0.05")
        self.similarity_value_label.grid(row=0, column=1)

        optimize_button = tk.Button(similarity_frame, text="Best match", command=self.match_histograms)
        optimize_button.grid(row=1, column=0, columnspan=2)

        sliding_frame = tk.Frame(similarity_frame)
        sliding_frame.grid(row=2, column=0, columnspan=2)
        slide_left_button = tk.Button(sliding_frame, text="<", command=self.decrement_slide_step)
        slide_left_button.grid(row=2, column=0)
        self.slide_value_label = tk.Label(sliding_frame, text="0")
        self.slide_value_label.grid(row=2, column=1)
        slide_right_button = tk.Button(sliding_frame, text=">", command=self.increment_slide_step)
        slide_right_button.grid(row=2, column=2)

        self.update_ui()

    def decrement_slide_step(self):
        self.slide_value -= 1
        self.slide_value %= len(self.file_histogram)
        self.similarity_value = self.compute_similarity()
        self.update_ui()

    def increment_slide_step(self):
        self.slide_value += 1
        self.slide_value %= len(self.file_histogram)
        self.similarity_value = self.compute_similarity()
        self.update_ui()


if __name__ == "__main__":
    app = FileAndLanguageHistogramPlotter()
    app.wm_attributes('-zoomed', 1)
    app.mainloop()
