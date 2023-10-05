from enum import Enum


class Language(Enum):
    ESP = 1
    ENG = 2

    @staticmethod
    def from_string(s: str) -> "Language":
        mapping = {
            "ESP": Language.ESP,
            "ENG": Language.ENG,
        }
        return mapping.get(s.upper())

    @staticmethod
    def to_string(lang: "Language") -> str:
        mapping = {
            Language.ESP: "ESP",
            Language.ENG: "ENG",
        }
        return mapping.get(lang)


def alphabet_for_language(lang: Language) -> list:
    if lang == Language.ENG:
        return 'abcdefghijklmnopqrstuvwxyz'
    elif lang == Language.ESP:
        return 'abcdefghijklmnñopqrstuvwxyz'
    else:
        raise ValueError(f"Unsupported language: {lang}")

def normalized_histogram(s: str, lang: Language) -> dict:
    # Define the alphabet for each language
    alphabet = alphabet_for_language(lang)

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

    return freq


def frequency_per_language(lang: Language) -> dict:
    if not hasattr(frequency_per_language, "esp_histogram"):
        frequency_per_language.esp_histogram = {
            'a': 12.53, 'b': 1.42, 'c': 4.68, 'd': 5.86, 'e': 13.68, 'f': 0.69, 'g': 1.01, 'h': 0.70, 'i': 6.25,
            'j': 0.44, 'k': 0.02, 'l': 4.97, 'm': 3.15, 'n': 6.71, 'ñ': 0.31, 'o': 8.68, 'p': 2.51, 'q': 0.88,
            'r': 6.87, 's': 7.98, 't': 4.63, 'u': 3.93, 'v': 0.90, 'w': 0.01, 'x': 0.22, 'y': 0.90, 'z': 0.52}

        for key in frequency_per_language.esp_histogram:
            frequency_per_language.esp_histogram[key] /= 100


    if not hasattr(frequency_per_language, "eng_histogram"):
        frequency_per_language.eng_histogram = {
            'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2, 'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.15,
            'k': 0.77, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1,
            'u': 2.8, 'v': 0.98, 'w': 2.4, 'x': 0.15, 'y': 2.0, 'z': 0.074}

        for key in frequency_per_language.eng_histogram:
            frequency_per_language.eng_histogram[key] /= 100

    if lang == Language.ESP:
        return frequency_per_language.esp_histogram
    elif lang == Language.ENG:
        return frequency_per_language.eng_histogram


def empty_histogram(lang: Language) -> dict:
    result = dict()
    alphabet = alphabet_for_language(lang)
    for char in alphabet:
        result[char] = 0
    return result


def similarity(histo1: dict, histo2: dict) -> float:
    difference = 0
    for key in histo1.keys():
        difference += abs(histo1[key] - histo2[key])**2
    return 1 - difference

def slide_histogram(histo: dict, step: int) -> dict:
    result = dict()

    letters = list(histo.keys())
    n = len(letters)

    for index, char in enumerate(letters):
        result[char] = histo[letters[(index - step) % n]]

    return result
