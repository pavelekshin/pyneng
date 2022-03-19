# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def get_int_vlan_map(config_filename):
    access_dict = {}
    trunk_dict = {}
    with open(config_filename, "r") as f:
        for line in f:
            if "FastEthernet" in line:
                intf = line.split()[-1]
            elif "trunk allowed vlan" in line:
                _vlan = line.split()[-1].split(",")
                _vlan_list = sorted({int(item) for item in _vlan})
                trunk_dict[intf] = _vlan_list
            elif "access vlan" in line:
                _vlan = int(line.split()[-1])
                access_dict[intf] = _vlan
            elif "mode access" in line:
                if intf not in access_dict.keys() or trunk_dict.keys():
                    access_dict[intf] = 1
        return access_dict, trunk_dict


access, trunk = get_int_vlan_map("config_sw2.txt")
print(access)
print(trunk)
