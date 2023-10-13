from classiccrypto.utils import alphabets
from classiccrypto.cryptoschemes.keys.vigenere import VigenereKey
from classiccrypto.utils import Mode


def encrypt(message: str, key: VigenereKey) -> str:
    """
    Encrypt a message using the Vigenere cipher with the provided key.

    :param str message: The plaintext message to be encrypted.
    :param VigenereKey key: The key (containing the shift value and language) to be used for encryption.

    :return: The encrypted message.
    :rtype: str
    """
    return translate(message, key, Mode.ENCRYPTION)


def decrypt(message: str, key: VigenereKey) -> str:
    """
    Decrypt a message using the Vigenere cipher with the provided key.

    :param str message: The ciphertext message to be decrypted.
    :param VigenereKey key: The key (containing the shift value and language) to be used for decryption.

    :return: The decrypted message.
    :rtype: str
    """
    return translate(message, key, Mode.DECRYPTION)


def translate(message: str, key: VigenereKey, mode: Mode) -> str:
    """
    Translate (encrypt/decrypt) a message using the Vigenere cipher based on the provided key and mode.

    This function performs the encryption or decryption (based on `mode`) by shifting each letter
    in `message` by the shift value defined in `key`.

    :param str message: The message to be translated.
    :param VigenereKey key: The key (containing the shift value and language) to be used for translation.
    :param Mode mode: The mode of translation - can be either ENCRYPTION or DECRYPTION.

    :return: The translated message.
    :rtype: str
    """
    result = []

    processed_letters = 0
    for index in range(len(message)):
        to_translate = message[index]

        if not alphabets.is_in_alphabet(key.lang, to_translate):
            result += to_translate
            continue

        offset = key.key_as_offset[processed_letters % len(key.key_as_offset)]
        if mode == Mode.DECRYPTION:
            offset = -offset

        result += alphabets.shifted_letter(to_translate,
                                           key.lang,
                                           offset)
        processed_letters += 1

    return ''.join(result)
