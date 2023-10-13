import math
from collections import defaultdict

import classiccrypto.utils.frequency
from classiccrypto.cryptoschemes.vigenere import VigenereKey
from classiccrypto.utils import alphabets, Language, LetterCase
from classiccrypto.utils import cli
from classiccrypto.utils import gui
from classiccrypto.utils.cli import histogram
from classiccrypto.utils.gui import histogram


def _get_divisors(n):
    """
    Retrieve all divisors of a given integer.

    Utilizes memoization to store previously calculated divisors for efficiency.

    Args:
        n (int): The integer to find divisors for.

    Returns:
        list[int]: A list containing all divisors of `n`.
    """
    if not hasattr(_get_divisors, 'divisors'):
        _get_divisors.divisors = dict()

    if n not in _get_divisors.divisors:
        divs = set()

        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divs.add(i)
                divs.add(n // i)

        _get_divisors.divisors[n] = list(divs)

    return _get_divisors.divisors[n]


def get_separation_of_3_and_4_letter_blocks(msg: str) -> dict:
    """
    Determine the separations between all 3 and 4-letter blocks within a message.

    Args:
        msg (str): The message to analyze.

    Returns:
        dict: A dictionary containing blocks as keys and lists of their respective
              separations as values.

    Raises:
        RuntimeError: If the message is too short to analyze.
    """
    if len(msg) < 8:
        raise RuntimeError("Cannot analyse message, too short")

    latest_position = dict()
    result = defaultdict(list)

    for i in range(len(msg) - 3):
        trigram = msg[i:i + 3]
        quadrigram = msg[i:i + 4]

        if trigram not in latest_position:
            latest_position[trigram] = i

        if quadrigram not in latest_position:
            latest_position[quadrigram] = i

        trigram_distance = i - latest_position[trigram]
        quadrigram_distance = i - latest_position[quadrigram]

        if trigram_distance != 0:
            result[trigram].append(trigram_distance)
        if quadrigram_distance != 0:
            result[quadrigram].append(quadrigram_distance)

    return result


def crack(ciphertext: str, lang: Language, no_gui=False, fast=False) -> VigenereKey:
    """
    Attempt to crack a ciphertext encrypted with the Vigenere cipher using statistical analysis.

    The function can leverage both a GUI-based histogram display and a CLI variant based on the
    `no_gui` parameter. The process is made up of estimating the key length, analyzing the 
    distances between recurring trigrams and quadrigrams, and evaluating Caesar cipher on every
    nth letter, according to the guessed key length.

    Args:
        ciphertext (str): The encrypted message.
        lang (Language): The language object to be used for decryption.
        no_gui (bool, optional): If True, utilize CLI for displaying histograms instead of GUI.
                                 Defaults to False.
        fast (bool, optional): If True, utilize fast cracking methods. Defaults to False.

    Returns:
        VigenereKey: The most likely key to have been used for the encryption.
    """
    # Find separation for all 3 and 4 letter sequences
    distance_between_occurrences = get_separation_of_3_and_4_letter_blocks(ciphertext)
    divisor_frequency = defaultdict(int)
    processed_distances = 0

    for _, distance_list in distance_between_occurrences.items():
        for distance in distance_list:
            processed_distances += 1
            for divisor in _get_divisors(distance):
                divisor_frequency[divisor] += 1

    print('Here are the top 20 candidates for key length')

    def top_items(d, n=20):
        return sorted(d.items(),
                      key=lambda item: item[1],
                      reverse=True)[:n]

    if no_gui:
        histogram_orientation = cli.histogram.AsciiHistogramDisplayMode.VERTICAL
        cli.histogram.display_ascii_histogram(top_items(divisor_frequency), histogram_orientation)
    else:
        gui.histogram.display_histogram_figure_in_popup(top_items(divisor_frequency))

    while True:
        try:
            key_length = int(input("Selected key length: "))
            break
        except ValueError:
            print("Invalid key.")

    guessed_key = []

    for i in range(key_length):
        every_nth_letter = ciphertext[i::key_length]
        caesar_key = classiccrypto.cryptoschemes.cracking.caesar.crack(every_nth_letter, lang, fast)
        guessed_key.append(alphabets.alphabet(lang, LetterCase.UPPER)[caesar_key.key])

    return VigenereKey(''.join(guessed_key), lang)
