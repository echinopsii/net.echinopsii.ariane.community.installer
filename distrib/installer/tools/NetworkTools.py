# CC installer network interfaces tooling
#
# Copyright (C) 2014 Mathilde Ffrench
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import socket
import netifaces

__author__ = 'mffrench'


def get_system_network_interfaces_and_ip_addresses():
    ifaces = netifaces.interfaces()
    # print("interfaces : " + ",".join(ifaces))
    ret = []
    for iface in ifaces:
        iface_address_list = []
        addresses = netifaces.ifaddresses(iface)[netifaces.AF_INET]
        # print("addresses for interfaces " + iface + " : " + ",".join(str(d) for d in addresses))
        for address in addresses:
            ip_address = address.get('addr')
            iface_address_list.append([iface, ip_address])
            # print("ifaceAddressList : " + str(",".join(str(d) for d in ifaceAddressList)))

        ret.extend(iface_address_list)
        # print("ret : " + ",".join(str(d) for d in ret))
    return ret


def is_system_network_address(address):
    pass


def print_system_network_interfaces(available_interfaces_and_ip_addresses):
    print("Available system network interfaces and addresses :\n")
    print('{:20} {:20}'.format("interface", "address"))
    print('{:20} {:20}'.format("---------", "-------"))
    for ifAndAddr in available_interfaces_and_ip_addresses:
        print('{:20} {:20}'.format(ifAndAddr[0], ifAndAddr[1]))
    print('{:20} {:20}\n'.format("---------", "-------"))


def is_port_available(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip_address,port))
    sock.close()
    if result == 0:
        return False
    else:
        return True
