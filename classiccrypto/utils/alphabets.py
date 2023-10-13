from classiccrypto.utils import LetterCase, Language
from classiccrypto.cryptoschemes.affine import AffineKey


def alphabet(lang: Language, case: LetterCase) -> list:
    if case == LetterCase.LOWER:
        return _lowercase_alphabet(lang)
    else:
        return _uppercase_alphabet(lang)


def _lowercase_alphabet(lang: Language) -> list:
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
    src = alphabet(lang, case)
    dst = list(src)
    for index, elem in enumerate(src):
        dst[index] = src[(index + step) % len(src)]
    return dst


def shifted_letter(c: str, lang: Language, step: int) -> str:
    letter_case = LetterCase.LOWER if c.islower() else LetterCase.UPPER
    src_alphabet = alphabet(lang, letter_case)
    target_alphabet = shifted_alphabet(lang,
                                       step,
                                       letter_case)

    if c not in src_alphabet:
        return c
    return target_alphabet[src_alphabet.index(c)]


def is_in_alphabet(lang: Language, char: str) -> bool:
    return char.lower() in _lowercase_alphabet(lang)


def alphabet_affine(key: AffineKey, case: LetterCase) -> list:
    src = alphabet(key.lang, case)
    dst = list(src)
    for index, elem in enumerate(src):
        dst[index] = src[(key.a * index + key.b) % len(src)]
    return dst
