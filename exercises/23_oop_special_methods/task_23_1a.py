# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""

import ipaddress


class IPAddress:
    def __init__(self, ip_address):
        self.ip, self.mask = self._check_address(ip_address)

    def __str__(self):
        return f"IP address {self.ip}/{self.mask}"

    def __repr__(self):
        return f"""IPAddress('{self.ip}/{self.mask}')"""

    def _check_address(self, ip_address):
        ip, mask = ip_address.split("/")
        try:
            if ipaddress.ip_address(ip):
                pass
        except ValueError:
            raise ValueError("Incorrect IPv4 address")
        if int(mask) in range(8, 33):
            pass
        else:
            raise ValueError("Incorrect mask")

        return ip, int(mask)


if __name__ == "__main__":
    ip = IPAddress("10.1.1.1/24")
    print(ip.ip)
    print(ip.mask)
    print(ip)
    ip_list = []
    ip_list.append(ip)
    print(ip_list)
