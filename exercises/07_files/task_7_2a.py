#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]


from pprint import pprint
from sys import argv

file = argv[1]

with open(file, "r") as f:
    output = f.read()

output = output.split("\n")
for line in output:
    if line.startswith("!"):
        pass
    elif line.startswith(","):
        pass
    elif set(ignore).intersection(line.split(" ")):
        pass
    else:
        print(line)
