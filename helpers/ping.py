from icmplib import ping

from helpers.logs import logging

def ip4_ping(ip4_addr):
    """
    ip4_ping A simple pinger that will send icmp packets to the ip address provided using
    the icmplib library

    Args:
        ip4_addr (str): The IP address of the device to be pinged

    Returns:
        bool: True if the device is pingable, False otherwise.
    """

    if ping(ip4_addr, count=2, interval=0.5, timeout=1, privileged=False):
        logging.info(f"{ip4_addr} responded to ping and is reachable")
        return True
    else:
        logging.info(f"{ip4_addr} is not responding to ping")
        return False

