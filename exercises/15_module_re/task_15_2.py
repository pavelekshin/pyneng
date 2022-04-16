# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""

import re
from pprint import pprint


def parse_sh_ip_int_br(file):
    result = []
    regex = r"(?P<intf>[A-Z]\S+)\s+(?P<ip>\S+)\s+YES\s+\S+\s+(?P<status>up|down|\S+\s\S+)\s+(?P<protocol>\S+)"
    with open(file, "r") as f:
        for line in f:
            m = re.search(regex,line)
            if m:
                result.append(m.group("intf","ip","status","protocol"))
    return result


if __name__ == "__main__":
    pprint(parse_sh_ip_int_br("sh_ip_int_br.txt"))
