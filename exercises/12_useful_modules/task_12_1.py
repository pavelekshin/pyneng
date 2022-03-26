# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import subprocess

from pprint import pprint

iplist = ["192.168.1.1", "127.0.0.1", "192.168.100.100"]


def ping_ip_addresses(ip_address):
    ok = []
    n_ok = []
    for address in ip_address:
        command = f"ping {address} -c1"
        result = subprocess.run(command.split(),stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            ok.append(address)
        else:
            n_ok.append(address)
    return ok, n_ok


if __name__ == "__main__":
    ping_ip_addresses(iplist)
