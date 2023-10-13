from classiccrypto.utils import alphabets
from classiccrypto.cryptoschemes.keys.caesar import CaesarKey
from classiccrypto.utils import Mode


def encrypt(message: str, key: CaesarKey) -> str:
    return translate(message, key, Mode.ENCRYPTION)


def decrypt(message: str, key: CaesarKey) -> str:
    return translate(message, key, Mode.DECRYPTION)


def translate(message: str, key: CaesarKey, mode: Mode) -> str:
    result = []
    for c in message:
        result += alphabets.shifted_letter(c,
                                           key.lang,
                                           key.key if mode == Mode.ENCRYPTION else -key.key)

    return ''.join(result)
