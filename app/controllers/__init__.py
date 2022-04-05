# -*- coding: utf-8 -*-
from app.api import HTTPStatus, Resource, api
from app.auth import auth


@api.response(code=HTTPStatus.UNAUTHORIZED.value, description="Unauthorized access")
class BaseController(Resource):
    method_decorators = [auth.login_required]
