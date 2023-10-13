from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey
from classiccrypto.utils import alphabets, LetterCase, Language


class VigenereKey(Cipherkey):
    """
    Class representing a key for the Vigenere cipher, derived from the Cipherkey base class.

    The VigenereKey class holds the key used in Vigenere cipher operations and provides
    functionality for converting the string key into a sequence of shifts.

    :ivar str key: The string used as the cipher key in Vigenere cipher operations.
    :ivar List[int] key_as_offset: A list of integer offsets derived from `key` and the specified alphabet.
    :ivar Language lang: Language to be used when using this key
    """

    def __init__(self, key: str, lang: Language):
        """
        Initialize a new VigenereKey instance.

        :param key (str): The string used as the cipher key in Vigenere cipher operations.
        :param Language lang: Instance managing language-specific operations.

        :raises ValueError: If `key` is an empty string or contains invalid characters.
        """
        super().__init__(lang)
        self.key = key
        self.key_as_offset = list()

        if not self.key:
            self.key_as_offset = [0]

        alphabet = alphabets.alphabet(lang, LetterCase.UPPER)
        self.key_as_offset = [alphabet.index(c.upper()) for c in key]

    def to_string(self) -> str:
        """
        Generate a string representation of the Vigenere cipher key.

        :return: String representation of the key.
        :rtype: str
        """
        return self.key
