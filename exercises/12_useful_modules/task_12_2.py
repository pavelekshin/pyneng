# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""

from pprint import pprint

import ipaddress

ipaddrlist = ["10.1.1.1", "10.4.10.10-13", "192.168.1.12-192.168.1.15"]


def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def convert_ranges_to_ip_list(ip_address):
    """
    convert ip:
    10.1.1.1
    10.1.1.1-10.1.1.10
    10.1.1.1-10
    """
    iplist = []
    for ip in ip_address:
        if check_ip(ip):
            iplist.append(ip)
        else:
            ip, iprange = ip.split("-")
            if 1 <= len(iprange) <= 3 and check_ip(ip):
                _start = int(ip.split(".")[-1])
                _end = int(iprange)
                _range = (_end - _start) +1
                print(_range)
                ip = ipaddress.ip_address(ip)
                _iplist = [iplist.append(str(ip + x)) for x in range(_range)]
            elif len(iprange) > 3 and check_ip(ip):
                _start = int(ip.split(".")[-1])
                _end = int(iprange.split(".")[-1])
                _range = (_end - _start) +1
                ip = ipaddress.ip_address(ip)
                _iplist = [iplist.append(str(ip + x)) for x in range(_range)]
    return iplist


if __name__ == "__main__":
    result = convert_ranges_to_ip_list(ipaddrlist)
    pprint(result)
