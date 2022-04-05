# -*- coding: utf-8 -*-
from celery import Celery, Task
from flask import Flask


class Tasks(Celery):
    def __init__(self, app: Flask = None, config: dict = None) -> None:
        super().__init__()

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

        celery_broker_url = config.get("CELERY_BROKER_URL")
        celery_backend_url = config.get("CELERY_RESULT_BACKEND")
        celery_concurrency = config.get("CELERY_CONCURRENCY")
        celery_log_level = config.get("CELERY_LOG_LEVEL")

        if celery_broker_url:
            self.conf.update(
                main=app.import_name,
                broker=celery_broker_url,
                backend=celery_backend_url,
                worker_concurrency=celery_concurrency,
                worker_redirect_stdouts_level=celery_log_level,
            )

            class ContextTask(Task):
                def __call__(self, *args, **kwargs):
                    with app.app_context():
                        return self.run(*args, **kwargs)

            self.Task = ContextTask


tasks = Tasks()
