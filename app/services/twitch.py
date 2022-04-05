# -*- coding: utf-8 -*-
from app.services import BaseService
from app.validators import Validator

ENDPOINTS = {
    "account_age": "accountage",
    "creation": "creation",
    "follow_age": "followage",
    "followed": "followed",
    "avatar": "avatar",
    "follows": "followcount",
    "id": "id",
    "total_views": "total_views",
    "title": "title",
    "game": "game",
    "uptime": "uptime",
    "viewers": "viewercount",
}
ERRORS = (
    "Ocorreu um erro",
    "dados inválidos",
    "Não foi possível",
)


class TwitchService(BaseService):
    url = "https://www.decapi.me/twitch"

    def fetch(
        self,
        infos: str,
        channel: str,
        user: str = "",
        language: str = "pt",
        precision: str = "3",
        format: str = "d/m/Y \\à\\s H:i:s",
        timezone: str = "America/Sao_Paulo",
    ) -> dict:
        params = {
            "lang": language,
            "precision": precision,
            "format": format,
            "tz": timezone,
        }
        data = {}
        channel = Validator.username(channel)
        for info in infos.split(","):
            if info not in ENDPOINTS:
                continue
            endpoint = ENDPOINTS[info]
            if endpoint in ("follow_age", "followed"):
                user = Validator.username(user)
                url = f"{self.url}/{endpoint}/{channel}/{user}"
            else:
                url = f"{self.url}/{endpoint}/{channel}"
            response = str(self.http_get(url, params=params, res_type="text"))
            if any(e in response for e in ERRORS):
                raise ValueError(response)
            data[info] = int(response) if response.isdigit() else response
        return data
