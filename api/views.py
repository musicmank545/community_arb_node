from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import updateCache, ApiKey
from infra.models import Node
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from .metrics import *
import json
import traceback
from requests.adapters import HTTPAdapter, Retry
from django.conf import settings
from django.http import JsonResponse



eth_rpc_url = 'http://154.53.49.145:8088'

@csrf_exempt
@never_cache
def test(request,apikey):
    if apikey == settings.MASTER_KEY:
        keys = list(ApiKey.objects.all().values())
        return JsonResponse(keys, safe=False)
    else:
        return HttpResponse('Fail', status=305)

@csrf_exempt
@never_cache
def arb(request,apikey):
    body=request.body.decode("utf-8")
    keys = cache.get('keys')
    arb_rpc_url = cache.get('activeNode')
    
    if arb_rpc_url is None:
        arb_rpc_url = Node.objects.get(default=True).url
        cache.set('activeNode',arb_rpc_url,)
        print('updateActiveNodeCache')
    
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
            print(body, flush=True)
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
        
        
@csrf_exempt
@never_cache
def health(request):
    print('cloudflare health checked', flush=True)
    return HttpResponse(cache.get('health'))