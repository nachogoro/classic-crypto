import math
from collections import defaultdict

import classiccrypto.utils.frequency
from classiccrypto.cryptoschemes.vigenere import VigenereKey
from classiccrypto.utils import alphabets, Language, LetterCase
from classiccrypto.utils import cli
from classiccrypto.utils import gui
from classiccrypto.utils.cli import histogram
from classiccrypto.utils.gui import histogram


def get_divisors(n):
    if not hasattr(get_divisors, 'divisors'):
        get_divisors.divisors = dict()

    if n not in get_divisors.divisors:
        divs = set()

        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divs.add(i)
                divs.add(n // i)

        get_divisors.divisors[n] = list(divs)

    return get_divisors.divisors[n]


def get_separation_of_3_and_4_letter_blocks(msg: str) -> dict:
    if len(msg) < 8:
        raise RuntimeError("Cannot analyse message, too short")

    latest_position = dict()
    result = defaultdict(list)

    for i in range(len(msg) - 3):
        trigram = msg[i:i + 3]
        cuatrigram = msg[i:i + 4]

        if trigram not in latest_position:
            latest_position[trigram] = i

        if cuatrigram not in latest_position:
            latest_position[cuatrigram] = i

        trigram_distance = i - latest_position[trigram]
        cuatrigram_distance = i - latest_position[cuatrigram]

        if trigram_distance != 0:
            result[trigram].append(trigram_distance)
        if cuatrigram_distance != 0:
            result[cuatrigram].append(cuatrigram_distance)

    return result


def crack(ciphertext: str, lang: Language, no_gui=False, fast=False) -> VigenereKey:
    # Find separation for all 3 and 4 letter sequences
    distance_between_occurrences = get_separation_of_3_and_4_letter_blocks(ciphertext)
    divisor_frequency = defaultdict(int)
    processed_distances = 0

    for _, distance_list in distance_between_occurrences.items():
        for distance in distance_list:
            processed_distances += 1
            for divisor in get_divisors(distance):
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
