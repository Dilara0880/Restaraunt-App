# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Модуль со служебными функциями
"""

import sys
import os
import tkinter as tk

from settings import font

tah = (font, 12)

os.chdir(os.path.abspath(os.path.join(os.getcwd(), '..')))
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'Library'))


def choosing(notebook1, notebook2):
    """
    Функция choosing перемещает выбранные столбцы из notebook1 в notebook2
    Входные данные:
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
    Выходные данные:
        -
    """
    if notebook1.curselection():
        str_num = notebook1.curselection()[0]
        st = notebook1.get(str_num)
        notebook2.insert('end', st)
        notebook1.delete(str_num)


def choosing2(notebook1, notebook2, columns):
    """
    Функция choosing2 перемещает выбранные столбцы из notebook2 в notebook1
    Входные данные:
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
        columns - выбранные столбцы
    Выходные данные:
        -
    """
    if notebook2.curselection():
        str_num = notebook2.curselection()[0]
        st = notebook2.get(str_num)
        notebook1.insert(0, st)
        new_columns = notebook1.get(0, 8)
        new_columns = [[columns.index(x), x] for x in new_columns]
        new_columns.sort()
        new_columns = [x[1] for x in new_columns]
        notebook1.delete(0, 8)
        for column in new_columns:
            notebook1.insert('end', column)
        notebook2.delete(str_num)


def help1():
    """
    Функция help1 создаёт окно со справкой
    Входные данные:
        -
    Выходные данные:
        -
    """
    # Создание окна
    root1 = tk.Toplevel()
    root1.title("Справка")
    root1.geometry('320x250+450+220')
    root1.resizable(False, False)

    # Текст
    label1 = tk.Label(root1, text='О программе:', fg="Black", bd=3, font=tah)
    label2 = tk.Label(root1, text='Разработчики:\nОразметова Дилара\nПопов Павел\n\6 бригада, группа БИВ213', fg="Black", bd=3, font=tah)
    label7 = tk.Label(root1, text='Руководитель: \nПоляков Константин Львович', fg="Black", bd=3, font=tah)
    label8 = tk.Label(root1, text='МИЭМ НИУ ВШЭ\n2022', fg="Black", bd=3, font=tah)

    # Положение элементов
    label1.grid(row=0, column=0, pady=3, padx=100)
    label2.grid(row=1, column=0, pady=3, padx=3)
    label7.grid(row=2, column=0, pady=3)
    label8.grid(row=3, column=0, pady=3)


def fact(canvas1, canvas2, combobox, entr1, entr2):
    """
    Функция fact возвращает заводские настройки
    Входные данные:
        canvas1 - отображение цвета фона
        canvas2 - отображение цвета кнопок
        combobox - список шрифтов
        entr1 - путь к сохранению тектовых отчётов
        entr2 - путь к сохранению графических отчётов
    Выходные данные:
        -
    """
    canvas1['bg'] = "#052F6D"
    canvas2['bg'] = "#6A94D4"
    combobox.set('Tahoma')
    entr1['state'] = 'normal'
    entr1.delete(0, tk.END)
    entr1.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'Output')))
    entr1['state'] = 'readonly'
    entr2['state'] = 'normal'
    entr2.delete(0, tk.END)
    entr2.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'Graphics')))
    entr2['state'] = 'readonly'


def save_configurations(path, configurations):
    '''
    Функция сохранения настроек в файл
    Входные параметры:
        path (строка) - путь к файлу настроек
        configurations (кортеж) - 5 элементов настроек:
            [0] (строка) - место сохранения текстовых отчётов
            [1] (строка) - место сохранения графических отчётов
            [2] (строка) - шрифт
            [3] (строка) - цвет фона
            [4] (строка) - цвет кнопок
    Выходные параметры:
        -
    '''
    with open(path, 'w', encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('# pylint: disable=C0103\n')
        f.write('"""\nФайл с настройками\n"""')
        f.write(f'\ntext_path = r"{configurations[0]}"')
        f.write(f'\ngraph_path = r"{configurations[1]}"')
        f.write(f'\nfont = "{configurations[2]}"')
        f.write(f'\ncfon = "{configurations[3]}"')
        f.write(f'\ncknop = "{configurations[4]}"\n')
