import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from classiccrypto.utils import Language, gui
from classiccrypto.utils import frequency
from classiccrypto.utils.gui import histogram

matplotlib.use('TkAgg')


class TwoFileHistogramPlotter(tk.Tk):
    @staticmethod
    def get_histogram_base_title(filepath):
        if not filepath:
            return "<No file selected>"
        else:
            return f"Frequency of letters in {os.path.basename(filepath)}"

    def update_ui(self):
        self.similarity_value_label.config(text=f"{self.similarity_value:.4f}")
        self.slide_value_label.config(text=f"{self.slide_value}")

        new_target_title = self.get_histogram_base_title(self.target_file_entry_var.get())
        gui.histogram.update_histogram_figure(self.target_histogram_fig,
                                              histogram=self.target_histogram,
                                              title=new_target_title)

        self.target_histogram_canvas.draw()

        slided_histogram = frequency.slide_histogram(self.sliding_histogram, self.slide_value)
        new_sliding_title = self.get_histogram_base_title(self.sliding_file_entry_var.get())
        if self.sliding_file_entry_var.get() and self.slide_value != 0:
            new_sliding_title += f" (shifted by {self.slide_value})"

        gui.histogram.update_histogram_figure(self.sliding_histogram_fig,
                                              histogram=slided_histogram,
                                              title=new_sliding_title)

        self.sliding_histogram_canvas.draw()

    def on_new_file_selected(self):
        # Update the file label or entry with the selected file path
        self.target_histogram = frequency.histogram_from_file(self.target_file_entry_var.get(),
                                                              self.selected_language)

        self.sliding_histogram = frequency.histogram_from_file(self.sliding_file_entry_var.get(),
                                                               self.selected_language)
        self.similarity_value = self.compute_similarity()

        self.update_ui()

    def browse_target_file(self):
        # Open file dialog and get the file path
        filepath = filedialog.askopenfilename(title="Select a file")
        self.target_file_entry_var.set(filepath)
        self.on_new_file_selected()

    def browse_sliding_file(self):
        # Open file dialog and get the file path
        filepath = filedialog.askopenfilename(title="Select a file")
        self.sliding_file_entry_var.set(filepath)
        self.on_new_file_selected()

    def on_enter_key_pressed(self, event=None):
        self.on_new_file_selected()

    def on_select_language(self, value):
        self.selected_language = Language.from_string(value)

        self.target_histogram = frequency.histogram_from_file(
            self.target_file_entry_var.get(),
            self.selected_language)

        self.sliding_histogram = frequency.histogram_from_file(
            self.target_file_entry_var.get(),
            self.selected_language)

        self.similarity_value = self.compute_similarity()

        self.update_ui()

    def match_histograms(self):
        self.slide_value = frequency.find_step_for_best_match(self.target_histogram,
                                                              self.sliding_histogram)
        self.similarity_value = self.compute_similarity()
        self.update_ui()

    def compute_similarity(self):
        return frequency.similarity(
            self.target_histogram,
            frequency.slide_histogram(self.sliding_histogram, self.slide_value)
        )

    def __init__(self):
        super().__init__()

        self.selected_language = Language.ESP
        self.target_histogram = frequency.empty_histogram(self.selected_language)
        self.sliding_histogram = frequency.empty_histogram(self.selected_language)
        self.slide_value = 0
        self.similarity_value = self.compute_similarity()

        # UI components
        self.target_file_entry_var = None
        self.sliding_file_entry_var = None
        self.target_histogram_fig = None
        self.target_histogram_canvas = None
        self.sliding_histogram_fig = None
        self.sliding_histogram_canvas = None
        self.similarity_value_label = None
        self.slide_value_label = None

        self.title("Frequency analysis")
        self.geometry('800x800')

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=9)
        self.rowconfigure(2, weight=9)

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
        file_selector_frame = tk.Frame(self)
        file_selector_frame.grid(row=0, column=0, sticky='w')
        target_file_selector_frame = tk.Frame(file_selector_frame)
        target_file_selector_frame.grid(row=0, column=0, sticky="ew")
        target_guide_label = tk.Label(target_file_selector_frame, text="Target file:")
        target_guide_label.pack(padx=5, side='left')

        # Use a StringVar to track and display the selected filepath
        self.target_file_entry_var = tk.StringVar()
        target_file_entry = tk.Entry(target_file_selector_frame, textvariable=self.target_file_entry_var, width=50)
        target_file_entry.pack(padx=5, side='left')
        target_file_entry.bind('<Return>', self.on_enter_key_pressed)

        # Create a button to open the file dialog
        target_browse_button = tk.Button(target_file_selector_frame, text="Browse", command=self.browse_target_file)
        target_browse_button.pack(padx=5, side='left')

        sliding_file_selector_frame = tk.Frame(file_selector_frame)
        sliding_file_selector_frame.grid(row=1, column=0, sticky="ew")
        sliding_guide_label = tk.Label(sliding_file_selector_frame, text="Sliding file:")
        sliding_guide_label.pack(padx=5, side='left')

        # Use a StringVar to track and display the selected filepath
        self.sliding_file_entry_var = tk.StringVar()
        sliding_file_entry = tk.Entry(sliding_file_selector_frame, textvariable=self.sliding_file_entry_var, width=50)
        sliding_file_entry.pack(padx=5, side='left')
        sliding_file_entry.bind('<Return>', self.on_enter_key_pressed)

        # Create a button to open the file dialog
        sliding_browse_button = tk.Button(sliding_file_selector_frame, text="Browse", command=self.browse_sliding_file)
        sliding_browse_button.pack(padx=5, side='left')

        ########################
        # Place histogram
        self.target_histogram_fig = gui.histogram.create_histogram_figure(
            self.sliding_histogram,
            "<No file selected>",
            "Frequency")

        self.target_histogram_canvas = FigureCanvasTkAgg(self.target_histogram_fig, self)
        self.target_histogram_canvas.get_tk_widget().grid(row=1, column=0, sticky='nswe', padx=5, pady=5)

        self.sliding_histogram_fig = gui.histogram.create_histogram_figure(
            self.sliding_histogram,
            "<No file selected>",
            "Frequency")
        self.sliding_histogram_canvas = FigureCanvasTkAgg(self.sliding_histogram_fig, self)
        self.sliding_histogram_canvas.get_tk_widget().grid(row=2, column=0, sticky='nswe', padx=5, pady=5)

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
        self.slide_value %= len(self.sliding_histogram)
        self.similarity_value = self.compute_similarity()
        self.update_ui()

    def increment_slide_step(self):
        self.slide_value += 1
        self.slide_value %= len(self.sliding_histogram)
        self.similarity_value = self.compute_similarity()
        self.update_ui()


if __name__ == "__main__":
    app = TwoFileHistogramPlotter()
    app.wm_attributes('-zoomed', 1)
    app.mainloop()
