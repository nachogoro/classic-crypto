import classiccrypto.utils.frequency
from classiccrypto.utils import Language, LetterCase, alphabets
from classiccrypto.cryptoschemes.caesar import CaesarKey


def crack(ciphertext: str, lang: Language, fast: bool) -> CaesarKey:
    """
    Attempt to crack a ciphertext encrypted with the Caesar cipher using statistical analysis.

    The function can use either a congruence method or a method based on finding the best fit
    between letter frequency histograms, depending on the value of `fast`.

    :param str ciphertext: The encrypted message.
    :param Language lang: The language object to be used for decryption.
    :param bool fast: If True, use a faster congruence method.

    :return: The most likely key to have been used for the encryption.
    :rtype: CaesarKey
    """
    if fast:
        crack_congruence(ciphertext, lang)
    # Find best fit between message histogram and language histogram
    return CaesarKey(
        classiccrypto.utils.frequency.find_step_for_best_match(
            classiccrypto.utils.frequency.normalized_histogram(ciphertext, lang),
            classiccrypto.utils.frequency.language_histogram(lang)),
        lang)


def crack_congruence(ciphertext: str, lang: Language) -> CaesarKey:
    """
    Attempt to crack a Caesar cipher using congruence relations between the most frequent letters.

    This function finds the most frequent letters in the `ciphertext` and a reference language,
    then determines the most likely shift value (key) using the positional difference between these
    letters.

    :param str ciphertext: The encrypted message.
    :param Language lang: The language object to be used for decryption.

    :return: The most likely key to have been used for the encryption.
    :rtype: CaesarKey
    """
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
