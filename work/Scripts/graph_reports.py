# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Модуль с функциями для графических отчётов
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def gist(ATTR1, ATTR2):
    '''
    Функция построения категоризированной гистограммы
    Входные данные:
        ATTR1 - столбец значений качественного атрибута (pandas.Series)
        ATTR2 - столбец значений количественного атрибута (pandas.Series)
    Выходные данные:
        словарь вида {'fig': fig, 'error': error}
        fig - фигура matplotlib.figure
        error - код ошибки
        Коды ошибок:
            0 - нет ошибок
            1 - неверный тип 2 столбца
            2 - мало элементов в одной из групп (плохой график)
            3 - много групп (плохой график)
    '''
    values = ATTR1.groupby(ATTR1).groups
    keys = list(values.keys())
    values = values.values()
    fig = plt.Figure()
    ax = fig.add_subplot()
    error = 0
    x = []
    ATTR1 = ATTR1.astype(str)
    if ATTR2.dtype == int or ATTR2.dtype == float:
        if len(values) >= 15:
            error = 3
        for value in values:
            if len(value) < 4 and error == 0:
                error = 2
            x.append(list(ATTR2[list(value)]))
        ax.hist(x, bins=5, density=True, histtype='bar')
        if len(values) < 15:
            ax.legend(title=ATTR1.name, labels=keys, bbox_to_anchor=(1.03, 1),
                      borderaxespad=0, loc=2)
        ax.set_xlabel(ATTR2.name)
        ax.set_ylabel('Плотность вероятности')
        ax.set_title('Категоризированная гистограмма')
        fig.set_tight_layout(True)
    else:
        error = 1
    return {'fig': fig, 'error': error}

def scatter(attr1, attr2, attr3):
    """
    Функция формирования графического отчёта диаграмма рассеивания
    Входные параметры:
    столбец значений количественного атрибута
    столбец значений количественного атрибута
    столбец значений качественных атрибута
    Выходные параметры:
    фигура
    код ошибки
    0 - фигура построена
    1 - неверный тип данных
    2 - количество данных слишком большое для построения
    """
    err = 1
    fig = plt.Figure()
    ax = fig.add_subplot()
    attr3 = attr3.astype(str)
    if attr1.dtype == float and attr2.dtype == float:
        err = 2
        data = pd.DataFrame([attr1, attr2, attr3]).T
        data[attr1.name] = data[attr1.name].astype(float)
        data[attr2.name] = data[attr2.name].astype(float)
        data = data.pivot_table(values=[attr1.name, attr2.name], index=attr3.name)
        for column in data.columns:
            data[column] = data[column].round(2)
        n = len(data)
        for i in range(n):
            ax.scatter(data[attr1.name][i], data[attr2.name][i])
        ax.set_ylabel(attr1.name)
        ax.set_xlabel(attr2.name)
        ax.set_title('Диаграмма рассеивания')
        if n < 15:
            err = 0
            ax.legend(title=attr3.name, labels=data.index, bbox_to_anchor=(1.03, 1),
                      borderaxespad=0, loc=2)
        fig.set_tight_layout(True)
    return {'fig': fig, 'error': err}

def boxplot(attr1, attr2):
    """
    Функция формирования графического отчёта диаграмма Бокса-Вискера
    Входные параметры:
    столбец значений качественного атрибута
    столбец значений количественного атрибута
    Выходные параметры:
    фигура
    код ошибки
    0 - фигура построена
    1 - неверный тип данных
    2 - количество данных слишком большое для построения
    """
    err = 1
    fig = plt.Figure()
    ax = fig.add_subplot()
    attr1 = attr1.astype(str)
    if attr2.dtype == float:
        err = 2
        data = pd.DataFrame([attr1, attr2]).T.groupby(attr1.name).groups
        num = [list(map(lambda x: attr2[x], group)) for group in data.values()]
        if len(num) <= 5:
            ax.boxplot(num)
            ax.set_ylabel(attr2.name)
            keys = list(data.keys())
            labels = [str(i) + ' - ' + keys[i - 1] for i in range(1, len(num) + 1)]
            ax.legend(title=attr1.name, labels=labels, bbox_to_anchor=(1.03, 1),
                      borderaxespad=0, loc=2)
            ax.set_title('Диаграмма Бокса-Вискера')
            err = 0
        else:
            ax.boxplot(num)
            ax.set_ylabel(attr2.name)
            ax.set_title('Диаграмма Бокса-Вискера')
    fig.set_tight_layout(True)
    return {'fig': fig, 'error': err}

def diagram(attr1, attr2):
    '''
    Столбчатая диаграмма
    Входные параметры:
        качественный атрибут
        качественный атрибут
    Выодные параметры:
        фигура
        код ошибки
        Коды ошибок:
            0 - нет ошибок
            1 - много данных
    '''
    attr1 = attr1.astype(str)
    attr2 = attr2.astype(str)
    data = pd.DataFrame([attr1, attr2]).T
    data['0'] = [0 for _ in range(len(attr1))]
    info = data.pivot_table(values='0', index=attr1.name, columns=attr2.name,
                            aggfunc='count').fillna(0)
    for i in info.columns:
        info[i] = info[i].astype(int)
    fig = plt.Figure()
    ax = fig.add_subplot()
    if len(info.columns) >= 15 or len(info) > 5:
        error = 1
    else:
        bottom = np.zeros(len(info), dtype=int)
        for column in info.columns:
            ax.bar(info.index, list(info[column].values), bottom=bottom, label=column)
            bottom += np.array(info[column].values)
        ax.legend(title=attr2.name, bbox_to_anchor=(1.03, 1), borderaxespad=0, loc=2)
        ax.set_title('Столбчатая диаграмма')
        ax.set_xlabel(attr1.name)
        ax.set_ylabel('Количество')
        fig.set_tight_layout(True)
        error = 0
    return {'fig': fig, 'error': error}