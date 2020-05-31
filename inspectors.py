from concurrent.futures import ThreadPoolExecutor
from packets import TestPackets
import socket


class PortChecker:
    def __init__(self, args):
        self.args = args
        self.packets = TestPackets()
        self.executor = ThreadPoolExecutor(5)

    def run(self):
        p_range = range(self.args.ports[0], self.args.ports[1] + 1)
        if not (self.args.tcp or self.args.udp):
            self.args.tcp = True
            self.args.udp = True

        if self.args.udp:
            for port in p_range:
                self.executor.submit(self.check_udp, port)
        if self.args.tcp:
            for port in p_range:
                self.executor.submit(self.check_tcp, port)

    def check_udp(self, port):
        protocol = 'Unknown'

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)

            for packet in self.packets.udp:
                try:
                    s.sendto(packet, (self.args.ip, port))
                    response, _ = s.recvfrom(1024)
                    protocol = self.packets.get_protocol(response)
                except Exception:
                    continue

        if protocol != 'Unknown':
            print('UDP {} port: {} server detected!'.format(port, protocol))
        else:
            print('UDP {} port: Not used...'.format(port))

    def check_tcp(self, port):
        protocol = 'Unknown'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)

            try:
                s.connect((self.args.ip, port))
            except socket.error:
                print('TCP {} port: Not used...'.format(port))
            else:
                for packet in self.packets.tcp:
                    try:
                        s.sendall(packet)
                        response = s.recv(1024)
                        protocol = self.packets.get_protocol(response)
                        if protocol != '\'Unknown\'' or protocol != 'Unknown':
                            break
                    except Exception:
                        continue

        if protocol != 'Unknown':
            print('TCP {} port: {} server detected!'.format(port, protocol))


