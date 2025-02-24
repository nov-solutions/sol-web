from kombu import Exchange

from django.conf import settings

broker_url = f"redis://:{settings.REDIS_PASSWORD}@redis:6379/0"
result_backend = f"redis://:{settings.REDIS_PASSWORD}@redis:6379/0"
result_expires = 60 * 60 * 24  # 24 hours

task_default_queue = "default"
task_default_exchange_type = "topic"
task_default_routing_key = "default"
task_default_priority = 5

broker_connection_retry_on_startup = True
broker_connection_max_retries = 10

redbeat_redis_url = f"redis://:{settings.REDIS_PASSWORD}@redis:6379/1"

default_exchange = Exchange("default", type="topic")

task_queues = ()
