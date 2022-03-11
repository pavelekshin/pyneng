# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from pprint import pprint

user_input = input("Please ennter VLAN: ")

with open("CAM_table.txt", "r") as f:
    output = f.read()

output = output.split("\n")
sl = []
for line in output:
    if "DYNAMIC" in line:
        vlan, mac, _dynamic, intf = line.split()
        _ll = int(vlan), mac, intf
        sl.append(list(_ll))
sl = sorted(sl)
for vlan, mac, intf in sl:
    if vlan == int(user_input):
        print(f"{vlan:<8} {mac:<24} {intf:<8}")
