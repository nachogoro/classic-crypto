from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from classiccrypto.utils import frequency


def create_histogram_figure(histogram: list, title: str, y_label: str) -> Figure:
    """
    Create a matplotlib Figure object representing a bar chart of the given histogram data.

    :param list histogram: A list of (key, value) pairs representing the histogram data.
    :param str title: The title to be displayed above the histogram.
    :param str y_label: The label for the y-axis.

    :return: A matplotlib Figure object displaying the histogram.
    :rtype: Figure
    """
    letters = [k for (k,v) in histogram]
    letter_freqs = [v for (k,v) in histogram]

    figure = Figure(figsize=(4, 4), dpi=100)
    axes = figure.add_subplot()
    axes.bar(list(letters), list(letter_freqs))
    axes.set_title(title)
    axes.set_ylabel(y_label)

    return figure


def update_histogram_figure(figure: Figure, histogram: list, title: str = None, ylabel: str = None):
    """
    Update a matplotlib Figure object with new histogram data while maintaining the previous titles and labels
    if new ones are not provided.

    :param Figure figure: A matplotlib Figure object to be updated.
    :param list histogram: A list of (key, value) pairs representing the new histogram data.
    :param str title: A new title for the histogram. If None, the previous title is kept.
    :param str ylabel: A new y-axis label for the histogram. If None, the previous label is kept.
    """
    axes = figure.get_axes()[0]

    current_title = axes.title.get_text()
    current_ylabel = axes.yaxis.get_label().get_text()

    axes.clear()
    axes.bar([k for (k,v) in histogram], [v for (k,v) in histogram])

    axes.set_title(title if title else current_title)
    axes.set_ylabel(ylabel if ylabel else current_ylabel)


def display_histogram_figure_in_popup(data: list):
    """
    Display a bar chart of the provided histogram data in a pop-up window using matplotlib's pyplot.

    This function filters out keys with zero values, sorts the data, separates keys and values, and
    plots a histogram with labeled axes and a title.

    :param list data: A list of (key, value) pairs representing the histogram data.

    Returns:
        None"""

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
