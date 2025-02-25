from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celeryapp import celery_config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery("web")

app.config_from_object(celery_config)
