# -*- coding: utf-8 -*-
from flask import Flask


def init_bugsnag(app: Flask, config: dict) -> None:
    if config.get("BUGSNAG_API_KEY"):

        import bugsnag
        from bugsnag.flask import handle_exceptions

        env = config.get("ENV")
        version = config.get("VERSION")
        bugsnag_api_key = config.get("BUGSNAG_API_KEY")
        bugsnag_app_type = config.get("BUGSNAG_APP_TYPE")
        bugsnag_asynchronous = config.get("BUGSNAG_ASYNCHRONOUS")
        bugsnag_notify_release_stages = config.get("BUGSNAG_NOTIFY_RELEASE_STAGES")
        bugsnag_params_filters = config.get("BUGSNAG_PARAMS_FILTERS")
        if isinstance(bugsnag_notify_release_stages, str):
            bugsnag_notify_release_stages = bugsnag_notify_release_stages.split(",")
        if isinstance(bugsnag_params_filters, str):
            bugsnag_params_filters = bugsnag_params_filters.split(",")
        bugsnag.configure(
            api_key=bugsnag_api_key,
            release_stage=env,
            app_version=version,
            app_type=bugsnag_app_type,
            asynchronous=bugsnag_asynchronous,
            notify_release_stages=bugsnag_notify_release_stages,
            params_filters=bugsnag_params_filters,
        )
        handle_exceptions(app)


def init_rollbar(app: Flask, config: dict) -> None:
    if config.get("ROLLBAR_ACCESS_TOKEN"):

        import rollbar
        import rollbar.contrib.flask
        from flask import got_request_exception

        env = config.get("ENV")
        version = config.get("VERSION")
        rollbar_access_token = config.get("ROLLBAR_ACCESS_TOKEN")
        rollbar_include_request_body = config.get("ROLLBAR_INCLUDE_REQUEST_BODY")
        rollbar.init(
            access_token=rollbar_access_token,
            environment=env,
            code_version=version,
            include_request_body=rollbar_include_request_body,
        )
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


def init_sentry(app: Flask, config: dict) -> None:
    if config.get("SENTRY_DNS"):

        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        env = config.get("ENV")
        version = config.get("VERSION")
        sentry_dsn = config.get("SENTRY_DNS")
        sentry_sample_rate = config.get("SENTRY_SAMPLE_RATE")
        sentry_request_bodies = config.get("SENTRY_REQUEST_BODIES")
        sentry_with_locals = config.get("SENTRY_WITH_LOCALS", True)
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=env,
            release=version,
            integrations=[FlaskIntegration()],
            with_locals=sentry_with_locals,
            traces_sample_rate=sentry_sample_rate,
        )


def init_moesif(app: Flask, config: dict) -> None:
    if config.get("MOESIF_APP_ID"):

        from moesifwsgi import MoesifMiddleware

        moesif_app_id = config.get("MOESIF_APP_ID")
        moesif_log_body = config.get("MOESIF_LOG_BODY")
        moesif_settings = dict(APPLICATION_ID=moesif_app_id, LOG_BODY=moesif_log_body)
        app.wsgi_app = MoesifMiddleware(app.wsgi_app, moesif_settings)


def init_prometheus(app: Flask, config: dict) -> None:

    from prometheus_flask_exporter import PrometheusMetrics

    PrometheusMetrics(app)


class Monitor:
    def __init__(self, app: Flask = None, config: dict = None) -> None:
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")

        self.config = config

        if app is not None:
            self.init_app(app, config)

    def init_app(self, app: Flask, config: dict = None) -> None:
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")

        base_config = app.config.copy()
        if self.config:
            base_config.update(self.config)
        if config:
            base_config.update(config)
        config = base_config

        init_bugsnag(app, config)
        init_rollbar(app, config)
        init_sentry(app, config)
        init_moesif(app, config)
        init_prometheus(app, config)


monitor = Monitor()
