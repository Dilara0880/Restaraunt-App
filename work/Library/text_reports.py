# -*- coding: utf-8 -*-
# pylint: disable=C0103, E0110
"""
Модуль с функциями для текстовых отчётов
"""
import os
import tkinter.filedialog as fd
import pandas as pd
import Library.excel as excel
from Library.filename import time_filename

def kol_statistic(data):
    '''
    Функция построения таблицы с количественной статистикой
    Входные данные:
        data - таблица с количественными атрибутами (pandas.DataFrame)
    Выходные данные:
        Словарь вида {'stat': new_info, 'error': error}
        new_info - таблица с количественной статистикой (pandas.DataFrame)
        error - код ошибки
        Коды ошибок:
            0 - успешное проведение анализа
            1 - анализ не был проведён (ошибка типа данных)
    '''
    if not False in [x in [int, float] for x in data.dtypes]:
        new_info = pd.DataFrame({'Атрибут': '', 'Максимум': '',
                                 'Минимум': '', 'Среднее арифметическое': '',
                                 'Выборочная дисперсия': '',
                                 'Стандартное отклонение': ''}, index=[0])
        for i in range(len(data.columns)):
            column = data.columns[i]
            new_info.loc[i, 'Атрибут'] = column
            new_info.loc[i, 'Максимум'] = round(data[column].max(), 5)
            new_info.loc[i, 'Минимум'] = round(data[column].min(), 5)
            new_info.loc[i, 'Среднее арифметическое'] = round(data[column].mean(), 5)
            new_info.loc[i, 'Выборочная дисперсия'] = round(data[column].var(), 5)
            new_info.loc[i, 'Стандартное отклонение'] = round(data[column].std(), 5)
        new_info.fillna('—')
        error = 0
    else:
        new_info = pd.DataFrame()
        error = 1
    return {'stat': new_info, 'error': error}


def kach_statistic(data):
    '''
    Функция построения таблицы с количественной статистикой
    Входные данные:
        data - столбец со значениями качественной переменной (pandas.Series)
    Выходные данные:
        Словарь вида {'stat': new_info, 'error': error}
        new_info - таблица с качественной статистикой (pandas.DataFrame)
        error - код ошибки
        Коды ошибок:
            0 - успешное проведение анализа
            1 - анализ не был проведён (ошибка типа данных)
    '''
    if data.dtype == int or data.dtype == float:
        new_info = pd.DataFrame()
        error = 1
    else:
        stat1 = data.value_counts()
        stat2 = (data.value_counts(normalize=True)*100).round(2)
        stat2 = stat2.astype(str)
        for i, value in enumerate(stat2):
            stat2[i] = value + '%'
        new_info = pd.DataFrame({'Значения': stat1.index,
                                 'Частоты': stat1, 'Процент': stat2})
        error = 0
    return {'stat': new_info, 'error': error}


def pivot_table(data, values, index, columns=None):
    '''
    Функция построения сводной таблицы
    Входные данные:
        data - база данных (pandas.DataFrame)
        values - название столбца - значения для агрегирования
        index - название столбца - строка сводной таблицы
        columns - название столбца - столбец сводной таблицы
    Выходные данные:
        Словарь вида {'table': table, 'error': error}
        table - сводная таблица (pandas.DataFrame)
        error - код ошибки
        Коды ошибок:
            0 - успешное построение таблицы
            1 - таблицу не удалось построить, ошибка в названии столбцов
            2 - ошибка в типе столбца значений
    '''
    crit1 = values not in data #Нет 1 столбца
    crit2 = index not in data #Нет 2 столбца
    crit3 = columns is not None and columns not in data #Нет 3 столбца
    if crit1 or crit2 or crit3:
        error = 1
        table = pd.DataFrame()
    elif data[values].dtype == int or data[values].dtype == float:
        table = pd.pivot_table(data, values, index, columns)
        for column in table.columns:
            table[column] = table[column].round(2)
        table = table.fillna('—')
        name = index
        if columns:
            name += fr'\{columns}'
        table.insert(0, name, table.index)
        error = 0
    else:
        table = pd.DataFrame()
        error = 2
    return {'table': table, 'error': error}



def save(data, path, name):
    '''
    Функция сохранения текстового отчёта в файл Excel
    Входные данные:
        data - таблица (pandas.DataFrame)
        path - путь к папке для сохранения отчёта
        name - название текстового отчёта
    Выходные данные:
        True/False - результат сохранения
    '''
    if os.path.exists(path):
        filename = fd.asksaveasfilename(initialdir=path,
                                        initialfile=(time_filename(name) + '.xlsx'),
                                        filetypes=[("Excel files (.xlsx)", '*.xlsx')],
                                        defaultextension=".xlsx")
        if filename.endswith('.xlsx'):
            try:
                f = open(filename, 'w')
                f.close()
                with pd.ExcelWriter(filename) as f:
                    data.to_excel(f, index=False, sheet_name='Отчёт')
                    writer = f.sheets['Отчёт']
                    for i in range(len(data.columns)):
                        s = excel.index2Excel(i) #Название столбца
                        writer.set_column(':'.join([s, s]),
                                          excel.w_column(data.iloc[:, i]))
                    f.save()
                x = True
            except IOError:
                x = False
        else:
            x = False
    else:
        x = False
    return x