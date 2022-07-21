# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""

from textfsm import clitable
import telnetlib
import time
from pprint import pprint


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
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

    def _write_line(self, line):
        self.telnet.write(line.encode("ascii") + b"\n")

    def _parse_output(
        self, command, command_output, templates="templates", index="index"
    ):
        cli_table = clitable.CliTable(index, templates)
        cli_table.ParseCmd(command_output, {"Command": command})
        data_rows = [list(row) for row in cli_table]
        header = list(cli_table.header)
        return [dict(zip(header, line)) for line in data_rows]

    def send_show_command(
        self, command, parse=True, templates="templates", index="index"
    ):
        self._write_line(command)
        output = self.telnet.read_until(b"#").decode("utf-8")
        if parse:
            return self._parse_output(command, output)
        else:
            return output

    def send_config_commands(self, command, strict=False):
        if type(command) is str:
            commands = ["conf t", command, "end"]
        else:
            commands = ["conf t", *command, "end"]
        result = ""
        for cmd in commands:
            self._write_line(cmd)
            output = self.telnet.read_until(b"#").decode("utf-8")
            if "% Invalid input detected at '^' marker" in output and strict:
                raise ValueError(
                    f"При выполнении комманды {cmd} на устройстве {self.ip} возникла ошибка -> % Invalid input detected at '^' marker"
                )
            elif "% Ambiguous command" in output and strict:
                raise ValueError(
                    f"При выполнении комманды {cmd} на устройстве {self.ip} возникла ошибка -> % Ambiguous command"
                )
            elif "% Incomplete command" in output and strict:
                raise ValueError(
                    f"При выполнении комманды {cmd} на устройстве {self.ip} возникла ошибка -> % Incomplete command"
                )
            elif "%" in output and not strict:
                print(
                    f"При выполнении комманды {cmd} на устройстве {self.ip} возникла ошибка -> {output}"
                )
            result += output
        return result


if __name__ == "__main__":
    r1_params = {
        "ip": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    r1 = CiscoTelnet(**r1_params)
    commands_with_errors = ["logging 0255.255.1", "logging", "a"]
    correct_commands = ["logging buffered 20010", "ip http server"]
    commands = commands_with_errors + correct_commands

    print(r1.send_show_command("show clock", parse=True))
    print(r1.send_config_commands(commands, strict=True))
