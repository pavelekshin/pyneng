# -*- coding: utf-8 -*-
"""
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
"""

import re
from pprint import pprint


def generate_description_from_cdp(file):
    regex = r"(?P<Devid>[A-Z]+\d+)\s+(?P<Lintf>\S+ \S+) +.+?(?P<Portid>[GEF]\S+ \S+)"
    result = {}
    with open(file, "r") as f:
        for line in f:
            m = re.search(regex, line)
            if m:
                result[
                    m.group("Lintf")
                ] = f"""description Connected to {m.group("Devid")} port {m.group("Portid")}"""

    return result


if __name__ == "__main__":
    pprint(generate_description_from_cdp("sh_cdp_n_sw1.txt"))
