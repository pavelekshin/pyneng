# -*- coding: utf-8 -*-

"""
Задание 22.1

Создать класс Topology, который представляет топологию сети.

При создании экземпляра класса, как аргумент передается словарь,
который описывает топологию. Словарь может содержать "дублирующиеся" соединения.
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Задача оставить только один из этих линков в итоговом словаре, не важно какой.

В каждом экземпляре должна быть создана переменная topology, в которой содержится
словарь топологии, но уже без "дублей". Переменная topology должна содержать словарь
без "дублей" сразу после создания экземпляра.

Пример создания экземпляра класса:
In [2]: top = Topology(topology_example)

После этого, должна быть доступна переменная topology:

In [3]: top.topology
Out[3]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

"""


class Topology:
    def __init__(self, topology):
        self.topology = topology
        self.topology = self.create_unique_topology()

    def __str__(self):
        return f"{self.topology}"

    def __repr__(self):
        return f"Topology {self}"

    def create_unique_topology(self):
        d = {}
        for key, value in self.topology.items():
            if key not in d.values():
                d[key] = value
        return d


if __name__ == "__main__":
    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }
    top = Topology(topology_example)
    print(top.topology)
