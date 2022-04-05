# -*- coding: utf-8 -*-
from emoji import is_emoji

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
LETTERS = LOWERCASE + UPPERCASE
HEXDIGITS = DIGITS + "abcdef" + "ABCDEF"
USERCHARS = DIGITS + LETTERS + "_"


class Validator:
    @staticmethod
    def color(value: str) -> str:
        if value[0] == "#":
            value = value[1:]
        if len(value) not in (3, 6) or any([char not in HEXDIGITS for char in value]):
            raise ValueError(f"Invalid HEX code: '{value}'")
        return value.upper()

    @staticmethod
    def username(value: str) -> str:
        if not value:
            raise ValueError("Username must be specified")
        if any([char not in USERCHARS for char in value]):
            raise ValueError(f"Invalid username: '{value}'")
        return value.lower()


class FieldValidator:
    @staticmethod
    def username(field: str, value: str) -> str:
        if any([char not in USERCHARS for char in value]):
            raise ValueError(f"Invalid username in '{field}' field: '{value}'")
        return value.lower()

    @staticmethod
    def content(field: str, value: str) -> str:
        return value.replace("ACTION", "", 1)

    @staticmethod
    def color(field: str, value: str) -> str:
        if value[0] == "#":
            value = value[1:]
        if len(value) != 6 or any([char not in HEXDIGITS for char in value]):
            raise ValueError(f"Invalid HEX code in '{field}' field: '{value}'")
        return value.upper()

    @staticmethod
    def positive(field: str, value: int) -> int:
        if value < 0:
            raise ValueError(f"Invalid positive number in '{field}' field: '{value}'")
        return value

    @staticmethod
    def emoji(field: str, value: str) -> str:
        if value != "" and not is_emoji(value):
            raise ValueError(f"Invalid emoji in '{field}' field: '{value}'")
        return value
