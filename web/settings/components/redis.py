import os

REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "solsecretpassredis")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
