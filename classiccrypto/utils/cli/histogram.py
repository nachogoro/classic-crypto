from enum import Enum

from classiccrypto.utils import frequency


class AsciiHistogramDisplayMode(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

def display_ascii_histogram(histogram: list, display_mode: AsciiHistogramDisplayMode):
    """
    Displays an ASCII histogram in either horizontal or vertical orientation based on the specified display mode.

    Args:
        histogram (list): A list of (key, value) pairs representing the histogram data.
        display_mode (AsciiHistogramDisplayMode): An enum indicating the desired display mode, either HORIZONTAL or
        VERTICAL.

    Returns:
        None
    """

    if display_mode == AsciiHistogramDisplayMode.HORIZONTAL:
        _display_horizontal(histogram)
    else:
        _display_vertical(histogram)

def _display_horizontal(histogram: list):
    """
    Displays an ASCII histogram horizontally given a list of (key, value) pairs.

    This is a private function that prints the histogram to stdout with the keys
    displayed vertically on the left and bars extending to the right.

    Args:
        histogram (list): A list of (key, value) pairs representing the histogram data.

    Returns:
        None
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
    Displays an ASCII histogram vertically given a list of (key, value) pairs.

    This is a private function that prints the histogram to stdout with the keys
    displayed horizontally at the bottom and bars extending upwards.

    Args:
        histogram (list): A list of (key, value) pairs representing the histogram data.

    Returns:
        None
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
