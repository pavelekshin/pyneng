# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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
        elif (
            (src in self.topology.keys())
            or (dst in self.topology.values())
        ):
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
    top = Topology(topology_example)
    print(top.topology)
    top.delete_node("SW1")
    top.add_link(("SW1", "Eth0/1"), ("R1", "Eth0/0"))
    top.add_link(("SW1", "Eth0/1"), ("R9", "Eth0/0"))
    print(top.topology)
