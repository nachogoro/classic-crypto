from classiccrypto.utils import alphabets, LetterCase, Language
from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey


class VigenereKey(Cipherkey):
    def __init__(self, key: str, lang: Language):
        super().__init__(lang)
        self.key = key
        self.key_as_offset = list()

        if not self.key:
            self.key_as_offset = [0]

        alphabet = alphabets.alphabet(lang, LetterCase.UPPER)
        self.key_as_offset = [alphabet.index(c.upper()) for c in key]

    def to_string(self) -> str:
        return self.key