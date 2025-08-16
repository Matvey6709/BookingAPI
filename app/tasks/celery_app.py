from celery import Celery
from app.config import s


celery_app = Celery(
    'tasks',
    broker=f'redis://{s.REDIS_HOST}:{s.REDIS_PORT}/',
    # backend='redis://{s.REDIS_HOST}:{s.REDIS_PORT}/',
    include=['app.tasks.tasks']
)
