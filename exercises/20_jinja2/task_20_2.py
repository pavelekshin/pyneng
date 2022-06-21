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


def generate_template(template_dir, data, *, filename=None):
    templates = glob.glob(template_dir + "[!f]*.txt")
    templates.reverse()
    new_template = f"{template_dir}{filename}"
    for template in templates:
        with open(template, "r") as f, open(new_template, "a") as w:
            file = f.read()
            w.write(file)
            w.write("\n")
    print(generate_config(new_template, data))


if __name__ == "__main__":
    template_dir = "templates/"
    data_file = "data_files/router_info.yml"
    with open(data_file) as f:
        data = yaml.safe_load(f)
    generate_template(template_dir, data, filename="cisco_router_base.txt")
