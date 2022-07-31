# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def __str__(self):
        return f"{self.topology}"

    def __repr__(self):
        return f"Topology {self}"

    def __add__(self, other):
        stacked_topology = self.topology.copy()
        stacked_topology.update(other.topology)
        return Topology(stacked_topology)

    def __iter__(self):
        return iter(self.topology.items())

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
