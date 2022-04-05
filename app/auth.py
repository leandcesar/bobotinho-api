# -*- coding: utf-8 -*-
from http import HTTPStatus
from typing import Optional

from flask_httpauth import HTTPTokenAuth

from app.config import config

auth = HTTPTokenAuth(scheme="Bearer", header="Authorization")


@auth.verify_token
def verify_token(token: str) -> Optional[str]:
    users = {config.AUTH_TOKEN: "admin"}
    return users.get(token)


@auth.error_handler
def default_error_handler(status: int) -> tuple[dict[str, str], HTTPStatus]:
    return {"message": "Unauthorized Access"}, HTTPStatus.UNAUTHORIZED
