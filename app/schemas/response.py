# -*- coding: utf-8 -*-
from app.marshmallow import fields
from app.schemas import BaseSchema


class ResponseSchema(BaseSchema):
    class Meta:
        fields = (
            "response",
        )

    response = fields.String(allow_none=True)
