import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_backend.settings")

app = Celery("shop_backend", broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"))

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()