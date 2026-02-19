import socket
import psutil
import ipaddress
import netifaces

def parse_ports(port_input):
    ports = set()
    parts = port_input.split(",")

    for part in parts:
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))

    return sorted([p for p in ports if 1 <= p <= 65535])


def get_local_network():
    interfaces = psutil.net_if_addrs()

    for interface in interfaces:
        for addr in interfaces[interface]:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                network = ipaddress.IPv4Network(
                    f"{addr.address}/{addr.netmask}", strict=False
                )
                return str(network)

    return None


def get_default_gateway():
    gateways = netifaces.gateways()
    default = gateways.get("default")

    if default and netifaces.AF_INET in default:
        return default[netifaces.AF_INET][0]

    return None
