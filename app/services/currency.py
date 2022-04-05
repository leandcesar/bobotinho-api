# -*- coding: utf-8 -*-
from app.services import BaseService


class CurrencyService(BaseService):
    url = "https://rest.coinapi.io/v1"

    def __init__(self, api_key: str) -> None:
        self.headers = {"x-coinapi-key": api_key}

    def rate(self, base: str, quote: str) -> dict:
        url = f"{self.url}/exchangerate/{base.upper()}/{quote.upper()}"
        data = self.http_get(url, headers=self.headers)
        return {"response": str(data["rate"])}
