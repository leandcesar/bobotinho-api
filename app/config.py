# -*- coding: utf-8 -*-
from os import environ, path, urandom
from urllib.parse import urlparse


class Config(object):
    VERSION = environ.get("VERSION")

    # Flask
    FLASK_APP = environ.get("FLASK_APP", "__main__.py")
    SECRET_KEY = environ.get("SECRET_KEY", urandom(24))
    ERROR_INCLUDE_MESSAGE = bool(environ.get("ERROR_INCLUDE_MESSAGE", False))
    ENV = FLASK_ENV = environ.get("ENV", "dev")
    AUTH_TOKEN = environ.get("AUTH_TOKEN", "secret")

    if ENV == "prod":
        DEBUG = FLASK_DEBUG = DEBUG_TB_ENABLED = SQLALCHEMY_ECHO = False
        TESTING = False
        SQLALCHEMY_DATABASE_URI = DATABASE_URL = environ.get("DATABASE_URL")
        CSRF_ENABLED = True
    elif ENV == "test":
        DEBUG = FLASK_DEBUG = DEBUG_TB_ENABLED = SQLALCHEMY_ECHO = True
        TESTING = True
        SQLALCHEMY_DATABASE_URI = DATABASE_URL = "sqlite:///:memory:"
    elif ENV == "dev":
        DEBUG = FLASK_DEBUG = DEBUG_TB_ENABLED = SQLALCHEMY_ECHO = True
        TESTING = False
        SQLALCHEMY_DATABASE_URI = DATABASE_URL = f"sqlite:///{path.abspath(path.dirname(__file__))}/../db.sqlite3"
    else:
        raise ValueError(f"Invalid ENV value, expected 'prod', 'dev' or 'test', not '{ENV}'")

    # Flask-Caching
    # TODO: https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching
    CACHE_DEFAULT_TIMEOUT = int(environ.get("CACHE_DEFAULT_TIMEOUT", 300))
    CACHE_IGNORE_ERRORS = bool(environ.get("CACHE_IGNORE_ERRORS", False))
    CACHE_THRESHOLD = int(environ.get("CACHE_THRESHOLD", 500))
    CACHE_KEY_PREFIX = environ.get("CACHE_KEY_PREFIX", "flask_cache_")
    CACHE_TYPE = environ.get("CACHE_TYPE", "SimpleCache")

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False))

    # Flask-Limiter
    RATELIMIT_ENABLED = bool(environ.get("RATELIMIT_ENABLED", True))
    RATELIMIT_APPLICATION = environ.get("RATELIMIT_APPLICATION", "1000/minute, 10000/hour")
    RATELIMIT_DEFAULT = environ.get("RATELIMIT_DEFAULT", "100/minute, 1000/hour")
    RATELIMIT_DEFAULTS_PER_METHOD = bool(environ.get("RATELIMIT_DEFAULTS_PER_METHOD", True))
    RATELIMIT_HEADERS_ENABLED = bool(environ.get("RATELIMIT_HEADERS_ENABLED", True))
    RATELIMIT_STORAGE_URI = environ.get("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_KEY_PREFIX = environ.get("RATELIMIT_KEY_PREFIX", "flask_limiter_")

    # Celery
    CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = environ.get("CELERY_RESULT_BACKEND")
    CELERY_CONCURRENCY = environ.get("CELERY_CONCURRENCY", 4)
    CELERY_LOG_LEVEL = environ.get("CELERY_LOG_LEVEL", "WARNING")

    # Bugsnag
    BUGSNAG_API_KEY = environ.get("BUGSNAG_API_KEY")
    BUGSNAG_APP_TYPE = environ.get("BUGSNAG_APP_TYPE")
    BUGSNAG_ASYNCHRONOUS = bool(environ.get("BUGSNAG_ASYNCHRONOUS", True))
    BUGSNAG_NOTIFY_RELEASE_STAGES = environ.get("BUGSNAG_NOTIFY_RELEASE_STAGES")
    BUGSNAG_PARAMS_FILTERS = environ.get("BUGSNAG_PARAMS_FILTERS")

    # Rollbar
    ROLLBAR_ACCESS_TOKEN = environ.get("ROLLBAR_ACCESS_TOKEN")
    ROLLBAR_INCLUDE_REQUEST_BODY = bool(environ.get("ROLLBAR_INCLUDE_REQUEST_BODY", True))

    # Sentry
    SENTRY_DNS = environ.get("SENTRY_DNS")
    SENTRY_SAMPLE_RATE = float(environ.get("SENTRY_SAMPLE_RATE", 1.0))
    SENTRY_REQUEST_BODIES = environ.get("SENTRY_REQUEST_BODIES", "medium")
    SENTRY_WITH_LOCALS = bool(environ.get("SENTRY_WITH_LOCALS"))

    # Moesif
    MOESIF_APP_ID = environ.get("MOESIF_APP_ID")
    MOESIF_LOG_BODY = bool(environ.get("MOESIF_LOG_BODY", True))

    # APIs
    CURRENCY_API_KEY = environ.get("API_KEY_CURRENCY")
    WEATHER_API_KEY = environ.get("API_KEY_WEATHER")


config = Config()
