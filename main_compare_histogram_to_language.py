import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import matplotlib
import frequency_analysis
from frequency_analysis import Language

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HistogramPlotter(tk.Tk):
    def update_ui(self):
        self.similarity_value_label.config(text=f"{self.similarity_value:.4f}")
        self.slide_value_label.config(text=f"{self.slide_value}")

        language_histogram = frequency_analysis.frequency_per_language(self.selected_language)

        axes = self.language_histogram_fig.get_axes()[0]
        axes.clear()
        axes.bar(list(language_histogram.keys()), list(language_histogram.values()))
        axes.set_title('Frequency of letters language-wide')
        axes.set_ylabel('Frequency')

        self.language_histogram_canvas.draw()

        slided_text_histogram = frequency_analysis.slide_histogram(self.file_histogram, self.slide_value)
        axes = self.text_histogram_fig.get_axes()[0]
        axes.clear()
        axes.bar(list(slided_text_histogram.keys()), list(slided_text_histogram.values()))
        axes.set_title('Frequency of letters in text')
        axes.set_ylabel('Frequency')

        self.text_figure_canvas.draw()

    def histogram_from_file(self, filepath: str, lang: Language) -> dict:
        try:
            if filepath:
                with open(filepath, 'r') as file:
                    return frequency_analysis.normalized_histogram(file.read(), lang)
        except:
            pass

        return frequency_analysis.empty_histogram(lang)

    def browse_file(self):
        # Open file dialog and get the file path
        filepath = filedialog.askopenfilename(title="Select a file")

        # Update the file label or entry with the selected file path
        self.file_entry_var.set(filepath)
        self.file_histogram = self.histogram_from_file(filepath, self.selected_language)
        self.similarity_value = frequency_analysis.similarity(self.file_histogram,
                                                              frequency_analysis.frequency_per_language(
                                                                  self.selected_language))

        self.update_ui()

    def on_enter_key_pressed(self, event=None):
        # Update the file label or entry with the selected file path
        self.file_histogram = self.histogram_from_file(self.file_entry_var.get(), self.selected_language)
        self.similarity_value = frequency_analysis.similarity(self.file_histogram,
                                                              frequency_analysis.frequency_per_language(
                                                                  self.selected_language))
        self.update_ui()

    def on_select_language(self, value):
        print(f"Selected Language: {value}")

        self.selected_language = Language.from_string(value)
        self.file_histogram = self.histogram_from_file(self.file_entry_var.get(), self.selected_language)
        self.similarity_value = frequency_analysis.similarity(self.file_histogram,
                                                              frequency_analysis.frequency_per_language(self.selected_language))

        self.update_ui()

    def create_histogram_figure(self, histogram: dict):
        letters = histogram.keys()
        frequency = histogram.values()

        figure = Figure(figsize=(4, 4), dpi=100)
        axes = figure.add_subplot()
        axes.bar(list(letters), list(frequency))
        axes.set_title('Frequency of letters language-wide')
        axes.set_ylabel('Frequency')

        return figure


    def match_histograms(self):
        language_histogram = frequency_analysis.frequency_per_language(self.selected_language)
        best_similarity = frequency_analysis.similarity(self.file_histogram, language_histogram)
        step_for_best_fit = 0

        for step in range(1, len(language_histogram.keys())):
            slid_histogram = frequency_analysis.slide_histogram(self.file_histogram, step)
            candidate_similarity = frequency_analysis.similarity(slid_histogram, language_histogram)

            if candidate_similarity > best_similarity:
                best_similarity = candidate_similarity
                step_for_best_fit = step

        self.similarity_value = best_similarity
        self.slide_value = step_for_best_fit

        self.update_ui()


    def __init__(self):
        super().__init__()

        self.selected_language = Language.ESP
        self.file_histogram = frequency_analysis.empty_histogram(self.selected_language)
        self.slide_value = 0
        self.similarity_value = frequency_analysis.similarity(self.file_histogram,
                                                              frequency_analysis.frequency_per_language(self.selected_language))

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
        lang_var = tk.StringVar(value=Language.to_string(Language.ESP))  # Default selection is "ES"

        # Create radiobuttons
        es_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ESP), variable=lang_var, value=Language.to_string(Language.ESP),
                                  command=lambda: self.on_select_language(lang_var.get()))
        es_radio.grid(row=0, column=1)

        en_radio = tk.Radiobutton(lang_frame, text=Language.to_string(Language.ENG), variable=lang_var, value=Language.to_string(Language.ENG),
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
        self.language_histogram_fig = self.create_histogram_figure(frequency_analysis.frequency_per_language(self.selected_language))
        self.language_histogram_canvas = FigureCanvasTkAgg(self.language_histogram_fig, self)
        self.language_histogram_canvas.get_tk_widget().grid(row=1, column=0, sticky='nswe', padx=5, pady=5)

        self.text_histogram_fig = self.create_histogram_figure(self.file_histogram)
        self.text_figure_canvas = FigureCanvasTkAgg(self.text_histogram_fig, self)
        self.text_figure_canvas.get_tk_widget().grid(row=2, column=0, sticky='nswe', padx=5, pady=5)

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
        self.slide_value_label .grid(row=2, column=1)
        slide_right_button = tk.Button(sliding_frame, text=">", command=self.increment_slide_step)
        slide_right_button.grid(row=2, column=2)

        self.update_ui()


    def decrement_slide_step(self):
        self.slide_value -= 1
        self.slide_value %= len(self.file_histogram.keys())
        self.similarity_value = frequency_analysis.similarity(frequency_analysis.frequency_per_language(self.selected_language),
                                                              frequency_analysis.slide_histogram(self.file_histogram, self.slide_value))
        self.update_ui()

    def increment_slide_step(self):
        self.slide_value += 1
        self.slide_value %= len(self.file_histogram.keys())
        self.similarity_value = frequency_analysis.similarity(
            frequency_analysis.frequency_per_language(self.selected_language),
            frequency_analysis.slide_histogram(self.file_histogram, self.slide_value))
        self.update_ui()


if __name__ == "__main__":
    app = HistogramPlotter()
    app.mainloop()
