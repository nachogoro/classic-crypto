from classiccrypto.utils import alphabets, LetterCase, Language
from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey


class VigenereKey(Cipherkey):
    """
    Class representing a key for the Vigenere cipher, derived from the Cipherkey base class.

    The VigenereKey class holds the key used in Vigenere cipher operations and provides
    functionality for converting the string key into a sequence of shifts.

    Attributes:
        key (str): The string used as the cipher key in Vigenere cipher operations.
        key_as_offset (List[int]): A list of integer offsets derived from `key` and the specified alphabet.
        lang (Language): Language to be used when using this key

    Methods:
        to_string: Provide a string representation of the cipher key.
    """

    def __init__(self, key: str, lang: Language):
        """
        Initialize a new VigenereKey instance.

        Args:
            key (str): The string used as the cipher key in Vigenere cipher operations.
            lang (Language): Instance managing language-specific operations.

        Raises:
            ValueError: If `key` is an empty string or contains invalid characters.
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

        Returns:
            str: String representation of the key.
        """
        return self.key
