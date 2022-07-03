# -*- coding: utf-8 -*-
"""
Задание 21.2

Сделать шаблон TextFSM для обработки вывода sh ip dhcp snooping binding
и записать его в файл templates/sh_ip_dhcp_snooping.template

Вывод команды находится в файле output/sh_ip_dhcp_snooping.txt.

Шаблон должен обрабатывать и возвращать значения таких столбцов:
* mac - такого вида 00:04:A3:3E:5B:69
* ip - такого вида 10.1.10.6
* vlan - 10
* intf - FastEthernet0/10

Проверить работу шаблона с помощью функции parse_command_output из задания 21.1.
"""
from pprint import pprint
from netmiko import ConnectHandler
import textfsm

from task_21_1 import parse_command_output


# вызов функции должен выглядеть так
if __name__ == "__main__":
    output = "output/sh_ip_dhcp_snooping.txt"
    template = "templates/sh_ip_dhcp_snooping.template"
    with open(output, "r") as f:
        output = f.read()
    pprint(output)
    result = parse_command_output(template, output)
    print(result)
