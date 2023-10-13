from abc import abstractmethod, ABC

from classiccrypto.utils import Language


class Cipherkey(ABC):
    """
    Abstract base class representing a cipher key used in encryption and decryption processes.

    The `Cipherkey` class ensures that each cipher key implementation has a consistent interface and can be used interchangeably in encryption and decryption operations.

    :ivar Language lang: Language to be used when using this key
    """

    def __init__(self, lang: Language):
        """
        Initializes a new instance of the Cipherkey class.

        :param Language lang: An instance of the Language class managing language-related functionality.
        """
        self.lang = lang

    @abstractmethod
    def to_string(self):
        """
        Abstract method that, when implemented, should return a string representation of the cipher key.

        :return: A string representation of the cipher key.
        :rtype: str
        """
        pass
