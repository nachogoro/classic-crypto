import classiccrypto.utils.frequency
from classiccrypto.utils import Language, LetterCase, alphabets
from classiccrypto.cryptoschemes.caesar import CaesarKey


def crack(ciphertext: str, lang: Language, fast: bool) -> CaesarKey:
    if fast:
        crack_congruence(ciphertext, lang)
    # Find best fit between message histogram and language histogram
    return CaesarKey(
        classiccrypto.utils.frequency.find_step_for_best_match(
            classiccrypto.utils.frequency.normalized_histogram(ciphertext, lang),
            classiccrypto.utils.frequency.language_histogram(lang)),
        lang)


def crack_congruence(ciphertext: str, lang: Language) -> CaesarKey:
    alphabet = alphabets.alphabet(lang, LetterCase.LOWER)
    cipher_histogram = classiccrypto.utils.frequency.normalized_histogram(ciphertext, lang)
    language_histogram = classiccrypto.utils.frequency.language_histogram(lang)
    most_common_cipher_letter = alphabet.index(max(cipher_histogram,
                                                   key=lambda x: x[1])[0])
    most_common_language_letter = alphabet.index(max(language_histogram,
                                                     key=lambda x: x[1])[0])

    n = len(alphabet)

    b = (most_common_cipher_letter - most_common_language_letter) % n

    return CaesarKey(b, lang)
