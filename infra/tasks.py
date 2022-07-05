from celery import shared_task
from .models import health_check
import requests

@shared_task(name="health_check")
def healthCheckTask():
    health_check()