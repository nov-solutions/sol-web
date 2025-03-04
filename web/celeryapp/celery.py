from __future__ import absolute_import, unicode_literals

from celery import Celery
from celeryapp import celery_config

app = Celery("web")

app.config_from_object(celery_config)
