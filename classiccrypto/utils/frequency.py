from classiccrypto.utils import alphabets
from classiccrypto.utils import Language, LetterCase


def normalized_histogram(s: str, lang: Language) -> list:
    # Define the alphabet for each language
    alphabet = alphabets.alphabet(lang, LetterCase.LOWER)

    # Initialize the dictionary with all letters set to 0
    freq = {letter: 0 for letter in alphabet}

    total_char_count = 0

    # Count the frequency of each letter in the string
    for char in s.lower():
        # This avoids non-alphabetic symbols
        if char in freq:
            freq[char] += 1
            total_char_count += 1

    for char in freq.keys():
        freq[char] /= total_char_count

    return [(k, v) for k, v in freq.items()]


def language_histogram(lang: Language) -> list:
    if not hasattr(language_histogram, "esp_histogram"):
        language_histogram.esp_histogram = {
            'a': 12.53, 'b': 1.42, 'c': 4.68, 'd': 5.86, 'e': 13.68, 'f': 0.69, 'g': 1.01, 'h': 0.70, 'i': 6.25,
            'j': 0.44, 'k': 0.02, 'l': 4.97, 'm': 3.15, 'n': 6.71, 'ñ': 0.31, 'o': 8.68, 'p': 2.51, 'q': 0.88,
            'r': 6.87, 's': 7.98, 't': 4.63, 'u': 3.93, 'v': 0.90, 'w': 0.01, 'x': 0.22, 'y': 0.90, 'z': 0.52}

        for key in language_histogram.esp_histogram:
            language_histogram.esp_histogram[key] /= 100

    if not hasattr(language_histogram, "eng_histogram"):
        language_histogram.eng_histogram = {
            'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2, 'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.15,
            'k': 0.77, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1,
            'u': 2.8, 'v': 0.98, 'w': 2.4, 'x': 0.15, 'y': 2.0, 'z': 0.074}

        for key in language_histogram.eng_histogram:
            language_histogram.eng_histogram[key] /= 100

    if lang == Language.ESP:
        return [(k, v) for k, v in language_histogram.esp_histogram.items()]
    elif lang == Language.ENG:
        return [(k, v) for k, v in language_histogram.eng_histogram.items()]


def empty_histogram(lang: Language) -> list:
    return [(k, 0) for k in alphabets.alphabet(lang, LetterCase.LOWER)]


def similarity(histo1: list, histo2: list) -> float:
    shortest = histo1 if len(histo1) < len(histo2) else histo2
    longest = histo2 if len(histo1) < len(histo2) else histo1

    difference = 0
    for index in range(len(longest)):
        if index < len(shortest):
            diff = abs(longest[index][1] - shortest[index][1])
        else:
            diff = abs(longest[index][1])

        difference += diff ** 2

    return 1 - difference


def _shift_list(l: list, step: int) -> list:
    if not l:
        return []

    step = -step
    step = step % len(l)
    return l[step:] + l[:step]


def slide_histogram(histogram: list, step: int) -> list:
    return _shift_list(histogram, step)


def histogram_from_file(filepath: str, lang: Language) -> list:
    try:
        if filepath:
            with open(filepath, 'r') as file:
                return normalized_histogram(file.read(), lang)
    except:
        pass

    return empty_histogram(lang)


def find_step_for_best_match(target_histogram: list, sliding_histogram: list) -> int:
    """
    Returns how many times should sliding_histogram shift to the right (closed)
    so it is as similar as possible to target_histogram.
    :param target_histogram: Histogram used as reference
    :param sliding_histogram: Histogram which slides
    :return: The number of closed right shifts sliding histogram which maximises their similarity.
    It is a number in [0, len(target_histogram) - 1]
    """
    best_similarity = similarity(target_histogram, sliding_histogram)
    step_for_best_fit = 0

    for step in range(1, len(target_histogram)):
        shifted_histogram = slide_histogram(sliding_histogram, step)
        candidate_similarity = similarity(shifted_histogram, target_histogram)

        if candidate_similarity > best_similarity:
            best_similarity = candidate_similarity
            step_for_best_fit = step

    return step_for_best_fit


def sort_histogram_by_key(histogram: list) -> list:
    if not histogram:
        return []

    if isinstance(histogram[0][0], str) and all(len(c) == 1 for (c,_) in histogram):
        # It's a letter histogram, so we need to take care of letter ñ in Spanish
        alphabet = None
        if len(histogram) == len(alphabets.alphabet(Language.ESP, LetterCase.LOWER)):
            alphabet = alphabets.alphabet(Language.ESP, LetterCase.LOWER)
        else:
            alphabet = alphabets.alphabet(Language.ENG, LetterCase.LOWER)

        return sorted(histogram, key=lambda x: alphabet.index(x[0]), reverse=False)

    return sorted(histogram, key=lambda e: e[0], reverse=False)
