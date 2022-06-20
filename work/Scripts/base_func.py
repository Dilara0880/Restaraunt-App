# -*- coding: utf-8 -*-
# pylint: disable=C0103, E0611
"""
Модуль с функциями для работы с базой данных
"""
import os
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import pandas as pd
import numpy as np
from Library import checking


# Функции добавления в базу данных
def add_dish(tree, database, info):
    """
    Добавление столика
    Входные данные:
        tree - виджет TreeView
        database - база данных (список из 4 таблиц pandas.DataFrame)
        info - список с данными нового заказа (код блюда, код заказа, блюдо, рецепт,
            состав, время приготовления, цена, объем)
    Выходные данные:
        -
    """

    info = {'Код блюда': info[0], 'Код заказа': info[1], 'Блюдо': info[2], 'Рецепт': info[3], 'Состав': info[4],
            'Время приготовления': info[5], 'Цена': info[6], 'Объем': info[7]}
    info = pd.Series(info)
    database[2] = database[2].append(info, ignore_index=True)
    database[3] = merging(database[0], database[1], database[2])
    children = tree.get_children()
    for i in children:
        tree.delete(i)
    i = iter(database[1].index)
    for item in database[1].values:
        tree.insert('', 'end', next(i), values=list(item))


def add_employee(tree, database, info):
    """
    Добавление сотрудника
    Входные данные:
        tree - виджет TreeView
        database - база данных (список из 4 таблиц pandas.DataFrame)
        info - список с данными нового сотрудника (код, фамилия, возраст, серия и номер паспорта, адрес, номер телефона, оклад)
    Выходные данные:
        -
    """
    if not checking.is_phone(info[5]):
        mb.showinfo('Предупреждение', 'Запись не будет добавлена, неверный формат номера телефона')
    elif (info[0], info[1]) in map(tuple, list(database[0][["Код сотрудника", "Фамилия"]].values)):
        mb.showinfo('Предупреждение', 'Запись не будет добавлена, так как уже есть такой сотрудник')
    else:
        info = {'Код сотрудника': info[0], 'Фамилия': info[1], 'Возраст': info[2], 'Паспорт': info[3],
                'Адрес': info[4], 'Телефон': info[5], 'Оклад': info[6]}
        info = pd.Series(info)
        database[0] = database[0].append(info, ignore_index=True)
        database[3] = merging(database[0], database[1], database[2])
        employees = tree.get_children()
        for i in employees:
            tree.delete(i)
        i = iter(database[0].index)
        for item in database[0].values:
            tree.insert('', 'end', next(i), values=list(item))


def add_order(tree, database, info):
    """
    Добавление заказа
    Входные данные:
        tree - виджет TreeView
        database - база данных (список из 4 таблиц pandas.DataFrame)
        info - список с данными для добавления (код заказа, код сотрудника, дата заказа, время заказа,
            номер стола, стоимость заказа)
    Выходные данные:
        -
    """
    if not checking.is_date(info[2]):
        mb.showinfo('Предупреждение', 'Запись не будет добавлена, неверный формат даты')
    elif info[1] not in map(tuple, list(database[0][['Код сотрудника']].values)):
        mb.showinfo('Предупреждение', 'Запись не будет добавлена, нет такого сотрудника')
    elif (info[0], info[1], info[2]) in map(tuple, list(database[1][["Код заказа", "Код сотрудника",
                                                                     "Дата"]].values)):
        mb.showinfo('Предупреждение',
                    'Запись не будет добавлена, эта информация уже есть в базе данных')
    else:
        info = {'Код заказа': info[0], 'Код сотрудника': info[1], 'Дата': info[2], 'Время': info[3],
                'Стол': info[4], 'Стоимость': info[5]}
        info = pd.Series(info)
        database[1] = database[1].append(info, ignore_index=True)
        database[3] = merging(database[0], database[1], database[2])
        orders = tree.get_children()
        for i in orders:
            tree.delete(i)
        i = iter(database[1].index)
        for item in database[1].values:
            tree.insert('', 'end', next(i), values=list(item))


