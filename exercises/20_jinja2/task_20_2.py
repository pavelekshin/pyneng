# -*- coding: utf-8 -*-
"""
Задание 20.2

Создать шаблон templates/cisco_router_base.txt.

В шаблон templates/cisco_router_base.txt должно быть включено содержимое шаблонов:
* templates/cisco_base.txt
* templates/alias.txt
* templates/eem_int_desc.txt

При этом, нельзя копировать текст шаблонов.

Проверьте шаблон templates/cisco_router_base.txt, с помощью
функции generate_config из задания 20.1. Не копируйте код функции generate_config.

В качестве данных, используйте информацию из файла data_files/router_info.yml

"""
import os
import glob

import yaml

from task_20_1 import generate_config


def generate_template(template_file, templates, data):
    with open(template_file, "w") as w:
        for line in templates:
            w.write(line + "\n")
    print(generate_config(template_file, data))


if __name__ == "__main__":
    template_file = "templates/cisco_router_base.txt"
    data_file = "data_files/router_info.yml"
    templates = [
        "{% include 'cisco_base.txt' %}",
        "{% include 'alias.txt' %}",
        "{% include 'eem_int_desc.txt' %}",
    ]
    with open(data_file) as f:
        data = yaml.safe_load(f)
    generate_template(template_file, templates, data)
