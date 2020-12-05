import requests
from .models import Call
from celery import shared_task

@shared_task
def update_model(url, instance_id):
    print('TASK RUNNING')
    instance = Call.objects.get(id=instance_id)
    try:
        r = requests.get(url)
        response = r.json()
        instance.response = response
    except:
        instance.response = 'No response received.'
    instance.processed = True
    instance.save()