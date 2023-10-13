from enum import Enum

from classiccrypto.utils import frequency


class AsciiHistogramDisplayMode(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

def display_ascii_histogram(histogram: list, display_mode: AsciiHistogramDisplayMode):
    if display_mode == AsciiHistogramDisplayMode.HORIZONTAL:
        _display_horizontal(histogram)
    else:
        _display_vertical(histogram)

def _display_horizontal(histogram: list):
    """
    Print an ASCII histogram given a list of (key, value) pairs.

    :param histogram: list of (key, value) pairs.
    """
    # Find the longest key for alignment purposes
    max_key_len = max(len(str(key)) for key, value in histogram)

    # Find the maximum value to scale the histogram
    max_value = max(value for key, value in histogram)

    # Maximum width of the histogram bar
    max_bar_width = 80

    for key, value in frequency.sort_histogram_by_key(histogram):
        # Scale the value to max_bar_width
        scaled_value = int((value / max_value) * max_bar_width)

        # Print the key and value, aligned and scaled
        print(f"{str(key).rjust(max_key_len)} | {'#' * scaled_value} ({value})")

def _display_vertical(histogram: list):
    """
    Print an ASCII vertical histogram given a list of (key, value) pairs.

    :param histogram: list of (key, value) pairs.
    """
    histogram = frequency.sort_histogram_by_key(histogram)
    # Find the longest key for alignment purposes
    max_key_len = max(len(str(key)) for key, value in histogram)

    # Find the maximum value to scale the histogram
    max_value = max(value for key, value in histogram)

    # Maximum height of the histogram bar
    max_bar_height = 30

    # Scaling the values
    scaled_values = [
        (key, int((value / max_value) * max_bar_height))
        for key, value in histogram
    ]

    # Printing the histogram
    for i in range(max_bar_height, 0, -1):
        for key, scaled_value in scaled_values:
            print("  " if scaled_value < i else "##", end=" ")
        print()

    # Printing the keys
    for key, _ in scaled_values:
        print(f"{str(key).ljust(max_key_len)}", end=" ")
    print()
