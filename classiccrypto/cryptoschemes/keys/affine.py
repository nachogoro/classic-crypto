from classiccrypto.utils import Language
from classiccrypto.cryptoschemes.keys.cipherkey import Cipherkey


class AffineKey(Cipherkey):
    """
    Class representing a key for the Affine cipher, derived from the Cipherkey base class.

    The AffineKey class stores and manages the parameters for Affine cipher operations, ensuring
    consistent functionality for converting the key to its string representation.

    Attributes:
        a (int): The 'a' parameter in the affine cipher key, used for encryption and decryption.
        b (int): The 'b' parameter in the affine cipher key, used for encryption and decryption.
        lang (Language): Language to be used when using this key

    Methods:
        to_string: Provide a string representation of the cipher key.
    """

    def __init__(self, a: int, b: int, lang: Language):
        """
        Initialize a new AffineKey instance.

        Args:
            a (int): The 'a' parameter in the affine cipher key.
            b (int): The 'b' parameter in the affine cipher key.
            lang (Language): Instance managing language-specific operations.
        """
        super().__init__(lang)
        self.a = a
        self.b = b

    def to_string(self) -> str:
        """
        Generate a string representation of the Affine cipher key.

        Returns:
            str: String representation of the key in the format "a: [a_value]; b: [b_value]".
        """
        return f"a: {self.a}; b: {self.b}"
