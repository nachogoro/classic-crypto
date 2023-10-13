from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from classiccrypto.utils import frequency


def create_histogram_figure(histogram: list, title: str, y_label: str) -> Figure:
    letters = [k for (k,v) in histogram]
    frequency = [v for (k,v) in histogram]

    figure = Figure(figsize=(4, 4), dpi=100)
    axes = figure.add_subplot()
    axes.bar(list(letters), list(frequency))
    axes.set_title(title)
    axes.set_ylabel(y_label)

    return figure


def update_histogram_figure(figure: Figure, histogram: list, title: str = None, ylabel: str = None):
    axes = figure.get_axes()[0]

    current_title = axes.title.get_text()
    current_ylabel = axes.yaxis.get_label().get_text()

    axes.clear()
    axes.bar([k for (k,v) in histogram], [v for (k,v) in histogram])

    axes.set_title(title if title else current_title)
    axes.set_ylabel(ylabel if ylabel else current_ylabel)


def display_histogram_figure_in_popup(data: list):
    # Filter out keys with zero values and then sort
    sorted_data = frequency.sort_histogram_by_key([(k, v) for k, v in data if v > 0])

    # Separate the keys and values
    keys = [item[0] for item in sorted_data]
    values = [item[1] for item in sorted_data]

    # Plot the histogram
    plt.bar(keys, values)

    # Set x-ticks to be only for keys with non-zero values
    plt.xticks(keys)

    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Possible keys')
    plt.show(block=False)
