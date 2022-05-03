# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий
для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно,
чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии,
но и удалять "дублирующиеся" соединения (их лучше всего видно на схеме, которую
генерирует функция draw_topology из файла draw_network_graph.py).
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Из-за того что один и тот же линк описывается дважды, на схеме будут лишние соединения.
Задача оставить только один из этих линков в итоговом словаре, не важно какой.

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии
с помощью функции draw_topology.
Не копировать код функции draw_topology из файла draw_network_graph.py.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть "дублирующихся" линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""

import yaml
import glob
from pprint import pprint
from draw_network_graph import draw_topology


def transform_topology(topology):
    result = {}
    _k, _v = [], []
    if topology:
        with open(topology, "r", encoding="utf-8") as f:
            topology_dict = yaml.safe_load(f)
            for device, params in topology_dict.items():
                for key, value in params.items():
                    _k.append((device, key))  # create list key pair ('R4', 'Fa 0/1')
                    [
                        _v.append((key, value)) for key, value in value.items()
                    ]  # create list value pair ('R5', 'Fa 0/1')
                    d = dict(
                        zip(_k, _v)
                    )  # create dictionary with list key:value ('R4', 'Fa 0/1'): ('R5', 'Fa 0/1')
        for key, value in d.items():  # create new dictionary with unique key:value pair
            if key not in result.values():
                result[key] = value
    return result


if __name__ == "__main__":
    topology = transform_topology("topology.yaml")
    draw_topology(topology)
