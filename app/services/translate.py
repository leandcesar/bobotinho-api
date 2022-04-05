# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator


class TranslatorService:

    def translate(self, text: str, source: str = "auto", target: str = "pt") -> dict:
        return {"response": GoogleTranslator(source=source, target=target).translate(text)}
