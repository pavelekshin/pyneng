# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

from textfsm import clitable
from pprint import pprint
import yaml
import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from concurrent.futures import ThreadPoolExecutor


def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            router = ssh.find_prompt()
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


def send_and_parse_show_command(device_dict, command, templates_path, index="index"):
    command_output = send_show_command(device_dict, command)
    cli_table = clitable.CliTable(index, templates_path)
    cli_table.ParseCmd(
        command_output, {"Command": command}
    )
    data_rows = [list(row) for row in cli_table]
    header = list(cli_table.header)
    return [dict(zip(header, line)) for line in data_rows]
    

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    r1 = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    print(
        send_and_parse_show_command(
            r1, "sh ip int br", templates_path="templates", index="index"
        )
    )
