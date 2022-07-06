from django.db import models
from django.core.cache import cache
import requests
import json
import time
from threading import Thread, Event
from .metrics import *



# Create your models here.
class Node(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    port = models.CharField(max_length=250, default='8547')
    currentBlockHeight = models.IntegerField()
    healthy = models.BooleanField()
    default = models.BooleanField()
    
    @property
    def url(self):
        return str('http://{}:{}').format(self.address,self.port)

'''   
def health_check():
    blockHeights = []
    blockHeights.append(get_arbiscan_block_height())
    
    nodes = Node.objects.all()
    for node in nodes:
        print(node.name)
        block = get_block_height(address=node.address, port=node.port)
        node.currentBlockHeight = block 
        node.save()
        blockHeights.append(block)
    
    maxHeight = max(blockHeights)
    for node in nodes:
        delta = maxHeight - node.currentBlockHeight
        print(delta)
        if delta > 20:
            node.healthy = False
        else:
            node.healthy = True
        node.save()
'''

def get_block_height(address='127.0.0.1',port='8547'):
        url = 'http://{}:{}'.format(address,port)
        headers = {'Content-type': 'application/json'}
        data = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":0}'
        
        try:
            with requests.post(url,headers=headers,data=data,timeout=3) as r:
                data = r.json()
                block = int(data['result'], 16)
                return block
        except:
            return -1
    
def get_arbiscan_block_height():
    t = time.time()
    int_t=round(t)
    url = 'https://api.arbiscan.io/api?module=block&action=getblocknobytime&timestamp={}&closest=before&apikey=S3V1I8BMFPZ9CHJT2XRR6Q1S256GAUIN25'.format(str(int_t))
    try:
        r = requests.get(url,timeout=5)
        data = r.json()
        return int(data['result'])
    except:
        return None
    
def health_check_thread(node,blockHeights):
    print(node.name)
    block = get_block_height(address=node.address, port=node.port)
    node.currentBlockHeight = block 
    node.save()
    blockHeights.append(block)
    
        
def health_check():
    print('Checking node health', flush=True)
    threads = []
    blockHeights = []
    nodeNames = []
    blockHeights.append(get_arbiscan_block_height())
    
    nodes = Node.objects.all()
    for node in nodes:
        threads.append(Thread(target=health_check_thread, args=(node,blockHeights,)))
        
    for t in threads:
        t.start()
        t.join()
    print(blockHeights)
    
    maxHeight = max(blockHeights)
    for node in nodes:
        delta = maxHeight - node.currentBlockHeight
        print(delta)
        if delta > 20:
            node.healthy = False
        else:
            node.healthy = True
        node.save()
  
    actives = nodes.filter(healthy=True)
    default = actives.filter(default=True).first()
    
    if default is not None:
        cache.set('activeNode',default.url,)
        cache.set('health','good',)
        print('Node is Healthy')
    else:
        cache.set('health','bad',)
        print('Node is Unhealthy')
        
        highest = actives.order_by('-currentBlockHeight').first()
        if highest is not None:
            cache.set('activeNode',highest.url)
        else:
            cache.set('activeNode',default.url)
    
    
    