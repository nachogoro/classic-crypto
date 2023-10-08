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


def lowercase_alphabet(lang: Language) -> list:
    if not hasattr(lowercase_alphabet, "eng_alphabet"):
        lowercase_alphabet.eng_alphabet = [c for c in 'abcdefghijklmnopqrstuvwxyz']
    if not hasattr(lowercase_alphabet, "esp_alphabet"):
        lowercase_alphabet.esp_alphabet = [c for c in 'abcdefghijklmnñopqrstuvwxyz']
    
    if lang == Language.ENG:
        return lowercase_alphabet.eng_alphabet
    elif lang == Language.ESP:
        return lowercase_alphabet.esp_alphabet
    else:
        raise ValueError(f"Unsupported language: {lang}")

def uppercase_alphabet(lang: Language) -> list:
    if not hasattr(uppercase_alphabet, "eng_alphabet"):
        uppercase_alphabet.eng_alphabet = [c.upper() for c in lowercase_alphabet(lang)]
    if not hasattr(uppercase_alphabet, "esp_alphabet"):
        uppercase_alphabet.esp_alphabet = [c.upper() for c in lowercase_alphabet(lang)]

    if lang == Language.ENG:
        return uppercase_alphabet.eng_alphabet
    elif lang == Language.ESP:
        return uppercase_alphabet.esp_alphabet
    else:
        raise ValueError(f"Unsupported language: {lang}")

def shifted_alphabet(lang: Language, step: int) -> list:
    alphabet = lowercase_alphabet(lang)
    result = lowercase_alphabet(lang)
    for index, elem in enumerate(alphabet):
        result[index] = alphabet[(index + step) % len(alphabet)]
    return result

def shifted_letter(c: str, lang: Language, step: int) -> str:
    alphabet = lowercase_alphabet(lang)

    if c.lower() not in alphabet:
        return c
    index = alphabet.index(c.lower())
    translated = alphabet[(index + step) % len(alphabet)]

    return translated.upper() if c.isupper() else translated

def is_in_alphabet(lang: Language, char: str) -> bool:
    return char.lower() in lowercase_alphabet(lang)