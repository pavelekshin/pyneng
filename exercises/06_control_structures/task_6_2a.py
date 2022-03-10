# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
correct_ip = False
password_oct = []
while not correct_ip:
    ip_in = input("Please enter IP: ")
    ipaddr = ip_in.split(".")
    if len(ipaddr) == 4:
        for attr in ipaddr:
            if attr.isdigit() and (0 <= int(attr) <= 255):
                password_oct.append(True)
                if password_oct.count(True) == len(ipaddr):
                    correct_ip = True
            else:
                print("Неправильный IP-адрес")
                password_oct.clear()
                break
    else:
        print("Неправильный IP-адрес")
else:
    correct_ip = True

if ipaddr[0] >= "1" and ipaddr[0] <= "223":
    print("unicast")
elif ipaddr[0] >= "224" and ipaddr[0] <= "239":
    print("multicast")
elif (ipaddr.count(ipaddr[0]) == len(ipaddr)) and ipaddr[0] == "255":
    print("local broadcast")
elif (ipaddr.count(ipaddr[0]) == len(ipaddr)) and ipaddr[0] == "0":
    print("unassigned")
else:
    print("unused")
