# -*- coding: utf-8 -*-
from app.marshmallow import fields
from app.schemas import BaseSchema


class ColorSchema(BaseSchema):
    class Meta:
        fields = (
            "name",
            "hex",
            "rgb",
            "hsl",
            "hsv",
            "cmyk",
            "xyz",
            "contrast",
        )

    name = fields.String(allow_none=True, description="Color name")
    hex = fields.String(allow_none=True, description="HEX code color, like #123ABC")
    rgb = fields.String(allow_none=True, description="RGB code color, like rgb(18, 52, 86)")
    hsl = fields.String(allow_none=True, description="HSL code color, like hsl(210, 65%, 20%)")
    hsv = fields.String(allow_none=True, description="HSV code color, like hsv(210, 79%, 34%)")
    cmyk = fields.String(allow_none=True, description="CMYK code color, like cmyk(79, 40, 0, 66)")
    xyz = fields.String(allow_none=True, description="XYZ code color, like XYZ(16, 19, 35)")
    contrast = fields.String(allow_none=True, description="Contrast color")
