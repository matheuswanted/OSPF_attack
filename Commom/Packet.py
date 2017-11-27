import socket
import sys
from Utils import MAX_INT
from struct import *
from ConnectionInfo import *


class Ethernet:
    def __init__(self):
        self.src = None
        self.dst = None
        self.eth_type = 0x0800  # ipv4

    def setSrc(self, src):
        self.src = src

    def setDst(self, dst):
        self.dst = dst

    def pack(self):
        return pack('!6s6sH', self.dst, self.src, self.eth_type)

    def unpack(self, data):
        self.dst, self.src, self.eth_type = unpack("!6s6sH", data)


class IPV4:
    def __init__(self):
        self.version_ihl = (4 << 4) + 5
        self.tos = 0
        self.total_length = 20
        self.identification = 0
        self.flags_fragment_offset = 0
        self.ttl = 1
        self.protocol = 89  # ospf fixed
        self.checksum = 0
        self.src_addr = None
        self.dst_addr = None
        self.structure = '!BBHHHBBH4s4s'

    def setSrc(self, addr):
        self.src_addr = addr

    def setDst(self, addr):
        self.dst_addr = addr

    def pack(self):
        print (self.structure, self.version_ihl, self.tos, self.total_length,
                    self.identification, self.flags_fragment_offset, self.ttl, self.protocol,
                    self.checksum, self.src_addr, type(self.src_addr), self.dst_addr)
        return pack(self.structure, self.version_ihl, self.tos, self.total_length,
                    self.identification, self.flags_fragment_offset, self.ttl, self.protocol,
                    self.checksum, self.src_addr, self.dst_addr)

    def unpack(self, data):
        self.version_ihl, self.tos, self.total_length, self.identification, self.flags_fragment_offset, self.ttl, self.protocol, self.checksum, self.src_addr, self.dst_addr = unpack(
            self.structure, data)


class OSPF_Header:
    def __init__(self):
        self.version = 2
        self.type = 1
        self.length = 0
        self.router_id = MAX_INT
        self.area_id = 0
        self.checksum = 0
        self.auth_type = 0
        self.auth = 0
        self.structure = '!BBHIIHHQ'

    def pack(self):
        return pack(self.structure, self.version, self.type, self.length, self.router_id,
                    self.area_id, self.checksum, self.auth_type, self.auth)

    def unpack(self, data):
        self.version, self.type, self.length, self.router_id, self.area_id, self.checksum, self.auth_type, self.auth = unpack(
            self.structure, data)


class OSPF_Hello:
    def __init__(self):
        self.net_mask = None
        self.hello_interval = 0
        self.options = 0
        self.router_priority = 0
        self.dead_interval = 0
        self.designated_router = 0
        self.backup_router = 0
        self.neighbor = []
        self.structure = '!4sHBBIII'

    def pack(self):
        p = pack(self.structure, self.net_mask, self.hello_interval, self.options,
                 self.router_priority, self.dead_interval, self.designated_router,
                 self.backup_router)
        for n in self.neighbor:
            p = p + pack('!I', n)
        return p

    def unpack(self, data):
        self.net_mask, self.hello_interval, self.options, self.router_priority, self.dead_interval, self.designated_router, self.backup_router = unpack(
            self.structure, data)

    def get_structure(self):
        return self.structure + ('I' * len(self.neighbor))


class OSPF_DBD:
    def __init__(self):
        self.mtu = 1500
        self.options = 0
        self.flags = 0
        self.sequence = 0
        self.structure = '!HBBI'

    def pack(self):
        return pack(self.structure, self.mtu, self.options, self.flags, self.sequence)

    def unpack(self, data):
        self.mtu, self.options, self.flags, self.sequence = unpack(
            self.structure, data)

    def get_structure(self):
        return self.structure


class Packet:
    def __init__(self):
        self.eth = Ethernet()
        self.ip4 = IPV4()
        self.ospf = OSPF_Header()
        self.msg = None

    def pack(self):
        return self.eth.pack() + self.ip4.pack() + self.ospf.pack() + self.msg.pack()

    def get_connection_info(self):
        return ConnectionInfo(self.eth.dst, self.eth.src, self.ip4.dst_addr, self.ip4.src_addr)
