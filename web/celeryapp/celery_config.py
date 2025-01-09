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
    Queue("core_highmem", exchange=default_exchange, routing_key="core.highmem.#"),
    Queue("core_longrun", exchange=default_exchange, routing_key="core.longrun.#"),
    Queue(
        "core_spot_routine",
        exchange=default_exchange,
        routing_key="core.spot.routine.#",
    ),
    Queue("core_quick", exchange=default_exchange, routing_key="core.quick.#"),
)
