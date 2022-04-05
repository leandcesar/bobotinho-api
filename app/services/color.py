# -*- coding: utf-8 -*-
from app.services import BaseService
from app.validators import Validator


def normalize_dict(data: dict) -> dict:
    return {
        "cmyk": data["cmyk"]["value"],
        "contrast": data["contrast"]["value"],
        "hex": data["hex"]["value"],
        "hsl": data["hsl"]["value"],
        "hsv": data["hsv"]["value"],
        "name": data["name"]["value"],
        "rgb": data["rgb"]["value"],
        "xyz": data["XYZ"]["value"],
    }


class ColorService(BaseService):
    url = "https://www.thecolorapi.com"

    def by_hex(self, hex: str) -> dict:
        color = Validator.color(hex)
        params = {"hex": color}
        data = self.http_get(f"{self.url}/id", params=params)
        data = normalize_dict(data)
        return data
