# -*- coding: utf-8 -*-
from flask import Flask

from app.api import api
from app.cache import cache
from app.config import config
from app.controllers import ping, tools
from app.database import db
from app.limiter import limiter
from app.marshmallow import ma
from app.migrate import migrate
from app.monitor import monitor
from app.tasks import tasks


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    api.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    monitor.init_app(app)
    tasks.init_app(app)

    app.before_first_request(db.create_all)

    return app
