from prometheus_client import Summary
from prometheus_client import Gauge
from prometheus_client import Info
from prometheus_client import Counter

#initialise a prometheus counter
class Metrics:
    node_block_height = Gauge('node_block_height','Blockheight of all nodes',['name','url',])
    current_health = Counter('local_health', 'Health of this node')
    current_active_node = Info('current_active_node', 'Current arb node serving requests')