# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Модуль с функцией создания имени файла
"""
import time

def time_filename(report_type):
    """
    Функция создания названия файла
    Входные параметры:
    Строка - название файла
    Выходные параметры:
    Строка вида <Название файла>_<Дата сохранения>_<Время сохранения>
    """
    name = report_type.replace(' ', '_')
    struct = time.localtime()
    name += f'_{struct[2]:02}_{struct[1]:02}_{struct[0]:02}_'\
    f'{struct[3]:02}_{struct[4]:02}_{struct[5]:02}'
    return name