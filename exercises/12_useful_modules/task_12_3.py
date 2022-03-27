# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""

from tabulate import tabulate
from pprint import pprint
from itertools import zip_longest

from task_12_1 import ping_ip_addresses

ok = ["192.168.1.1", "127.0.0.1", "192.168.100.100", "125.0.1.24"]
nok = ["111.111.111.111"]


def print_ip_table(ok, nok):
    printlist = zip_longest(ok, nok)
    print(tabulate(printlist, headers=["Reachable", "Unreachable"]))


if __name__ == "__main__":
    print_ip_table(ok, nok)