# Функции редактирования записей
def edit_dishes(root, tree, base, info, num):
    """
    Редактирование таблицы Блюда
    Входные данные:
        root - окно tkinter (для закрытия)
        tree - виджет treeview
        base - база данных (список из 4 таблиц pandas.DataFrame)
        info - новая информация для записи (код блюда, код заказа, блюдо,
        рецепт, состав, время приготовления, цена, объем)
        num - индекс редактируемой строки
    Выходные данные:
        -
    """
    root.destroy()
    if '' in info:
        mb.showinfo('Предупреждение', 'Запись не будет изменена, одно из полей пустое')
    else:
        if (info[0], info[1]) not in map(tuple, list(base[2][["Код блюда", "Код заказа"]].drop(num).values)):
            mb.showinfo('Предупреждение', 'Запись не будет изменена, нет такого заказа')
        else:
            base[0].loc[num, 'Код блюда'] = info[0]
            base[0].loc[num, 'Код заказа'] = info[1]
            base[0].loc[num, 'Блюдо'] = info[2]
            base[0].loc[num, 'Рецепт'] = info[3]
            base[0].loc[num, 'Состав'] = info[4]
            base[0].loc[num, 'Время приготовления'] = info[5]
            base[0].loc[num, 'Цена'] = info[6]
            base[0].loc[num, 'Объем'] = info[7]
            children = tree.get_children()
            for i in children:
                tree.delete(i)
            i = iter(base[0].index)
            for item in base[0].values:
                tree.insert('', 'end', next(i), values=list(item))
            base[3] = merging(base[0], base[1], base[2])


def edit_orders(root, tree, base, info, num):
    """
    Редактирование таблицы Заказы
    Входные данные:
        root - окно tkinter (для закрытия)
        tree - виджет treeview
        base - база данных (список из 4 таблиц pandas.DataFrame)
        info - новая информация для записи (код заказа, код сотрудника, дата заказа, номер стола, стоимость заказа)
        num - индекс редактируемой строки
    Выходные данные:
        -
    """
    root.destroy()
    if '' in info:
        mb.showinfo('Предупреждение', 'Запись не будет изменена, одно из полей пустое')
    else:
        orders = list(base[1]['Код заказа'].values)
        orders.remove(orders[num])
        if info[0] in orders:
            mb.showinfo('Предупреждение', 'Запись не будет изменена, так как уже есть такой заказ')
        elif not checking.is_date(info[2]):
            mb.showinfo('Предупреждение', 'Запись не будет изменена, неверный формат даты')
        else:
            ind = (base[1]['Код заказа'] == base[1].loc[num][0]) & (base[1]['Код сотрудника'] ==
                                                                        base[1].loc[num][1])
            for i in base[1][ind].index:
                base[1].loc[i, 'Код заказа'] = info[0]
                base[1].loc[i, 'Код сотрудника'] = info[1]
            base[1].loc[num, 'Код заказа'] = info[0]
            base[1].loc[num, 'Код сотрудника'] = info[1]
            base[1].loc[num, 'Дата заказа'] = info[2]
            base[1].loc[num, 'Номер стола'] = info[3]
            base[1].loc[num, 'Стоимость'] = info[4]
            children = tree.get_children()
            for i in children:
                tree.delete(i)
            i = iter(base[1].index)
            for item in base[1].values:
                tree.insert('', 'end', next(i), values=list(item))
            base[3] = merging(base[0], base[1], base[2])


