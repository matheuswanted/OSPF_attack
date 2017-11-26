import socket
# config
MAX_INT = 4294967295
PROTOCOL = socket.AF_INET

INTERFACE_NAME = 'wlp2s0'

SRC_MAC = '68:14:01:a6:42:8d'
SRC_IP = '192.168.0.5'


# attack config
NET_MASK = '255.255.255.0'
DST_MAC = '00:00:00:00:00:00'
DST_IP = '192.168.0.1'

#OSPF config
SEQUENCE_START = 256
DST_ROUTER_ID = 0
AREA_ID = 1
HELLO_INTERVAL = 0
DEAD_INTERVAL = 0
AUTH_TYPE = 0
AUTH = 0

# addr convert functions
def to_net_addr( addr):
    return socket.inet_pton(PROTOCOL, addr)
def to_mac_str( addr):
    return addr.replace(':', '').decode('hex')
def to_str_addr(addr):
    return socket.inet_ntop(PROTOCOL, addr)
