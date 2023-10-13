from enum import Enum


class Mode(Enum):
    """
    Enumeration representing the modes of cryptographic operations.
    """
    ENCRYPTION = 1
    DECRYPTION = 2


class Language(Enum):
    """
    Enumeration representing supported languages for cryptographic operations.
    """

    ESP = 1
    ENG = 2

    @staticmethod
    def from_string(s: str) -> "Language":
        """
        Map a string to its corresponding `Language` enumeration member.

        :param str s: String representation of a language ("ESP", "ENG").

        :return: Corresponding Language enum member.
        :rtype: Language

        :raises ValueError: If the string does not map to a known Language member.
    """
        mapping = {
            "ESP": Language.ESP,
            "ENG": Language.ENG,
        }
        return mapping.get(s.upper())

    @staticmethod
    def to_string(lang: "Language") -> str:
        """
        Retrieve the string identifier of a `Language` enumeration member.

        :param Language lang: A Language enum member.

        :return: String representation of the provided Language enum member.
        :rtype: str

        :raises ValueError: If the Language member does not have a known string representation.
    """
        mapping = {
            Language.ESP: "ESP",
            Language.ENG: "ENG",
        }
        return mapping.get(lang)


class LetterCase(Enum):
    """
    Enumeration representing the case of letters (upper or lower).
    """
    UPPER = 1
    LOWER = 2
