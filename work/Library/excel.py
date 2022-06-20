# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Функции для работы с Excel
"""

def index2Excel(n):
    '''
    Функция перевода номера столбца в буквенное обозначение (как в Excel)
    Номера начинаются с нуля
    Входные данные:
        n - номер столбца
    Выходные данные:
        буквенное обозначение столбца в Excel
    Пример:
        0 -- A
        25 -- Z
        26 -- AA
    '''
    s = []
    #Перевод числа в 26-ричную систему, 0 - значащий разряд (01 != 1)
    while n // 26 != 0:
        s.append(n % 26)
        n = n // 26 - 1
    s.append(n % 26)
    s.reverse()
    return ''.join([chr(65 + i) for i in s])

def w_column(data):
    '''
    Функция для вычисления оптимальной ширины столбца в Excel
    Входные данные:
        data - столбец с данными (pandas.Series)
    Выходные данные:
        Ширина столбца (int)
    '''
    #Составляем массив длин строк
    lengths = [len(str(s)) for s in data]
    lengths.append(len(str(data.name)))
    return max(lengths) + 5