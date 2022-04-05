# -*- coding: utf-8 -*-
from app.services import BaseService


class MathService(BaseService):
    url = "https://api.mathjs.org/v4"

    def evaluate(self, expression: str, precision: int = 4) -> dict:
        payload = {
            "expr": expression,
            "precision": precision,
        }
        data = self.http_post(self.url, json=payload)
        return {"response": data["result"]}
