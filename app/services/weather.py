# -*- coding: utf-8 -*-
from app.services import BaseService

CODE_EMOJI = {
    "01d": "🌞",
    "02d": "🌤",
    "03d": "☁️",
    "04d": "🌥",
    "09d": "🌧",
    "10d": "🌦",
    "11d": "⛈",
    "13d": "🌨",
    "50d": "🌫",
    "01n": "🌙",
    "02n": "🌤",
    "03n": "☁️",
    "04n": "🌥",
    "09n": "🌧",
    "10n": "🌦",
    "11n": "⛈",
    "13n": "🌨",
    "50n": "🌫",
}


def code_to_emoji(code: str) -> str:
    return CODE_EMOJI[code]


def normalize_dict(data: dict) -> dict:
    if "all" in data:
        data["clouds"] = data.pop("all")
    if "feels_like" in data:
        data["temp_feels_like"] = data.pop("feels_like")
    if "icon" in data:
        data["emoji"] = code_to_emoji(data.pop("icon"))
    return data


def flatten_dict(data: dict) -> dict:
    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            new_data = {**value, **new_data}  # NOTE: will overwrites fields with the same name
        elif isinstance(value, list):
            new_data = {**value[0], **new_data}  # NOTE: will overwrites fields with the same name
        else:
            new_data[key] = value
    return new_data


class WeatherService(BaseService):
    url = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def by_location(self, location: str, language: str = "pt_br", units: str = "metric") -> dict:
        params = {
            "appid": self.api_key,
            "lang": language,
            "units": units,
            "q": location,
        }
        if params["lang"] == "pt":
            params["lang"] = "pt_br"
        data = self.http_get(self.url, params=params)
        data = flatten_dict(data)
        data = normalize_dict(data)
        return data
