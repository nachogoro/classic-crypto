from abc import abstractmethod, ABC

from classiccrypto.utils import Language


class Cipherkey(ABC):
    """
    Abstract base class representing a cipher key used in encryption and decryption processes.

    The `Cipherkey` class ensures that each cipher key implementation has a consistent interface and can be used interchangeably in encryption and decryption operations.

    Attributes:
        lang (Language): Language to be used when using this key
    Methods:
        to_string: Abstract method that should return a string representation of the cipher key.
    """

    def __init__(self, lang: Language):
        """
        Initializes a new instance of the Cipherkey class.

        Args:
            lang (Language): An instance of the Language class managing language-related functionality.
        """
        self.lang = lang

    @abstractmethod
    def to_string(self):
        """
        Abstract method that, when implemented, should return a string representation of the cipher key.

        Returns:
            str: A string representation of the cipher key.
        """
        pass
