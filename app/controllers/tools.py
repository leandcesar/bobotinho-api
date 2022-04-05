# -*- coding: utf-8 -*-
from app import config
from app.api import HTTPStatus, api, request
from app.controllers import BaseController
from app.schemas.color import ColorSchema
from app.schemas.dictionary import DicioSchema
from app.schemas.response import ResponseSchema
from app.schemas.twitch import TwitchSchema
from app.schemas.weather import WeatherSchema
from app.services.color import ColorService
from app.services.currency import CurrencyService
from app.services.dictionary import DicioService
from app.services.math import MathService
from app.services.translate import TranslatorService
from app.services.twitch import TwitchService
from app.services.weather import WeatherService

ns = api.namespace("tools", description="Tools", validate=True)

color = ns.model("Color", ColorSchema().as_model(), strict=True)
color_parser = ns.parser()
color_parser.add_argument("hex", type=str, help="HEX code, '#' is optional", required=True)

currency = ns.model("Currency", ResponseSchema().as_model(), strict=True)
currency_parser = ns.parser()
currency_parser.add_argument("base", type=str, help="Requested exchange rate base asset", required=True)
currency_parser.add_argument("quote", type=str, help="Requested exchange rate quote asset", required=True)

dicio = ns.model("Dictionary", DicioSchema().as_model(), strict=True)
dicio_parser = ns.parser()
dicio_parser.add_argument("word", type=str, help="Word to get definition", required=True)

math = ns.model("Math", ResponseSchema().as_model(), strict=True)
math_parser = ns.parser()
math_parser.add_argument("expression", type=str, help="Expression to be evaluated", required=True)
math_parser.add_argument("precision", type=int, help="Number of significant digits in formatted output", default=4)

translate = ns.model("Translate", ResponseSchema().as_model(), strict=True)
translate_parser = ns.parser()
translate_parser.add_argument("text", type=str, help="Desired text to translate", required=True)
translate_parser.add_argument("source", type=str, help="Source language to translate from", default="auto")
translate_parser.add_argument("target", type=str, help="Target language to translate to", default="pt")

twitch = ns.model("Twitch", TwitchSchema().as_model(), strict=True)
twitch_parser = ns.parser()
twitch_parser.add_argument("channel", type=str, help="The channel Twitch username", required=True)
twitch_parser.add_argument("user", type=str, help="The user Twitch username (only required for 'followed' info)")
twitch_parser.add_argument(
    "infos",
    type=str,
    help="What informations do you want to know, separated by commas?",
    choices=("account_age", "avatar", "creation", "follow_age", "followed", "follows", "game", "id", "title", "total_views", "uptime", "viewers"),
    required=True,
)
twitch_parser.add_argument("language", type=str, help="Output language", default="pt")
twitch_parser.add_argument("precision", type=str, help="How precise the timestamp should be", default="3")
twitch_parser.add_argument("format", type=str, help="Formatting of the returned date and time", default="d/m/Y \\à\\s H:i:s")
twitch_parser.add_argument("timezone", type=str, help="Timezone for displaying date and time other than UTC", default="America/Sao_Paulo")

weather = ns.model("Weather", WeatherSchema().as_model(), strict=True)
weather_parser = ns.parser()
weather_parser.add_argument("location", type=str, help="City name, state code and country code, separated by commas", required=True)
weather_parser.add_argument("language", type=str, help="Output language", default="pt")
weather_parser.add_argument("units", type=str, help="Units of measurement", choices=("standard", "metric", "imperial"), default="metric")


@ns.route("/color")
class ColorController(BaseController):
    @ns.doc(description="Get information about any color")
    @ns.marshal_with(color, envelope="data", code=HTTPStatus.OK.value, description="Color information")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="Invalid color")
    @ns.expect(color_parser)
    def get(self):
        color = ColorService().by_hex(**request.args)
        color_json = ColorSchema(many=False).dump(color)
        return color_json, HTTPStatus.OK


@ns.route("/currency")
class CurrencyController(BaseController):
    @ns.doc(description="Get the exchange rate between pair of requested assets")
    @ns.marshal_with(currency, envelope="data", code=HTTPStatus.OK.value, description="Exchange rate")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="Invalid asset")
    @ns.expect(currency_parser)
    def get(self):
        currency = CurrencyService(config.CURRENCY_API_KEY).rate(**request.args)
        currency_json = ResponseSchema(many=False).dump(currency)
        return currency_json, HTTPStatus.OK


@ns.route("/dicionary")
class DicioController(BaseController):
    @ns.doc(description="Get the dictionary definition of a word")
    @ns.marshal_with(dicio, envelope="data", code=HTTPStatus.OK.value, description="Word definition")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="Word not found")
    @ns.expect(dicio_parser)
    def get(self):
        dicio = DicioService().definition(**request.args)
        dicio_json = DicioSchema(many=False).dump(dicio)
        return dicio_json, HTTPStatus.OK


@ns.route("/math")
class MathController(BaseController):
    @ns.doc(description="Get the result of a mathematical expression")
    @ns.marshal_with(math, envelope="data", code=HTTPStatus.OK.value, description="Expression result")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="Invalid expression")
    @ns.expect(math_parser)
    def get(self):
        math = MathService().evaluate(**request.args)
        math_json = ResponseSchema(many=False).dump(math)
        return math_json, HTTPStatus.OK


@ns.route("/translate")
class TranslateController(BaseController):
    @ns.doc(description="Translate a text")
    @ns.marshal_with(translate, envelope="data", code=HTTPStatus.OK.value, description="Translated text")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="Invalid language")
    @ns.expect(translate_parser)
    def get(self):
        translate = TranslatorService().translate(**request.args)
        translate_json = ResponseSchema(many=False).dump(translate)
        return translate_json, HTTPStatus.OK


@ns.route("/twitch")
class TwitchController(BaseController):
    @ns.doc(description="Get Twitch information about a channel")
    @ns.marshal_with(twitch, envelope="data", code=HTTPStatus.OK.value, description="Twitch channel information")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="Invalid info requested or channel not found")
    @ns.expect(twitch_parser)
    def get(self):
        twitch = TwitchService().fetch(**request.args)
        twitch_json = TwitchSchema(many=False).dump(twitch)
        return twitch_json, HTTPStatus.OK


@ns.route("/weather")
class WeatherController(BaseController):
    @ns.doc(description="Get the current weather data for any location")
    @ns.marshal_with(weather, envelope="data", code=HTTPStatus.OK.value, description="Current weather")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="Location not found")
    @ns.expect(weather_parser)
    def get(self):
        weather = WeatherService(config.WEATHER_API_KEY).by_location(**request.args)
        weather_json = WeatherSchema(many=False).dump(weather)
        return weather_json, HTTPStatus.OK