def edit_employee(root, tree, base, info, num):
    """
    Редактирование таблицы Сотрудники
    Входные данные:
        root - окно tkinter (для закрытия)
        tree - виджет treeview
        base - база данных (список из 4 таблиц pandas.DataFrame)
        info - новая информация для записи (код, фамилия, возраст, серия и номер паспорта, адрес, номер телефона, оклад)
        num - индекс редактируемой строки
    Выходные данные:
        -
    """
    root.destroy()
    if '' in info:
        mb.showinfo('Предупреждение', 'Запись не будет изменена, одно из полей пустое')
    else:
        if not checking.is_phone(info[5]):
            mb.showinfo('Предупреждение', 'Запись не будет изменена. Неверный формат телефона')
        elif (info[0]) in map(tuple, list(base[0][["Код сотрудника"]].drop(num).values)):
            mb.showinfo('Предупреждение',
                        'Запись не будет изменена, так как уже есть такой сотрудник')
        else:
            ind = (base[0]['Код сотрудника'] == base[0].loc[num][0]) & (base[0]['Фамилия'] ==
                                                                        base[0].loc[num][1])
            for i in base[0][ind].index:
                base[0].loc[i, 'Код сотрудника'] = info[0]
                base[0].loc[i, 'Фамилия'] = info[1]
            base[0].loc[num, 'Код сотрудника'] = info[0]
            base[0].loc[num, 'Фамилия'] = info[1]
            base[0].loc[num, 'Возраст'] = info[2]
            base[0].loc[num, 'Паспорт'] = info[3]
            base[0].loc[num, 'Адрес'] = info[4]
            base[0].loc[num, 'Телефон'] = info[5]
            base[0].loc[num, 'Оклад'] = info[6]
            children = tree.get_children()
            for i in children:
                tree.delete(i)
            i = iter(base[0].index)
            for item in base[2].values:
                tree.insert('', 'end', next(i), values=list(item))
            base[3] = merging(base[0], base[1], base[2])


# Функция удаления записей
def delete_items(tree, database, number):
    """
    Удаление строк
    Входные данные:
        tree - виджет TreeView
        database - база данных (список из 4 таблиц pandas.DataFrame)
        number - номер таблицы, откуда удаляются строки
        Номера таблиц:
            0 - Сотрудники
            1 - Заказы
            2 - Блида
            3 - Полный список
    Выходные данные:
        -
    """
    items = tree.selection()
    if not items:
        mb.showerror('Ошибка', 'Не выбрана ни одна запись')
    else:
        for item in items:
            tree.delete(item)
            if number == 1:
                ind = database[0]['Код сотрудника'] == database[1].loc[int(item)][0]
                database[0] = database[0].drop(database[0][ind].index)
                ind = database[2]['Код сотрудника'] == database[1].loc[int(item)][0]
                database[2] = database[2].drop(database[2][ind].index)
            elif number == 2:
                ind = (database[0]['Код сотрудника'] == database[2].loc[int(item)][0]) & \
                      (database[0]['Код заказа'] == database[2].loc[int(item)][1])
                database[0] = database[0].drop(database[0][ind].index)
            elif number == 3:
                employee = database[3]['Код сотрудника'][int(item)]
                orders = database[3]['Код заказа'][int(item)]
                dishes = database[3]['Код блюда'][int(item)]
                if employee == '—':
                    ind = database[1]['Код заказа'] == orders
                    database[1] = database[1].drop(database[1][ind].index)
                elif dishes == '—':
                    ind = (database[2]['Код сотрудника'] == employee) & (database[2]['Код заказа'] == orders)
                    database[2] = database[2].drop(database[2][ind].index)
                else:
                    ind = (database[0]['Код сотрудника'] == employee) & (database[0]['Код заказа'] == orders)
                    database[0] = database[0].drop(database[0][ind].index)
        database[number] = database[number].drop(map(int, items))
        database[3] = merging(database[0], database[1], database[2])
        children = tree.get_children()
        for i in children:
            tree.delete(i)
        i = iter(database[number].index)
        for item in database[number].values:
            tree.insert('', 'end', next(i), values=list(item))


