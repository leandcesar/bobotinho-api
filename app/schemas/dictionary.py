# -*- coding: utf-8 -*-
from app.marshmallow import fields
from app.schemas import BaseSchema


class DicioSchema(BaseSchema):
    class Meta:
        fields = (
            "word",
            "word_class",
            "meaning",
            "etymology",
            "synonyms",
        )

    word = fields.String(allow_none=True, description="Word")
    word_class = fields.String(allow_none=True, description="Word grammatical class")
    meaning = fields.String(allow_none=True, description="Meaning of the word")
    etymology = fields.String(allow_none=True, description="Etymology of the word")
    synonyms = fields.String(allow_none=True, description="Synonyms of the word")
