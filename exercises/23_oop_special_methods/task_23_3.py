# -*- coding: utf-8 -*-

"""
Задание 23.3

Скопировать и изменить класс Topology из задания 22.1x.

Добавить метод, который позволит выполнять сложение двух экземпляров класса Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
"""


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def __str__(self):
        return f"{self.topology}"

    def __repr__(self):
        return f"Topology {self}"

    def __add__(self, other):
        stacked_topology = {}
        for k, v in self.topology.items():
            stacked_topology[k] = v
        for k, v in other.topology.items():
            stacked_topology[k] = v
        return Topology(stacked_topology)

    def __iter__(self):
        return iter(self.items())

    def __len__(self):
        return len(self.topology)

    def _normalize(self, topology_dict):
        d = {}
        for key, value in topology_dict.items():
            if key not in d.values():
                d[key] = value
        return d

    def delete_link(self, key, value):
        if self.topology.get(key) == value:
            del self.topology[key]
        elif self.topology.get(value) == key:
            del self.topology[value]
        else:
            print(f"Такого соединения нет")

    def delete_node(self, node):
        if self._check_node_in_topology(node):
            for k, v in list(self.topology.items()):
                if (node in k) or (node in v):
                    del self.topology[k]
        else:
            print(f"Такого устройства нет")

    def _check_node_in_topology(self, node):
        s = set()
        for k, v in self.topology.items():
            s.add(k[0])
            s.add(v[0])
        if node in s:
            return True
        else:
            return False

    def add_link(self, src, dst):
        if (src in self.topology.keys()) and (dst in self.topology.values()):
            print(f"Такое соединение существует")
        elif (src in self.topology.keys()) or (dst in self.topology.values()):
            self.topology[src] = dst
            print(f"Cоединение с одним из портов существует")
        else:
            self.topology[src] = dst


if __name__ == "__main__":
    topology_example2 = {
        ("R1", "Eth0/4"): ("R7", "Eth0/0"),
        ("R1", "Eth0/6"): ("R9", "Eth0/0"),
    }

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
    t1 = Topology(topology_example)
    t2 = Topology(topology_example2)
    print(t1.topology)
    print(t2.topology)
