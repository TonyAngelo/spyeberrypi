from __future__ import absolute_import, division, print_function
import logging
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import errno

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='../logs/ipscan.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def long2net(arg):
    if (arg <= 0 or arg >= 0xFFFFFFFF):
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))

def mac2int(mac):
    return int(mac.replace(':',''),16)

def to_CIDR_notation(bytes_network, bytes_netmask):
    network = scapy.utils.ltoa(bytes_network)
    netmask = long2net(bytes_netmask)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        logger.warn("%s is too big. skipping" % net)
        return None

    return net

def scan_and_find_mac(net, interface, target_mac, timeout=1):
    logger.info("Start arping %s on %s" % (net, interface))
    try:
        ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=False)
        logger.info("Found %s responsive IPs and %s non-responsive IPs." % (len(ans), len(unans)))

        if len(ans)>0:
            for s, r in ans.res:
                devMAC = r.sprintf("%Ether.src%")
                devIP = r.sprintf("%ARP.psrc%")
                #logger.info("Network device " + devMAC + " at " + devIP)
                
                if mac2int(devMAC) == mac2int(target_mac):
                    logger.info("Bingo! Target device " + devMAC + " found at " + devIP)
                    try:
                        socket.inet_aton(devIP)
                        logger.info("IP " + devIP + " is valid.")
                        return devIP
                    except socket.error:
                        logger.warn("IP " + devIP + " is not valid.")
        else:
            logger.error("No responsive IPs found; %s on %s" % (net, interface))
        return ''
            
    except socket.error as e:
        if e.errno == errno.EPERM:     # Operation not permitted
            logger.error("%s. Did you run as root?", e.strerror)
        else:
            raise


def find_mac_on_network(mac):
    for network, netmask, _, interface, address in scapy.config.conf.route.routes:

        # skip loopback network and default gw
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue

        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue

        net = to_CIDR_notation(network, netmask)

        if interface != scapy.config.conf.iface:
            # see http://trac.secdev.org/scapy/ticket/537
            logger.warn("skipping %s because scapy currently doesn't support arping on non-primary network interfaces", net)
            continue

        if net:
            return scan_and_find_mac(net, interface, mac)
