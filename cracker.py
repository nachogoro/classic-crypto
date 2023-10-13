import argparse
from enum import Enum

from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey
import classiccrypto.cryptoschemes.cracking.vigenere
import classiccrypto.cryptoschemes.cracking.caesar
import classiccrypto.cryptoschemes.cracking.affine
from classiccrypto.utils import alphabets
from classiccrypto.utils import Language
import classiccrypto

class Cryptoscheme(Enum):
    CAESAR = 1
    AFFINE = 2
    VIGENERE = 3

    @staticmethod
    def from_string(s: str) -> "Cryptoscheme":
        mapping = {
            "caesar": Cryptoscheme.CAESAR,
            "affine": Cryptoscheme.AFFINE,
            "vigenere": Cryptoscheme.VIGENERE,
        }
        return mapping.get(s.lower())


def parse_arguments() -> object:
    # Create the parser
    parser = argparse.ArgumentParser(description='Classic Encryption Cracker. '
                                                 'Cracks the key used to encrypt a ciphertext.')

    # Add the arguments
    parser.add_argument('--cryptoscheme',
                        metavar='cryptoscheme',
                        type=str,
                        choices=['vigenere', 'caesar', 'affine'],
                        help='The cryptoscheme to crack: vigenere, caesar, or affine',
                        required=True)

    parser.add_argument('--no-gui',
                        action='store_true',
                        help='Ensure no GUI pop ups, use CLI for all outputs')

    parser.add_argument('--fast',
                        action='store_true',
                        help='Crack as fast as possible (less reliable)')

    parser.add_argument('--lang',
                        metavar='lang',
                        type=str,
                        choices=['ESP', 'ENG'],
                        required=True,
                        help='Language used in the encryption: ESP or ENG')

    parser.add_argument('--decrypt',
                        action='store_true',
                        help='Whether the text should be decrypted')

    parser.add_argument('filepath',
                        metavar='filepath',
                        type=str,
                        help='The path to the file to decrypt')

    return parser.parse_args()


def crack(cryptoscheme: Cryptoscheme, message: str, lang: Language, no_gui: bool, fast: bool) -> Cipherkey:
    if cryptoscheme == Cryptoscheme.CAESAR:
        return classiccrypto.cryptoschemes.cracking.caesar.crack(message, lang, fast)
    elif cryptoscheme == Cryptoscheme.AFFINE:
        return classiccrypto.cryptoschemes.cracking.affine.crack(message, lang, fast)
    elif cryptoscheme == Cryptoscheme.VIGENERE:
        return classiccrypto.cryptoschemes.cracking.vigenere.crack(message, lang, no_gui, fast)
    else:
        raise ValueError('Invalid scheme: ' + str(cryptoscheme))


def decrypt(cryptoscheme: Cryptoscheme, message: str, key: Cipherkey) -> str:
    if cryptoscheme == Cryptoscheme.CAESAR:
        return classiccrypto.cryptoschemes.caesar.decrypt(message, key)
    elif cryptoscheme == Cryptoscheme.AFFINE:
        return classiccrypto.cryptoschemes.affine.decrypt(message, key)
    elif cryptoscheme == Cryptoscheme.VIGENERE:
        return classiccrypto.cryptoschemes.vigenere.decrypt(message, key)


def main():
    args = parse_arguments()
    try:
        with open(args.filepath, "r") as src:
            ciphertext = src.read()
    except IOError:
        print(f"Error opening {args.filepath}")
        return

    language = Language.from_string(args.lang)
    cryptoscheme = Cryptoscheme.from_string(args.cryptoscheme)

    # Clean the ciphertext
    clean_ciphertext = ''.join([c.upper() for c in ciphertext if alphabets.is_in_alphabet(language, c)])

    cipher_key = crack(cryptoscheme,
                       clean_ciphertext,
                       language,
                       args.no_gui,
                       args.fast)

    print(f'Encryption key: {cipher_key.to_string()}')

    if args.decrypt:
        print('\nDecrypted message:')
        print(decrypt(cryptoscheme, ciphertext, cipher_key))


if __name__ == '__main__':
    main()
