import math

from classiccrypto.utils import alphabets, Language, LetterCase
from classiccrypto.cryptoschemes.affine import decrypt, AffineKey
import classiccrypto.utils.frequency


def crack(ciphertext: str, lang: Language, fast:bool) -> AffineKey:
    if fast:
        return crack_congruence(ciphertext, lang)
    return crack_bruteforce(ciphertext, lang)


def crack_bruteforce(ciphertext: str, lang: Language) -> AffineKey:
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