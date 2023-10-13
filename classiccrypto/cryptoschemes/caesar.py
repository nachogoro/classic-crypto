from classiccrypto.cryptoschemes.keys.caesar import CaesarKey
from classiccrypto.utils import Mode
from classiccrypto.utils import alphabets


def encrypt(message: str, key: CaesarKey) -> str:
    """
    Encrypt a message using the Caesar cipher with the provided key.

    :param str message: The plaintext message to be encrypted.
    :param CaesarKey key: The key (containing the shift value and language) to be used for encryption.

    :return: The encrypted message.
    :rtype: str
    """
    return translate(message, key, Mode.ENCRYPTION)


def decrypt(message: str, key: CaesarKey) -> str:
    """
    Decrypt a message using the Caesar cipher with the provided key.

    :param str message: The ciphertext message to be decrypted.
    :param CaesarKey key: The key (containing the shift value and language) to be used for decryption.

    :return: The decrypted message.
    :rtype: str
    """
    return translate(message, key, Mode.DECRYPTION)


def translate(message: str, key: CaesarKey, mode: Mode) -> str:
    """
    Translate (encrypt/decrypt) a message using the Caesar cipher based on the provided key and mode.

    This function performs the encryption or decryption (based on `mode`) by shifting each letter
    in `message` by the shift value defined in `key`.

    :param str message: The message to be translated.
    :param CaesarKey key: The key (containing the shift value and language) to be used for translation.
    :param Mode mode: The mode of translation - can be either ENCRYPTION or DECRYPTION.

    :return: The translated message.
    :rtype: str
    """
    result = []
    for c in message:
        result += alphabets.shifted_letter(c,
                                           key.lang,
                                           key.key if mode == Mode.ENCRYPTION else -key.key)

    return ''.join(result)
