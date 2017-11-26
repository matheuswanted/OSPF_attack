from Packet import *
from struct import *
from Utils import *
import sys


class PacketBuilder:
    def __init__(self):
        self.p = Packet()

    def build_Eth(self, src_mac, dst_mac):
        self.p.eth.setSrc(src_mac)
        self.p.eth.setDst(dst_mac)

    def build_Ip4(self, src_addr, dst_addr):
        self.p.ip4.setDst(dst_addr)
        self.p.ip4.setSrc(src_addr)

    def build_Ospf(self):
        self.p.ospf.area_id = AREA_ID
        self.p.ospf.auth = AUTH
        self.p.ospf.auth_type = AUTH_TYPE
        self.p.ospf.checksum = 0

    def build_Hello(self):
        self.p.ospf.type = 1
        hello = OSPF_Hello()
        hello.net_mask = to_net_addr(NET_MASK)
        hello.backup_router = 0
        hello.designated_router = DST_ROUTER_ID
        hello.dead_interval = DEAD_INTERVAL
        hello.hello_interval = HELLO_INTERVAL
        hello.router_priority = 0
        hello.options = 0
        hello.neighbor.append(DST_ROUTER_ID)
        self.p.msg = hello

    def build_DBD(self, sequence, initial=False):
        self.p.ospf.type = 2
        dbd = OSPF_DBD()
        dbd.sequence = sequence
        dbd.flags = 1
        if initial:
            dbd.flags += 0b100
        self.p.msg = dbd

    def buid_Length(self):
        size = calcsize(self.p.msg.get_structure()) + \
            calcsize(self.p.ospf.structure)
        # print "size: " + str(size)
        # print "msg: " + str(message)
        self.p.ip4.total_length += size
        self.p.ospf.length = size
        return self

    def calculate_checksum(self):
        self.p.ip4.checksum = self.__checksum_from_packets__(
            self.p.ip4.pack(), calcsize(self.p.ip4.structure), [10, 11])

        self.p.ospf.checksum = self.__checksum_from_packets__(
            self.p.ospf.pack() + self.p.msg.pack(), calcsize(self.p.ospf.structure) + calcsize(self.p.msg.get_structure()), range(16, 24)+[12,13])

    def __checksum_from_packets__(self, packet, size, ignore=[]):
        fields = unpack('!' + 'B' * size, packet)
        return self.__checksum__(fields, size, ignore)

    def __checksum__(self, fields, size, ignore=[]):
        current = 0
        chksum = 0
        while size > 1:
            if current not in ignore:
                chksum += (fields[current] << 8) + fields[current + 1]
            size -= 2
            current += 2
        if size:
            chksum += fields[current]

        chksum = (chksum >> 16) + (chksum & 0xFFFF)
        chksum += (chksum >> 16)

        return ~chksum & 0xFFFF

#    def unpack_eth(self, data):
#        data_len = len(data)
#        if data_len < 14:
#            raise Exception('Wrong size ethernet packet!')
#        elif data_len > 14:
#            data = data[0:14]
#        self.p.eth.unpack(data)
#
#    def unpack_ipv6(self, data):
#        data_len = len(data)
#        if data_len < 40:
#            raise Exception('Wrong size ipv6 packet!')
#        elif data_len > 40:
#            data = data[14:54]
#        self.p.ip4.unpack(data)
#
#    def unpack_udp(self, data):
#        data_len = len(data)
#        if data_len < 8:
#            raise Exception('Wrong size udp packet!')
#        elif data_len > 8:
#            data = data[54:62]
#        self.p.udp.unpack(data)
#
#    def unpack_message(self, data):
#        self.p.msg.unpack(data[62:])

    def get_message(self):
        return self.p.msg

    def get_connection_info(self):
        return self.p.get_connection_info()

    def pack(self):
        return self.p.pack()
