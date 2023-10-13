from classiccrypto.utils import Language
from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey


class CaesarKey(Cipherkey):
    def __init__(self, key: int, lang: Language):
        super().__init__(lang)
        self.key = key

    def to_string(self) -> str:
        return str(self.key)