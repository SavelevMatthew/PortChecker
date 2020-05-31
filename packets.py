from random import randint
from struct import pack, unpack
from re import match


class TestPackets:
    def __init__(self):
        self.id = randint(1, 65535)
        self.dns = pack('!HHHHHH', self.id, 256, 1, 0, 0, 0) + \
                   b'\x06google\x03com\x00\x00\x01\x00\x01'
        self.smtp = b'EHLO savelevmatthew@gmail.com\r\n'
        self.pop = b'USER savelevmatthew\r\n'

        self.tcp = [self.dns, self.smtp, self.pop]
        self.udp = [self.dns]

    def get_protocol(self, response):
        if b'HTTP' in response:
            return '\'HTTP\''
        elif response.startswith(b'+'):
            return '\'POP3\''
        elif pack('!H', self.id) in response:
            return '\'DNS\''
        elif match(br'[0-9]{3}', response[:3]):
            return '\'SMTP\''
        else:
            try:
                unpack('!BBBb11I', response)
                return '\'NTP\''
            except Exception:
                return '\'Unknown\''
