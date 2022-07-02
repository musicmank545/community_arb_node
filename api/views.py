from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.template import loader
from django.http import Http404
from django.urls import reverse
from .models import *
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import ApiKey, updateCache
from django.core.cache import cache, caches
from django.views.decorators.cache import never_cache
from .metrics import *
import json
import traceback
from django.http import JsonResponse
from requests.adapters import HTTPAdapter, Retry

#arb_rpc_url = 'http://154.53.49.145:8080'
eth_rpc_url = 'http://154.53.49.145:8088'

arb_rpc_url = 'http://66.94.101.120:8547'


#from web3 import HTTPProvider
#from ens import ENS
#from django.core import serializers
#from rest_framework import viewsets
#from .serializers import *

# Create your views here.

#@silk_profile(name='API Call')

@csrf_exempt
@never_cache
def arb(request,apikey):
    body=request.body.decode("utf-8")
    keys = cache.get('keys')
    
    if keys is None:
        updateCache()
        keys = cache.get('keys')
        print('updateCache')
        
    session = cache.get('session')
    if session is None:
        session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.1,)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        cache.set('session',session)
        print('refreshed session cache')
    
    rpc_headers = {'Content-Type': request.content_type}
    try:
        key = keys.get(apikey)
        if key is None:
            return HttpResponse('API Key is not valid', status=300)
    except: #ApiKey.DoesNotExist:
        traceback.print_exc()
        return HttpResponse('Error looking up API key', status=300)
    
    if key['active'] or key['override']:        
        try:
            #prom_data = json.loads(request.body)
            Metrics.requests_by_key.labels(apikey,request.META.get('HTTP_X_FORWARDED_FOR')).inc()
            #Metrics.requests_by_rpc_method.labels(prom_data['method']).inc()
            #Metrics.requests_by_rpc_method.labels(prom_data).inc()
            '''
            lookup = hash(str(prom_data))
            egbb = cache.get(str(lookup))
            print("Request_Body",str(prom_data))
            if egbb is None:
                response = requests.post(arb_rpc_url,data=request,headers=rpc_headers)
                cache.set(str(lookup),response.content,10)
                print('New Content',response.content)
                
                return HttpResponse(response.content)
            else:
                print('served from cache')
                
                print('cached content',egbb)
                return HttpResponse(egbb)
            '''
            response = session.post(arb_rpc_url,data=body,headers=rpc_headers,timeout=10)

            return HttpResponse(response.content)
        except Exception:
            traceback.print_exc()
            for x,y in request.META.items():
                print(x,y)
            print(body)
            Metrics.requests_invalid.inc()
            return HttpResponse('Invalid RPC request', status=300)
    else:
        Metrics.requests_inactive.inc()
        return HttpResponse('API Key is not active', status=300)

@csrf_exempt
@never_cache
def eth(request,apikey):
    keys = cache.get('keys')
    if keys is None:
        updateCache()
        keys = cache.get('keys')
        print('updateCache')
    
    rpc_headers = {'Content-Type': request.content_type}
    try:
        key = keys.get(apikey)
        if key is None:
            return HttpResponse('API Key is not valid')
    except: #ApiKey.DoesNotExist:
        traceback.print_exc()
        return HttpResponse('Error looking up API key', status=300)
    
    if key['active'] or key['override']:        
        try:
            response = requests.post(eth_rpc_url,data=request,headers=rpc_headers,timeout=10)
            return HttpResponse(response.content)
        except Exception:
            traceback.print_exc()
            return HttpResponse('Invalid RPC request',status=300)
    else:
        return HttpResponse('API Key is not active', status=300)
        print('error')