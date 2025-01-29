from django.conf import settings
from kombu import Exchange, Queue

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

task_queues = (
    Queue("default", exchange=default_exchange, routing_key="default"),
    Queue("page_visits", exchange=default_exchange, routing_key="page_visits"),
    Queue("duration", exchange=default_exchange, routing_key="duration"),
    Queue("data_ingress", exchange=default_exchange, routing_key="data_ingress"),
    Queue("data_egress", exchange=default_exchange, routing_key="data_egress"),
)
