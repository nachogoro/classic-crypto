from enum import Enum


class Mode(Enum):
    ENCRYPTION = 1
    DECRYPTION = 2


class Language(Enum):
    ESP = 1
    ENG = 2

    @staticmethod
    def from_string(s: str) -> "Language":
        mapping = {
            "ESP": Language.ESP,
            "ENG": Language.ENG,
        }
        return mapping.get(s.upper())

    @staticmethod
    def to_string(lang: "Language") -> str:
        mapping = {
            Language.ESP: "ESP",
            Language.ENG: "ENG",
        }
        return mapping.get(lang)


class LetterCase(Enum):
    UPPER = 1
    LOWER = 2
