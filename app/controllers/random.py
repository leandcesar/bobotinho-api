# -*- coding: utf-8 -*-
import random

from app.api import HTTPStatus, api, request
from app.controllers import BaseController
from app.schemas.response import ResponseSchema

ns = api.namespace("random", description="Random", validate=True)
rand = ns.model("Random", ResponseSchema().as_model(), strict=True)


def random_line_from_text_file(filename: str, path: str = "app//data") -> str:
    with open(f"{path}//{filename}", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return random.choice(lines)


@ns.route("/joke")
class JokeController(BaseController):
    @ns.doc(description="Get some random joke")
    @ns.marshal_with(rand, envelope="data", code=HTTPStatus.OK.value, description="Random joke")
    def get(self):
        joke = {"response": random_line_from_text_file("jokes.txt")}
        joke_json = ResponseSchema(many=False).dump(joke)
        return joke_json, HTTPStatus.OK


@ns.route("/quote")
class QuoteController(BaseController):
    @ns.doc(description="Get some random quote")
    @ns.marshal_with(rand, envelope="data", code=HTTPStatus.OK.value, description="Random quote")
    def get(self):
        quote = {"response": random_line_from_text_file("quotes.txt")}
        quote_json = ResponseSchema(many=False).dump(quote)
        return quote_json, HTTPStatus.OK


@ns.route("/sadcat")
class CatController(BaseController):
    @ns.doc(description="Get some random sad cat")
    @ns.marshal_with(rand, envelope="data", code=HTTPStatus.OK.value, description="Random sad cat")
    def get(self):
        cat = {"response": "https://i.imgur.com/" + random_line_from_text_file("sadcats.txt")}
        cat_json = ResponseSchema(many=False).dump(cat)
        return cat_json, HTTPStatus.OK


@ns.route("/word")
class WordController(BaseController):
    @ns.doc(description="Get some random word")
    @ns.marshal_with(rand, envelope="data", code=HTTPStatus.OK.value, description="Random word")
    def get(self):
        word = {"response": random_line_from_text_file("words.txt")}
        word_json = ResponseSchema(many=False).dump(word)
        return word_json, HTTPStatus.OK
