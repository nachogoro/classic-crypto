from classiccrypto.utils import Language
from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey


class AffineKey(Cipherkey):
    def __init__(self, a: int, b: int, lang: Language):
        super().__init__(lang)
        self.a = a
        self.b = b

    def to_string(self) -> str:
        return f"a: {self.a}; b: {self.b}"