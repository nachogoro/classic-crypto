from abc import abstractmethod, ABC

from classiccrypto.utils import Language


class Cipherkey(ABC):
    def __init__(self, lang: Language):
        self.lang = lang
    @abstractmethod
    def to_string(self):
        pass