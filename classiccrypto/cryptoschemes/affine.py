from classiccrypto.utils import alphabets
from classiccrypto.utils.alphabets import LetterCase
from classiccrypto.cryptoschemes.keys.affine import AffineKey
from classiccrypto.utils import Mode


def encrypt(message: str, key: AffineKey) -> str:
    """
    Encrypt a message using the Affine cipher with the provided key.

    :param str message: The message to be encrypted.
    :param AffineKey key: The key to be used for encryption.

    :return: The encrypted message.
    :rtype: str
    """
    return translate(message, key, Mode.ENCRYPTION)


def decrypt(message: str, key: AffineKey) -> str:
    """
    Decrypt a message using the Affine cipher with the provided key.

    :param str message: The message to be decrypted.
    :param AffineKey key: The key to be used for decryption.

    :return: The decrypted message.
    :rtype: str
    """
    return translate(message, key, Mode.DECRYPTION)


def translate(message: str, key: AffineKey, mode: Mode) -> str:
    """
    Translate (encrypt/decrypt) a message using the Affine cipher based on the provided key and mode.

    :param str message: The message to be translated.
    :param AffineKey key: The key to be used for translation.
    :param Mode mode: The mode of translation - can be either ENCRYPTION or DECRYPTION.

    :return: The translated message.
    :rtype: str
    """
    original_alphabet = alphabets.alphabet(key.lang,
                                           LetterCase.UPPER)

    transformed_alphabet = alphabets.alphabet_affine(key, LetterCase.UPPER)

    if mode == Mode.ENCRYPTION:
        src = original_alphabet
        dst = transformed_alphabet
    else:
        src = transformed_alphabet
        dst = original_alphabet

    result = []
    for c in message:
        if c.upper() not in src:
            translated = c
        else:
            translated = dst[src.index(c.upper())]
        result.append(translated.upper() if c.isupper() else translated.lower())

    return ''.join(result)
