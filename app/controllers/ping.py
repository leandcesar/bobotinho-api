# -*- coding: utf-8 -*-
from app.api import HTTPStatus, api
from app.controllers import BaseController

ns = api.namespace("ping", description="Ping")


@ns.route("/")
class PingController(BaseController):
    @ns.doc(description="Get ping")
    @ns.response(code=HTTPStatus.NO_CONTENT.value, description="Pong")
    def get(self):
        return "", HTTPStatus.NO_CONTENT
