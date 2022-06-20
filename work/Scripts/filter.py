# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Модуль с функциями фильтрации таблицы
"""
import pandas as pd

def check_condition(table, condition):
    '''
    Функция проверки условия на правильность
    Входные данные:
        table - таблица pandas.DataFrame
        condition - условие - список из 3 элементов:
            1 элемент - название атрибута
            2 элемент - наименование способа сравнения
            3 элемент - значение для сравнения
    Выходные данные:
        Число -1, 0, 1
        -1 - одно из полей пустое
        0 - ошибочное условие
        1 - корректное условие
    '''
    if condition[0] and condition[1] and condition[2]:
        if table[condition[0]].dtype == int or table[condition[0]].dtype == float:
            x = 1
            try:
                condition[2] = float(condition[2])
            except ValueError:
                x = 0
        elif condition[1] in ['равно', 'не равно']:
            x = 1
        else:
            x = 0
    else:
        x = -1
    return x


def list2index(table, condition):
    '''
    Получение логического отбора строк из таблицы по условию
    Входные данные:
        table - таблица pandas.DataFrame
        condition - условие - список из 3 элементов:
            1 элемент - название атрибута
            2 элемент - наименование способа сравнения
            3 элемент - значение для сравнения
    Выходные данные:
        ind1 - pandas.Series, содержащий значения True при строках, подходящих
        под условие и False при неподходящих
    '''
    column = condition[0]
    value = condition[2]
    if condition[1] == 'равно':
        ind1 = table[column] == value
    elif condition[1] == 'не равно':
        ind1 = table[column] != value
    elif condition[1] == 'больше или равно':
        ind1 = table[column] >= value
    elif condition[1] == 'меньше или равно':
        ind1 = table[column] <= value
    elif condition[1] == 'больше':
        ind1 = table[column] > value
    else:
        ind1 = table[column] < value
    return ind1


def get_index(conditions, table):
    '''
    Получение общего логического отбора для 3 условий
    Входные данные:
        conditions - список условий вида condititon и способов объединения условий (И/ИЛИ)
            1 элемент - название атрибута
            2 элемент - наименование способа сравнения
            3 элемент - значение для сравнения
        table - база данных pandas.DataFrame
    Выходные данные:
        словарь вида {index: ind, error: error}
        ind - pandas.Series, содержащий значения True при строках, подходящих
        под условие и False при неподходящих
        error - код ошибки
        Коды ошибок:
            0 - успешный отбор строк
            1 - не удалось отборать строки
            2 - второе условие некорректно
            3 - третье условие некорректно
    '''
    ind = pd.Series([True for _ in range(len(table))])
    error = 0
    if check_condition(table, conditions[0]) == 1:
        #1 условие корректно
        ind = list2index(table, conditions[0])
        if check_condition(table, conditions[2]) == 1:
            #2 условие корректно
            if conditions[1] == 'И':
                ind = ind & list2index(table, conditions[2])
            else:
                ind = ind | list2index(table, conditions[2])
            if check_condition(table, conditions[4]) == 1:
                #3 условие корректно
                if conditions[3] == 'И':
                    ind = ind & list2index(table, conditions[4])
                else:
                    ind = ind | list2index(table, conditions[4])
            elif check_condition(table, conditions[4]) == 0:
                #3 условие некорректно
                error = 3
        elif check_condition(table, conditions[2]) == 0:
            #2 условие некорректно
            error = 2
        elif check_condition(table, conditions[4]) != -1:
            #Есть третье условие при пустом втором условии
            error = 2
    else:
        #1 условие некорректно
        error = 1
    return {'index': ind, 'error': error}