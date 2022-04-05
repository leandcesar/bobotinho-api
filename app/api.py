# -*- coding: utf-8 -*-
from http import HTTPStatus

from flask import request
from flask_restx import Api, Resource, fields
from sqlalchemy.exc import CompileError, IntegrityError, NoResultFound
from requests.exceptions import HTTPError, JSONDecodeError


api = Api(
    version="1.0",
    title="Bobotinho API",
    description="Bobotinho API for Bobotinho Twitch bot",
    validate=True,
    security=["Bearer"],
    authorizations={"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}},
    serve_challenge_on_401=True,
)


@api.errorhandler(ValueError)
def handle_validation_error(error: ValueError) -> tuple[dict[str, str], int]:
    return {"message": str(error)}, HTTPStatus.BAD_REQUEST


@api.errorhandler(CompileError)
def handle_compile_error(error: CompileError) -> tuple[dict[str, str], int]:
    return {"message": str(error)}, HTTPStatus.BAD_REQUEST


@api.errorhandler(IntegrityError)
def handle_integrity_error(error: IntegrityError) -> tuple[dict[str, str], int]:
    return {"message": str(error.orig)}, HTTPStatus.CONFLICT


@api.errorhandler(NoResultFound)
def handle_no_result_error(error: NoResultFound) -> tuple[dict[str, str], int]:
    return {"message": str(error)}, HTTPStatus.UNPROCESSABLE_ENTITY


@api.errorhandler(HTTPError)
def handle_http_error(error: HTTPError) -> tuple[dict[str, str], int]:
    try:
        data = error.response.json()
        if "message" in data:
            data = {"message": data["message"].capitalize()}
        if "error" in data:
            data = {"message": data["error"].capitalize()}
        return data, HTTPStatus.BAD_REQUEST
    except Exception:
        return {"message": str(error)}, HTTPStatus.BAD_REQUEST


@api.errorhandler
def default_error_handler(error) -> tuple[dict[str, str], int]:
    return {"message": str(error)}, getattr(error, "code", HTTPStatus.INTERNAL_SERVER_ERROR)
