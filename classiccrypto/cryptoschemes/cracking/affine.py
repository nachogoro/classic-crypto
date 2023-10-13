import math

from classiccrypto.utils import alphabets, Language, LetterCase
from classiccrypto.cryptoschemes.affine import decrypt, AffineKey
import classiccrypto.utils.frequency


def crack(ciphertext: str, lang: Language, fast:bool) -> AffineKey:
    """
    Attempt to crack a ciphertext encrypted with the Affine cipher using statistical analysis.

    :param str ciphertext: The encrypted message.
    :param Language lang: The language object to be used for decryption.
    :param bool fast: If True, use a faster but possibly less accurate cracking method.

    :return: The most likely key to have been used for the encryption.
    :rtype: AffineKey
    """
    if fast:
        return crack_congruence(ciphertext, lang)
    return crack_bruteforce(ciphertext, lang)


def crack_bruteforce(ciphertext: str, lang: Language) -> AffineKey:
    """
    Attempt to crack an Affine cipher by brute-forcing all possible keys.

    This function decrypts the `ciphertext` with all possible keys, comparing the decrypted text's
    letter frequency histogram to the reference language histogram and selecting the key for which
    the decrypted text has the highest similarity to the reference language.

    :param str ciphertext: The encrypted message.
    :param Language lang: The language object to be used for decryption.

    :return: The key that yields the most likely plaintext, based on letter frequency.
    :rtype: AffineKey
    """
    clear_alphabet = alphabets.alphabet(lang, LetterCase.UPPER)
    n = len(clear_alphabet)

    best_similarity = -1
    key = None

    # Brute force both parameters
    for a in range(1, n):
        if math.gcd(a, n) != 1:
            # Invalid value for a, don't try it
            continue

        for b in range(0, n):
            candidate_key = AffineKey(a, b, lang)
            candidate_decryption = decrypt(ciphertext, candidate_key)
            similarity = classiccrypto.utils.frequency.similarity(
                classiccrypto.utils.frequency.normalized_histogram(candidate_decryption, lang),
                classiccrypto.utils.frequency.language_histogram(lang))

            if similarity > best_similarity:
                best_similarity = similarity
                key = candidate_key

    return key


def crack_congruence(ciphertext: str, lang: Language) -> AffineKey | None:
    """
    Attempt to crack an Affine cipher using congruence relations between the most frequent letters.

    This function determines the most frequent letters in the `ciphertext` and in a reference
    language, then uses their positions to estimate the most likely key using congruence relations.

    :param str ciphertext: The encrypted message.
    :param Language lang: The language object to be used for decryption.

    :return: The most likely key to have been used for the encryption, or None if a likely key couldn't be determined.
    :rtype: AffineKey
    """
    language_histogram = classiccrypto.utils.frequency.language_histogram(lang)
    cipher_histogram = classiccrypto.utils.frequency.normalized_histogram(ciphertext, lang)

    def top_two(hist: list) -> list:
        return [k for (k, v) in sorted(hist, key=lambda x: x[1], reverse=True)[:2]]

    alphabet = alphabets.alphabet(lang, LetterCase.LOWER)
    n = len(alphabet)

    most_common_clear_letters = [alphabet.index(c) for c in top_two(language_histogram)]
    most_common_cipher_letters = [alphabet.index(c) for c in top_two(cipher_histogram)]

    cipher_diff = (most_common_cipher_letters[1] - most_common_cipher_letters[0]) % n
    clear_diff = (most_common_clear_letters[1] - most_common_clear_letters[0]) % n

    if math.gcd(clear_diff, n) != 1:
        return None

    a = cipher_diff * pow(clear_diff, -1, mod=n) % n
    b = (most_common_cipher_letters[0] - most_common_clear_letters[0] * a) % n

    return AffineKey(a, b, lang)
