from classiccrypto.utils import alphabets
from classiccrypto.cryptoschemes.keys.caesar import CaesarKey
from classiccrypto.utils import Mode


def encrypt(message: str, key: CaesarKey) -> str:
    """
    Encrypt a message using the Caesar cipher with the provided key.

    Args:
        message (str): The plaintext message to be encrypted.
        key (CaesarKey): The key (containing the shift value and language) to be used for encryption.

    Returns:
        str: The encrypted message.
    """
    return translate(message, key, Mode.ENCRYPTION)


def decrypt(message: str, key: CaesarKey) -> str:
    """
    Decrypt a message using the Caesar cipher with the provided key.

    Args:
        message (str): The ciphertext message to be decrypted.
        key (CaesarKey): The key (containing the shift value and language) to be used for decryption.

    Returns:
        str: The decrypted message.
    """
    return translate(message, key, Mode.DECRYPTION)


def translate(message: str, key: CaesarKey, mode: Mode) -> str:
    """
    Translate (encrypt/decrypt) a message using the Caesar cipher based on the provided key and mode.

    This function performs the encryption or decryption (based on `mode`) by shifting each letter
    in `message` by the shift value defined in `key`.

    Args:
        message (str): The message to be translated.
        key (CaesarKey): The key (containing the shift value and language) to be used for translation.
        mode (Mode): The mode of translation - can be either ENCRYPTION or DECRYPTION.

    Returns:
        str: The translated message.
    """
    result = []
    for c in message:
        result += alphabets.shifted_letter(c,
                                           key.lang,
                                           key.key if mode == Mode.ENCRYPTION else -key.key)

    return ''.join(result)
