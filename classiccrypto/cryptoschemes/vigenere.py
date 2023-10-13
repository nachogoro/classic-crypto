from classiccrypto.utils import alphabets
from classiccrypto.cryptoschemes.keys.vigenere import VigenereKey
from classiccrypto.utils import Mode


def encrypt(message: str, key: VigenereKey) -> str:
    return translate(message, key, Mode.ENCRYPTION)


def decrypt(message: str, key: VigenereKey) -> str:
    return translate(message, key, Mode.DECRYPTION)


def translate(message: str, key: VigenereKey, mode: Mode) -> str:
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