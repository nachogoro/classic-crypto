from classiccrypto.utils import Language
from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey


class CaesarKey(Cipherkey):
    """
    Class representing a key for the Caesar cipher, derived from the Cipherkey base class.

    The CaesarKey class holds the key for Caesar cipher operations, and ensures
    appropriate functionality is implemented for key string representation.

    :ivar int key: The shift value used for encryption and decryption in the Caesar cipher.
    :ivar Language lang: Language to be used when using this key
    """

    def __init__(self, key: int, lang: Language):
        """
        Initialize a new CaesarKey instance.

        :param int key: The Caesar cipher shift value.
        :param Language lang: Instance managing language-specific operations.
        """
        super().__init__(lang)
        self.key = key

    def to_string(self) -> str:
        """
        Generate a string representation of the Caesar cipher key.

        :return: String representation of the key.
        :rtype: str
        """
        return str(self.key)
