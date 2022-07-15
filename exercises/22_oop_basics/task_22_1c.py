# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

"""


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def __str__(self):
        return f"{self.topology}"

    def __repr__(self):
        return f"Topology {self}"

    def __iter__(self):
        print("iter!")
        return iter(self.topology)

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
            d = {
                k: v
                for k, v in self.topology.items()
                if (node not in k) and (node not in v)
            }
            self.topology = d
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
    top.delete_node("SW1")
