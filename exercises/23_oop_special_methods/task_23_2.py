# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка

Тест проверяет подключение с параметрами из файла devices.yaml. Там должны быть
указаны доступные устройства.
"""

import telnetlib
import time
from pprint import pprint


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username")
        self._write_line(username)
        self.telnet.read_until(b"Password")
        self._write_line(password)
        if secret:
            self.telnet.write(b"enable\n")
            self.telnet.read_until(b"Password")
            self._write_line(secret)
        time.sleep(0.5)
        self.telnet.read_very_eager()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.telnet.close()

    def _write_line(self, line):
        self.telnet.write(line.encode("ascii") + b"\n")

    def send_show_command(self, command):
        self._write_line(command)
        output = self.telnet.read_until(b"#").decode("utf-8")
        return output


if __name__ == "__main__":
    r1_params = {
        "ip": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with CiscoTelnet(**r1_params) as r1:
        print(r1.send_show_command("show clock"))
