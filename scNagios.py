# Author  : udp2013 (git at https://github.com/udp2013)
# Licence : wtfpl - http://www.wtfpl.net/

import optparse
import sys
import socket


def sc_unknown(msg):
    """ Print an unknown message, and exit with code 3
    Args:
        msg: A string with the message
    Returns:
        Nothing
    """
    print('UNKNOWN - %s' % msg)
    sys.exit(3)


def sc_critical(msg):
    """ Print a critical message, and exit with code 2
    Args:
        msg: A string with the message
    Returns:
        Nothing
    """
    print('CRITICAL - %s' % msg)
    sys.exit(2)


def sc_warning(msg):
    """ Print a warning message, and exit with code 1
    Args:
        msg: A string with the message
    Returns:
        Nothing
    """
    print('WARNING - %s' % msg)
    sys.exit(1)


def sc_ok(msg):
    """ Print an OK message, and exit with code 0
    Args:
        msg: A string with the message
    Returns:
        Nothing
    """
    print('OK - %s' % msg)
    sys.exit(0)


def parse_params():
    """ Parse and validate params
    Returns:
        Two dictionaries, one with the options, one with the arguments
    """
    usage = "%prong <arguments>"
    description = 'Check hosts status per ipp'
    parser = optparse.OptionParser(usage=usage, description=description)

    parser.add_option('--host', '-s', action='store', type='string',
                      help='host (hostname[:port])')
    parser.add_option('--version', '-v', action='store_true', default=False,
                      help='Show version')
    (params, args) = parser.parse_args()

    if params.version:
        sc_ok("scNagios version 1.0.0")

    if params.host is None:
        sc_unknown('Wrong syntax. Use -h to get help')

    return params, args


def main():
    """ Test mode  - nmap -p 0-65535 -T5 192.168.101.181
            info: 1 - http port 80
                  2 - https port 443
                  3 - lpr port 515
                  4 - RAW port 9100
                  5 - VNC Server 9062
        Args:

        Returns:
            A hosts' connection object
        """
    params, args = parse_params()
    hostname: object = params.host.split(':')[0]
    result = 1
    try:
        port = int(params.host.split(':')[1])
    except ValueError:
        sc_unknown('Invalid port (not numeric)')
        port = 80
    except IndexError:
        port = 80

    connect_ipp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = connect_ipp.connect_ex((hostname, port))
        # print(result)
        connect_ipp.close()
    except RuntimeError as e:
        # print(e)
        sc_warning(e)

    connect_ipp.close()

    if result == 0:
        sc_ok("Port is open")
    else:
        sc_critical("Port is not open")

    sc_critical("EXIT")


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
