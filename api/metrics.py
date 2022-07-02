from prometheus_client import Counter
from prometheus_client import Gauge


#initialise a prometheus counter
class Metrics:
    requests_by_key = Counter('requests_by_key', 'count of requests for each API key',['key','host'])
    requests_by_rpc_method = Counter('requests_by_rpc_method', 'count of requests for each rpc method type',['method',])
    requests_invalid = Counter('requests_invalid', 'count of invalid requests')
    requests_inactive = Counter('requests_inactive', 'count of requests with inactive keys')
    requests_key_invalid = Counter('requests_key_invalid', 'count of requests with invalid keys')
    stripe = Counter('stripe', 'stripe',['value',])