from celery import shared_task
from .models import ApiKey, updateCache
import requests

@shared_task(name="get_keys")
def updateKeys():
    response = requests.get('https://livepeer.ftkuhnsman.com/api/f8991fcd-7d60-4e3c-8296-73227ac34bdd/keys/')
    data = response.json()
    
    for key in data:
        try:
            obj, created = ApiKey.objects.update_or_create(
                key = key['key'],
                defaults={'active':key['active'], 'override':key['override']},
                )
        except Exception as e:
            print(e)
            
    return data

@shared_task(name="update_cache")
def updateKeyCache():
    updateCache()
    print('cache updated', flush=True)