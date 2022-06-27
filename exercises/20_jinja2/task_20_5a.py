# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

from pprint import pprint
import yaml
import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from concurrent.futures import ThreadPoolExecutor

from task_20_1 import generate_config
from task_20_5 import create_vpn_config


def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            router = ssh.find_prompt()
        return {router: result}
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


def send_config_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_config_set(command)
            router = ssh.find_prompt()
        return {router: result}
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


def send_show_command_to_devices(devices, *, command=None, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        for device in devices:
            future = executor.submit(send_show_command, device, command)
            future_list.append(future)
    return parse_data(future_list)


def send_config_command_to_devices(devices, *, command=None, limit=3):
    data = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(send_config_command, devices, command)
        for d in result:
            data.update(d)
    return data.values()


def parse_data(future_list):
    regex = r"(Tunnel(\d+))"
    tunnel_int = {}
    for d in future_list:
        data = d.result()
        for router, value in data.items():
            tunnel_int.setdefault(router, {"tunnels": [], "tunnels_numbers": []})
            if value.startswith("Tunnel"):
                m = re.findall(regex, value)
                if m:
                    for item in m:
                        tunnel_int[router]["tunnels"].append(item[0])
                        tunnel_int[router]["tunnels_numbers"].append(item[1])
    return tunnel_int


def configure_vpn(
    src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict
):
    sh_int_tunnel = send_show_command_to_devices(
        [src_device_params, dst_device_params], command="sh ip int br | b Tunnel"
    )
    unique_used_tunnels = {
        int(item)
        for key, items in sh_int_tunnel.items()
        for item in items["tunnels_numbers"]
    }
    select_tunnel = [num for num in range(0, max(unique_used_tunnels)+2) if num not in unique_used_tunnels]
    vpn_data_dict["tun_num"] = min(select_tunnel)
    src_command, dst_command = create_vpn_config(
        src_template, dst_template, vpn_data_dict
    )
    src_dev, dst_dev = send_config_command_to_devices(
        [src_device_params, dst_device_params],
        command=[src_command.split("\n"), dst_command.split("\n")],
    )
    return src_dev, dst_dev


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    r1, r2 = devices[:2]
    data = {
        "tun_num": None,
        "wan_ip_1": "192.168.100.1",
        "wan_ip_2": "192.168.100.2",
        "tun_ip_1": "10.0.1.1 255.255.255.252",
        "tun_ip_2": "10.0.1.2 255.255.255.252",
    }
    template1 = "templates/gre_ipsec_vpn_1.txt"
    template2 = "templates/gre_ipsec_vpn_2.txt"
    print(configure_vpn(r1, r2, template1, template2, data))
