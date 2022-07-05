from django.db import models
from django.core.cache import cache

# Create your models here.
class ApiKey(models.Model):
    key = models.CharField(max_length=250, primary_key=True)
    active = models.BooleanField()
    override = models.BooleanField()

def updateCache():
    
    res = {}
    keys = list(ApiKey.objects.all().values())
    
    for k in keys:
        res[k['key']] = k
    #cache.clear()
    cache.set('keys',res,300)