# Функция объединения
def merging(employees, orders, dishes):
    """
    Функция объединения таблиц
    Входные данные:
        employees, orders, dishes - 3 таблицы
    Выходные данные:
        объединённая таблицы
    """
    COL1 = ['Дата', 'Время', 'Стол', 'Стоимость', 'Фамилия', 'Код заказа',
            'Возраст', 'Паспорт', 'Адрес', 'Телефон', 'Оклад']
    COL2 = ['Дата', 'Время', 'Стол', 'Стоимость', 'Фамилия',
            'Возраст', 'Паспорт', 'Адрес', 'Телефон', 'Оклад',
            'Блюдо', 'Рецепт', 'Состав',
            'Время приготовления', 'Цена', 'Объем']
    temp = pd.merge(employees, orders, on='Код сотрудника', how='inner').fillna('—')[COL1]
    return pd.merge(dishes, temp, on='Код заказа', how='inner').fillna('—')[COL2]


# функция сортировки
def sorting(tree, base, col):
    """
    Функция сортировки таблицы по столбцу
    Входные данные:
        tree - виджет TreeView
        base - таблица pandas.DataFrame
        col - название столбца
    Выходные данные:
        -
    """
    if col == 'Дата':
        index = pd.to_datetime(base.replace('—', np.nan)[col],
                               format='%d.%m.%Y').sort_values().index
    else:
        index = base.replace('—', np.nan).sort_values(by=col).index
    children = tree.get_children()
    for i in children:
        tree.delete(int(i))
    for i in index:
        tree.insert('', 'end', i, values=list(base.loc[i]))


# Функция сохранения базы данных
def saving(base):
    """
    Сохранение базы данных
    Входные данные:
        base - база данных (список из 4 таблиц pandas.DataFrame)
    Выходные данные:
        -
    """
    path1 = fd.asksaveasfilename(initialdir=os.path.join(os.getcwd(), 'Data'),
                                 filetypes=[("Pickle (.pickle)", '*.pickle')],
                                 defaultextension=".pickle")
    if path1 != '':
        if not save_base(path1, (base[0], base[1], base[2])):
            mb.showinfo('Предупреждение',
                        'К сожалению, базу данных не удалось сохранить.\
                        Пожалуйста, попробуйте ещё раз.')


def check_base(base):
    '''
    Функция проверки, что кортеж содержит 3 отношения pandas.DataFrame
    с нужными столбцами
    Входные параметры:
        base - кортеж
    Выходные параметры:
        True/False
    '''
    columns = [('Код сотрудника', 'Фамилия', 'Возраст', 'Паспорт',
                'Адрес', 'Телефон', 'Оклад'),
               ('Код заказа', 'Код сотрудника', 'Дата', 'Время', 'Стол', 'Стоимость'),
               ('Код блюда', 'Код заказа', 'Блюдо', 'Рецепт', 'Состав', 'Время приготовления', 'Цена', 'Объем')]
    x = True
    if not (isinstance(base, tuple) and len(base) == 3):
        x = False
    else:
        for i in range(3):
            if not isinstance(base[i], pd.DataFrame):
                x = False
            elif tuple(base[i].columns) != columns[i]:
                x = False
                print(1)
    return x


def load_base(path):
    '''
    Функция открытия базы данных из формата pickle
    Входные параметры:
        path - путь к базе данных (строка)
    Выходные параметры:
        Словарь вида {base: base, error: error}
        base - кортеж из 3 баз данных pandas.DataFrame/пустой кортеж
        error - код ошибки
        Коды ошибок:
            0 - успешное считывание
            1 - не удалось считать
            2 - удалось считать, но содержимое неожиданное
    '''
    if path.endswith('.pickle') and os.path.exists(path):
        base = pd.read_pickle(path)
        if not check_base(base):
            error = 2
        else:
            error = 0
    else:
        base = ()
        error = 1
    return {'base': base, 'error': error}


def save_base(path, base):
    '''
    Функция сохранения базы данных в формате pickle
    Входные параметры:
        path - путь к файлу (строка)
        base - кортеж из 3 баз данных pandas.DataFrame
    Выходные параметры:
        True/False - результат сохранения
    '''
    if path.endswith('.pickle') and check_base(base):
        try:
            pd.to_pickle(base, path)
            x = True
        except IOError:
            x = False
    else:
        x = False
    return x
