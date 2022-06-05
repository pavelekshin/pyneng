# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""


import subprocess
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

iplist = ["192.168.1.1", "127.0.0.1", "192.168.100.100"]


def ping(address, count=1):
    command = f"ping {address} -c{count}"
    result = subprocess.run(command.split(), stdout=subprocess.DEVNULL)
    return {address: result.returncode}


def ping_ip_addresses(ip_list, limit=3):
    ok, n_ok = [], []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        for address in ip_list:
            future = executor.submit(ping, address)
            future_list.append(future)
        for f in future_list:
            result = f.result()
            for ip, code in result.items():
                if code == 0:
                    ok.append(ip)
                else:
                    n_ok.append(ip)
    return ok, n_ok


if __name__ == "__main__":
    print(ping_ip_addresses(iplist))
