from classiccrypto.utils import Language
from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey


class CaesarKey(Cipherkey):
    """
    Class representing a key for the Caesar cipher, derived from the Cipherkey base class.

    The CaesarKey class holds the key for Caesar cipher operations, and ensures
    appropriate functionality is implemented for key string representation.

    Attributes:
        key (int): The shift value used for encryption and decryption in the Caesar cipher.
        lang (Language): Language to be used when using this key
    Methods:
        to_string: Provide a string representation of the cipher key.
    """

    def __init__(self, key: int, lang: Language):
        """
        Initialize a new CaesarKey instance.

        Args:
            key (int): The Caesar cipher shift value.
            lang (Language): Instance managing language-specific operations.
        """
        super().__init__(lang)
        self.key = key

    def to_string(self) -> str:
        """
        Generate a string representation of the Caesar cipher key.

        Returns:
            str: String representation of the key.
        """
        return str(self.key)