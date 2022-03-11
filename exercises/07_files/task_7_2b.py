#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from pprint import pprint
from sys import argv

file_r = argv[1]
file_w = argv[2]

with open(file_r, "r") as f:
    output = f.read()

output = output.split("\n")
with open(file_w, "w") as f:
    for line in output:
        if line.startswith("!"):
            pass
        elif line.startswith(","):
            pass
        elif set(ignore).intersection(line.split(" ")):
            pass
        else:
            f.write(line + "\n")
