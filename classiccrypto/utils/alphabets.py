from classiccrypto.utils import LetterCase, Language
from classiccrypto.cryptoschemes.affine import AffineKey


def alphabet(lang: Language, case: LetterCase) -> list:
    """
    Get the alphabet for a given language and letter case.

    Args:
        lang (Language): The language for which to retrieve the alphabet.
        case (LetterCase): The case (upper/lower) of the alphabet.

    Returns:
        list: A list of characters representing the alphabet.

    Raises:
        ValueError: If an unsupported language is provided.
    """
    if case == LetterCase.LOWER:
        return _lowercase_alphabet(lang)
    else:
        return _uppercase_alphabet(lang)


def _lowercase_alphabet(lang: Language) -> list:
    """
    Internal function to get the lowercase alphabet for a given language.

    Args:
        lang (Language): The language for which to retrieve the alphabet.

    Returns:
        list: A list of lowercase characters representing the alphabet.

    Raises:
        ValueError: If an unsupported language is provided.
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

    Args:
        lang (Language): The language for which to retrieve the alphabet.

    Returns:
        list: A list of uppercase characters representing the alphabet.

    Raises:
        ValueError: If an unsupported language is provided.
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

    Args:
        lang (Language): The language for which to retrieve the alphabet.
        step (int): The number of positions to shift the alphabet.
        case (LetterCase): The case (upper/lower) of the alphabet.

    Returns:
        list: A list of characters representing the shifted alphabet.
    """

    src = alphabet(lang, case)
    dst = list(src)
    for index, elem in enumerate(src):
        dst[index] = src[(index + step) % len(src)]
    return dst


def shifted_letter(c: str, lang: Language, step: int) -> str:
    """
    Get a letter shifted right by a specified step for a language.

    Args:
        c (str): The character to be shifted.
        lang (Language): The language used for determining the shift.
        step (int): The number of positions to shift the letter.

    Returns:
        str: The shifted letter.
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

    Args:
        lang (Language): The language against which to check the character.
        char (str): The character to check.

    Returns:
        bool: True if the character is in the alphabet, False otherwise.
    """
    return char.lower() in _lowercase_alphabet(lang)


def alphabet_affine(key: AffineKey, case: LetterCase) -> list:
    """
    Get an affine-shifted alphabet for a language, based on the provided key.

    Args:
        key (AffineKey): The affine key providing the coefficients for the affine shift.
        case (LetterCase): The case (upper/lower) of the alphabet.

    Returns:
        list: A list of characters representing the affine-shifted alphabet.
    """
    src = alphabet(key.lang, case)
    dst = list(src)
    for index, elem in enumerate(src):
        dst[index] = src[(key.a * index + key.b) % len(src)]
    return dst
