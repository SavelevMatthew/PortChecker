from argparse import ArgumentParser
from inspectors import PortChecker


def main():
    parser = ArgumentParser(description='This utility will check device ports '
                                        'and try to detect servers, '
                                        'running on it')
    parser.add_argument('ip', help='IP address of device to check', type=str)
    parser.add_argument('-p', '--ports', nargs=2, type=int,
                        help='Ports range to scan')
    parser.add_argument('-u',  '--udp', help='Use flag to check using UDP',
                        action='store_true')
    parser.add_argument('-t', '--tcp', help='Use this to check ports via TCP',
                        action='store_true')
    args = parser.parse_args()

    inspector = PortChecker(args)
    inspector.run()


if __name__ == '__main__':
    main()