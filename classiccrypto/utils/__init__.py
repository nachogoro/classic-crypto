from enum import Enum


class Mode(Enum):
    """
    Enumeration representing the modes of cryptographic operations.

    Attributes:
        ENCRYPTION (int): Denotes encryption mode.
        DECRYPTION (int): Denotes decryption mode.
    """
    ENCRYPTION = 1
    DECRYPTION = 2


class Language(Enum):
    """
    Enumeration representing supported languages for cryptographic operations.

    Attributes:
        ESP (int): Represents the Spanish language.
        ENG (int): Represents the English language.

    Methods:
        from_string: Obtain a Language enum member from its string representation.
        to_string: Retrieve the string representation of a Language enum member.
    """

    ESP = 1
    ENG = 2

    @staticmethod
    def from_string(s: str) -> "Language":
        """
        Map a string to its corresponding `Language` enumeration member.

        Args:
            s (str): String representation of a language ("ESP", "ENG").

        Returns:
            Language: Corresponding Language enum member.

        Raises:
            ValueError: If the string does not map to a known Language member.
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

        Args:
            lang (Language): A Language enum member.

        Returns:
            str: String representation of the provided Language enum member.

        Raises:
            ValueError: If the Language member does not have a known string representation.
        """
        mapping = {
            Language.ESP: "ESP",
            Language.ENG: "ENG",
        }
        return mapping.get(lang)


class LetterCase(Enum):
    """
    Enumeration representing the case of letters (upper or lower).

    Attributes:
        UPPER (int): Denotes uppercase letters.
        LOWER (int): Denotes lowercase letters.
    """
    UPPER = 1
    LOWER = 2
