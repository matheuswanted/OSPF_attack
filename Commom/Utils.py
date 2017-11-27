import socket
# addr convert functions
def to_net_addr( addr):
    return socket.inet_pton(PROTOCOL, addr)
def to_mac_str( addr):
    return addr.replace(':', '').decode('hex')
def to_str_addr(addr):
    return socket.inet_ntop(PROTOCOL, addr)

# config
MAX_INT = 0xc0a80a05 #4294967295
PROTOCOL = socket.AF_INET

INTERFACE_NAME = 'enp3s0'

SRC_MAC = '84:7b:eb:e3:8a:ba'
SRC_IP = '10.32.143.234'


# attack config
NET_MASK = '255.255.255.0'
DST_MAC = 'c8:9c:1d:0e:0b:37'
DST_IP = '10.32.143.207'
KEEP_ALIVE_IP = '224.0.0.5'
KEEP_ALIVE_MAC = '01:00:5E:00:00:05'

#OSPF config
SEQUENCE_START = 268
BACKUP_ROUTER = 0x0a208faa
DST_ROUTER_ID = 0x0a208fcf #to_net_addr(DST_IP)
AREA_ID = 0
HELLO_INTERVAL = 10
DEAD_INTERVAL = 40
AUTH_TYPE = 0
AUTH = 0
