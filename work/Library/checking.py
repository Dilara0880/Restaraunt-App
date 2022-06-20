# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Модуль с функциями проверки значений
"""
import re
import time

def is_phone(s):
    '''
    Является ли строка телефоном
    Входные параметры:
        s - строка
    Выходные параметры:
        True/False
    '''
    if len(s) != 12 or not re.search(r"\d\d\d-\d\d\d-\d\d\d\d", s):
        x = False
    else:
        x = True
    return x

def is_date(s):
    '''
    Функция проверки, что строка является датой в пределах 01.01.2000 до сегодняшнего дня
    Входные параметры:
        s - строка
    Выходные параметры:
        True/False
    '''
    try:
        if len(s) == 10:
            date = time.strptime(s, '%d.%m.%Y')
        else:
            raise ValueError
    except ValueError:
        x = False
    else:
        now = time.localtime()
        d = f'{now[2]:02}'
        m = f'{now[1]:02}'
        y = f'{now[0]:02}'
        now = int(f'{y}{m}{d}')
        d = f'{date[2]:02}'
        m = f'{date[1]:02}'
        y = f'{date[0]:02}'
        date = int(f'{y}{m}{d}')
        past = 20000101
        if (date-past) < 0:
            x = False
        elif (now - date) < 0:
            x = False
        else:
            x = True
    return x