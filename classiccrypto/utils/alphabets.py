from classiccrypto.cryptoschemes.affine import AffineKey
from classiccrypto.utils import LetterCase, Language


def alphabet(lang: Language, case: LetterCase) -> list:
    """
    Get the alphabet for a given language and letter case.

    :param Language lang: The language for which to retrieve the alphabet.
    :param LetterCase case: The case (upper/lower) of the alphabet.

    :return: A list of characters representing the alphabet.
    :rtype: list

    :raises ValueError: If an unsupported language is provided.
    """
    if case == LetterCase.LOWER:
        return _lowercase_alphabet(lang)
    else:
        return _uppercase_alphabet(lang)


def _lowercase_alphabet(lang: Language) -> list:
    """
    Internal function to get the lowercase alphabet for a given language.

    :param Language lang: The language for which to retrieve the alphabet.

    :return: A list of lowercase characters representing the alphabet.
    :rtype: list

    :raises ValueError: If an unsupported language is provided.
    """
    if not hasattr(_lowercase_alphabet, "eng_alphabet"):
        _lowercase_alphabet.eng_alphabet = [c for c in 'abcdefghijklmnopqrstuvwxyz']
    if not hasattr(_lowercase_alphabet, "esp_alphabet"):
        _lowercase_alphabet.esp_alphabet = [c for c in 'abcdefghijklmnñopqrstuvwxyz']

    if lang == Language.ENG:
        return _lowercase_alphabet.eng_alphabet
    elif lang == Language.ESP:
        return _lowercase_alphabet.esp_alphabet
    else:
        raise ValueError(f"Unsupported language: {lang}")


def _uppercase_alphabet(lang: Language) -> list:
    """
    Internal function to get the uppercase alphabet for a given language.

    :param Language lang: The language for which to retrieve the alphabet.

    :return: A list of uppercase characters representing the alphabet.
    :rtype: list

    :raises ValueError: If an unsupported language is provided.
    """
    if not hasattr(_uppercase_alphabet, "eng_alphabet"):
        _uppercase_alphabet.eng_alphabet = [c.upper() for c in _lowercase_alphabet(Language.ENG)]
    if not hasattr(_uppercase_alphabet, "esp_alphabet"):
        _uppercase_alphabet.esp_alphabet = [c.upper() for c in _lowercase_alphabet(Language.ESP)]

    if lang == Language.ENG:
        return _uppercase_alphabet.eng_alphabet
    elif lang == Language.ESP:
        return _uppercase_alphabet.esp_alphabet
    else:
        raise ValueError(f"Unsupported language: {lang}")


def shifted_alphabet(lang: Language, step: int, case: LetterCase) -> list:
    """
    Get an alphabet shifted to the right by a specified step for a language and case.

    :param Language lang: The language for which to retrieve the alphabet.
    :param int step: The number of positions to shift the alphabet.
    :param LetterCase case: The case (upper/lower) of the alphabet.

    :return: A list of characters representing the shifted alphabet.
    :rtype: list
    """

    src = alphabet(lang, case)
    dst = list(src)
    for index, elem in enumerate(src):
        dst[index] = src[(index + step) % len(src)]
    return dst


def shifted_letter(c: str, lang: Language, step: int) -> str:
    """
    Get a letter shifted right by a specified step for a language.

    :param str c: The character to be shifted.
    :param Language lang: The language used for determining the shift.
    :param int step: The number of positions to shift the letter.

    :return: The shifted letter.
    :rtype: str
    """
    letter_case = LetterCase.LOWER if c.islower() else LetterCase.UPPER
    src_alphabet = alphabet(lang, letter_case)
    target_alphabet = shifted_alphabet(lang,
                                       step,
                                       letter_case)

    if c not in src_alphabet:
        return c
    return target_alphabet[src_alphabet.index(c)]


def is_in_alphabet(lang: Language, char: str) -> bool:
    """
    Check whether a character is in the alphabet of a specified language.

    :param Language lang: The language against which to check the character.
    :param str char: The character to check.

    :return: True if the character is in the alphabet, False otherwise.
    :rtype: bool
    """
    return char.lower() in _lowercase_alphabet(lang)


def alphabet_affine(key: AffineKey, case: LetterCase) -> list:
    """
    Get an affine-shifted alphabet for a language, based on the provided key.

    :param AffineKey key: The affine key providing the coefficients for the affine shift.
    :param LetterCase case: The case (upper/lower) of the alphabet.

    :return: A list of characters representing the affine-shifted alphabet.
    :rtype: list
    """
    src = alphabet(key.lang, case)
    dst = list(src)
    for index, elem in enumerate(src):
        dst[index] = src[(key.a * index + key.b) % len(src)]
    return dst
