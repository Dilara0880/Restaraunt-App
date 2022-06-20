# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Основной модуль
"""

from tkinter import ttk
from tkinter import colorchooser
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as fd
import pandas as pd
import service
from settings import cfon, cknop, font, text_path, graph_path
import base_func
import reports
import sys
import os


path = os.getcwd()

tah = (font, 14)


def settings():
    """
    Функция settings создаёт окно настроек
    Входные данные:
        -
    Выходные данные:
        -
    """

    def factory():
        """
        Вызов функции для восстановления заводских настроек
        """
        service.fact(canvas1, canvas2, combobox, entr1, entr2)

    # Создание окна
    root2 = tk.Toplevel()
    root2.title("Настройки")
    root2.geometry('800x300+360+280')
    root2.resizable(False, False)
    root2.configure(bg=cfon)

    # Текст
    tk.Label(root2, text='Место хранения текстовых отчётов', bg=cfon,
             fg="White", bd=3, font=tah).grid(row=0, column=0, pady=1)
    tk.Label(root2, text='Место хранения графических отчётов', bg=cfon,
             fg="White", bd=3, font=tah).grid(row=1, column=0, pady=1)
    tk.Label(root2, text='Шрифт', bg=cfon, fg="White", bd=3, font=tah).grid(row=2, column=0, pady=1)
    tk.Label(root2, text='Цвет фона', bg=cfon,
             fg="White", bd=3, font=tah).grid(row=3, column=0, pady=1)
    tk.Label(root2, text='Цвет кнопок', bg=cfon,
             fg="White", bd=3, font=tah).grid(row=4, column=0, pady=1)

    # Квадраты с выбором цвета
    canvas1 = tk.Canvas(root2, width=20, height=20, bg=cfon)
    canvas1.grid(row=3, column=1, sticky='w')
    canvas2 = tk.Canvas(root2, width=20, height=20, bg=cknop)
    canvas2.grid(row=4, column=1, sticky='w')

    def background():
        """
        Вызов функции для определения цвета фона
        """
        backgr = colorchooser.askcolor()
        root2.lift()
        canvas1['bg'] = backgr[1]

    def button():
        """
        Вызов функции для определения цвета кнопок
        """
        btn = colorchooser.askcolor()
        root2.lift()
        canvas2['bg'] = btn[1]

    def dialog(entry):
        """
        Функция выбора папки
        Входные данные:
            entry - виджет Entry
        Выходные данные:
            -
        """
        new_path = fd.askdirectory(initialdir=os.getcwd())
        root2.lift()
        if new_path:
            entry['state'] = 'normal'
            entry.delete(0, 'end')
            entry.insert(0, os.path.normpath(new_path))
            entry['state'] = 'readonly'

    def save_set():
        """
        Функция сохранения настроек
        """
        service.save_configurations(r'.\scripts\settings.py',
                                    (entr1.get(), entr2.get(), combobox.get(),
                                     canvas1['bg'], canvas2['bg']))
        root2.destroy()

    # Кнопки
    tk.Button(root2, text="...", bg=cknop, fg="Black", bd=3,
              font=tah, command=lambda: dialog(entr1)).grid(row=0, column=2, padx=10)
    tk.Button(root2, text="...", bg=cknop, fg="Black", bd=3,
              font=tah, command=lambda: dialog(entr2)).grid(row=1, column=2, padx=10)
    tk.Button(root2, text="Выбрать цвет", bg=cknop, fg="Black", bd=3,
              font=tah, command=background).grid(row=3, column=1, padx=10)
    tk.Button(root2, text="Выбрать цвет", bg=cknop, fg="Black", bd=3,
              font=tah, command=button).grid(row=4, column=1, padx=10)
    tk.Button(root2, text="Настройки по умолчанию", bg=cknop, fg="Black", bd=3,
              font=tah, command=factory).grid(row=5, column=0, padx=10)
    tk.Button(root2, text="Сохранить", bg=cknop, fg="Black", bd=3,
              font=tah, command=save_set).grid(row=5, column=1, padx=10, sticky='e', pady=30)

    # Ввод данных
    entr1 = tk.Entry(root2, font=tah, width=30)
    entr1.insert(0, text_path)
    entr1['state'] = 'readonly'
    entr2 = tk.Entry(root2, font=tah, width=30)
    entr2.insert(0, graph_path)
    entr2['state'] = 'readonly'

    # Раскрывающийся список
    combobox = ttk.Combobox(root2, state='readonly', width=28, font=tah)
    combobox['values'] = ['Tahoma', 'Calibri', 'Times New Roman', 'Arial']
    combobox.set(font)

    entr1.grid(row=0, column=1)
    entr2.grid(row=1, column=1)
    combobox.grid(row=2, column=1)


def column(notebook1, notebook2, columns):
    """
    Функция column выводит список столбцов открытой таблицы в notebook2
    Входные данные:
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
        columns - выбранные столбцы
    Выходные данные:
        -
    """

    def choosing_1(ev):
        """
        Вызов функции для перемещения данных из notebook1 в notebook2
        """
        service.choosing(notebook1, notebook2)

    def choosing_2(ev):
        """
        Вызов функции для перемещения данных из notebook2 в notebook1
        """
        service.choosing2(notebook1, notebook2, columns)

    notebook1.delete(0, 8)
    notebook2.delete(0, 8)
    for clmn in columns:
        notebook1.insert('end', clmn)
    notebook1.bind('<Button-1>', choosing_1)
    notebook2.bind("<Button-1>", choosing_2)


def table_employee(buttons, tree, base, notebook1, notebook2):
    """
    Функция table_cash выводит таблицу с окладом сотрудника
    Входные данные:
        buttons - список кнопок
        tree - виджет таблицы
        base - база данных
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
    Выходные данные:
        -
    """
    chart = base[0]
    but4 = buttons[0]
    but5 = buttons[1]
    but6 = buttons[2]
    but7 = buttons[3]
    children = tree.get_children()
    for i in children:
        tree.delete(i)
    tree.grid_forget()
    # Таблица
    tree['columns'] = ['code', 'surname', 'age', 'passport', 'address', 'phone', 'salary']
    tree.column('code', width=70, anchor=tk.CENTER)
    tree.column('surname', width=220, anchor=tk.CENTER)
    tree.column('age', width=120, anchor=tk.CENTER)
    tree.column('passport', width=200, anchor=tk.CENTER)
    tree.column('address', width=200, anchor=tk.CENTER)
    tree.column('phone', width=200, anchor=tk.CENTER)
    tree.column('salary', width=140, anchor=tk.CENTER)
    tree.heading('code', text='Код', command=lambda: base_func.sorting(tree, base[0], 'Код сотрудника'))
    tree.heading('surname', text='Фамилия сотрудника', command=lambda: base_func.sorting(tree, base[0], 'Фамилия'))
    tree.heading('age', text='Возраст', command=lambda: base_func.sorting(tree, base[0], 'Возраст'))
    tree.heading('passport', text='Паспорт', command=lambda: base_func.sorting(tree, base[0], 'Паспорт'))
    tree.heading('address', text='Адрес', command=lambda: base_func.sorting(tree, base[0], 'Адрес'))
    tree.heading('phone', text='Телефон', command=lambda: base_func.sorting(tree, base[0], 'Телефон'))
    tree.heading('salary', text='Оклад', command=lambda: base_func.sorting(tree, base[0], 'Оклад'))
    tree.grid(row=4, column=0, columnspan=7, sticky='nsew', padx=2)
    i = iter(chart.index)
    for item in chart.values:
        tree.insert('', 'end', next(i), values=list(item))
    # Скроллбар
    vscrollbar = tk.Scrollbar(orient='vertical', command=tree.yview)
    tree['yscrollcommand'] = vscrollbar.set
    vscrollbar.grid(row=4, column=6, sticky='nse')

    # Цвет кнопки
    but4.configure(bg="White")
    but5.configure(bg=cknop)
    but6.configure(bg=cknop)
    but7.configure(bg=cknop)

    # Выбор столбцов
    columns = ('Код сотрудника', 'Фамилия', 'Возраст', 'Паспорт', 'Адрес',
               'Телефон', 'Оклад')
    column(notebook1, notebook2, columns)


def table_orders(buttons, tree, base, notebook1, notebook2):
    """
    Функция table_orders выводит таблицу обслуженных заказов
    Входные данные:
        buttons - список кнопок
        tree - виджет таблицы
        base - база данных
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
    Выходные данные:
        -
    """
    chart = base[1]
    but4 = buttons[0]
    but5 = buttons[1]
    but6 = buttons[2]
    but7 = buttons[3]
    children = tree.get_children()
    for i in children:
        tree.delete(i)
    tree.grid_forget()
    # Таблица
    tree['columns'] = ['order', 'worker', 'date', 'time', 'table', 'cost']
    tree.column('order', width=250, anchor=tk.CENTER)
    tree.column('worker', width=200, anchor=tk.CENTER)
    tree.column('date', width=200, anchor=tk.CENTER)
    tree.column('time', width=200, anchor=tk.CENTER)
    tree.column('table', width=100, anchor=tk.CENTER)
    tree.column('cost', width=200, anchor=tk.CENTER)
    tree.heading('order', text='Код заказа', command=lambda: base_func.sorting(tree, base[1], 'Код заказа'))
    tree.heading('worker', text='Код сотрудника', command=lambda: base_func.sorting(tree, base[1], 'Код сотрудника'))
    tree.heading('date', text='Дата заказа', command=lambda: base_func.sorting(tree, base[1], 'Дата'))
    tree.heading('time', text='Время заказа', command=lambda: base_func.sorting(tree, base[1], 'Время'))
    tree.heading('table', text='Номер стола', command=lambda: base_func.sorting(tree, base[1], 'Стол'))
    tree.heading('cost', text='Стоимость заказа', command=lambda: base_func.sorting(tree, base[1], 'Стоимость'))
    tree.grid(row=4, column=0, columnspan=7, sticky='nsew', padx=2)
    i = iter(chart.index)
    for item in chart.values:
        tree.insert('', 'end', next(i), values=list(item))
    # Скроллбар
    vscrollbar = tk.Scrollbar(orient='vertical', command=tree.yview)
    tree['yscrollcommand'] = vscrollbar.set
    vscrollbar.grid(row=4, column=6, sticky='nse')

    # Цвет кнопки
    but4.configure(bg=cknop)
    but5.configure(bg="White")
    but6.configure(bg=cknop)
    but7.configure(bg=cknop)

    # Выбор столбцов
    columns = ('Код заказа', 'Код сотрудника', 'Дата заказа',
               'Время заказа', 'Номер стола', 'Стоимость заказа')
    column(notebook1, notebook2, columns)


def table_dishes(buttons, tree, base, notebook1, notebook2):
    """
    Функция table_dishes выводит таблицу блюд
    Входные данные:
        buttons - список кнопок
        tree - виджет таблицы
        base - база данных
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
    Выходные данные:
        -
    """
    chart = base[2]
    but4 = buttons[0]
    but5 = buttons[1]
    but6 = buttons[2]
    but7 = buttons[3]
    # Таблица
    children = tree.get_children()
    for i in children:
        tree.delete(i)
    tree.grid_forget()
    tree['columns'] = ['code', 'order', 'dish', 'recipe', 'components', 'time', 'price', 'volume']
    tree.column('code', width=120, anchor=tk.CENTER)
    tree.column('order', width=120, anchor=tk.CENTER)
    tree.column('dish', width=180, anchor=tk.CENTER)
    tree.column('recipe', width=120, anchor=tk.CENTER)
    tree.column('components', width=300, anchor=tk.CENTER)
    tree.column('time', width=110, anchor=tk.CENTER)
    tree.column('price', width=100, anchor=tk.CENTER)
    tree.column('volume', width=100, anchor=tk.CENTER)
    tree.heading('code', text='Код блюда', command=lambda: base_func.sorting(tree, base[2], 'Код блюда'))
    tree.heading('order', text='Код заказа', command=lambda: base_func.sorting(tree, base[2], 'Код заказа'))
    tree.heading('dish', text='Наименование блюда', command=lambda: base_func.sorting(tree, base[2], 'Блюдо'))
    tree.heading('recipe', text='Рецепт', command=lambda: base_func.sorting(tree, base[2], 'Рецепт'))
    tree.heading('components', text='Состав', command=lambda: base_func.sorting(tree, base[2], 'Состав'))
    tree.heading('time', text='Время приготовления', command=lambda: base_func.sorting(tree, base[2], 'Время приготовления'))
    tree.heading('price', text='Цена', command=lambda: base_func.sorting(tree, base[2], 'Цена'))
    tree.heading('volume', text='Объем', command=lambda: base_func.sorting(tree, base[2], 'Объем'))
    tree.grid(row=4, column=0, columnspan=7, sticky='nsew', padx=2)
    i = iter(chart.index)
    for item in chart.values:
        tree.insert('', 'end', next(i), values=list(item))
    # Скроллбар
    vscrollbar = tk.Scrollbar(orient='vertical', command=tree.yview)
    tree['yscrollcommand'] = vscrollbar.set
    vscrollbar.grid(row=4, column=6, sticky='nse')

    # Цвет кнопки
    but4.configure(bg=cknop)
    but5.configure(bg=cknop)
    but6.configure(bg="White")
    but7.configure(bg=cknop)

    # Выбор столбцов
    columns = ('Код блюда', 'Код заказа', 'Наименование блюда', 'Рецепт', 'Состав', 'Время приготовления', 'Цена', 'Объем')
    column(notebook1, notebook2, columns)


def table(buttons, tree, base, notebook1, notebook2):
    """
    Функция table выводит полный список
    Входные данные:
        buttons - список кнопок
        tree - виджет таблицы
        base - база данных
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
    Выходные данные:
        -
    """
    chart = base[3]
    but4 = buttons[0]
    but5 = buttons[1]
    but6 = buttons[2]
    but7 = buttons[3]
    # Таблица
    children = tree.get_children()
    for i in children:
        tree.delete(i)
    tree.grid_forget()
    tree['columns'] = ['date', 'time', 'table', 'cost', 'surname',
                       'age', 'passport', 'address', 'phone', 'salary',
                       'dish', 'recipe', 'components', 'prep_time', 'price', 'volume']
    tree.column('date', width=100, anchor=tk.CENTER)
    tree.column('time', width=70, anchor=tk.CENTER)
    tree.column('table', width=30, anchor=tk.CENTER)
    tree.column('cost', width=40, anchor=tk.CENTER)
    tree.column('surname', width=70, anchor=tk.CENTER)
    tree.column('age', width=30, anchor=tk.CENTER)
    tree.column('passport', width=70, anchor=tk.CENTER)
    tree.column('address', width=100, anchor=tk.CENTER)
    tree.column('phone', width=70, anchor=tk.CENTER)
    tree.column('salary', width=50, anchor=tk.CENTER)
    tree.column('dish', width=100, anchor=tk.CENTER)
    tree.column('recipe', width=90, anchor=tk.CENTER)
    tree.column('components', width=100, anchor=tk.CENTER)
    tree.column('prep_time', width=60, anchor=tk.CENTER)
    tree.column('price', width=60, anchor=tk.CENTER)
    tree.column('volume', width=60, anchor=tk.CENTER)
    tree.heading('date', text='Дата заказа', command=lambda: base_func.sorting(tree, base[3], 'Дата'))
    tree.heading('time', text='Время',command=lambda: base_func.sorting(tree, base[3], 'Время'))
    tree.heading('table', text='Номер стола', command=lambda: base_func.sorting(tree, base[3], 'Стол'))
    tree.heading('cost', text='Стоимость заказа', command=lambda: base_func.sorting(tree, base[3], 'Стоимость'))
    tree.heading('surname', text='Фамилия сотрудника', command=lambda: base_func.sorting(tree, base[3], 'Фамилия'))
    tree.heading('age', text='Возраст', command=lambda: base_func.sorting(tree, base[3], 'Возраст'))
    tree.heading('passport', text='Паспорт', command=lambda: base_func.sorting(tree, base[3], 'Паспорт'))
    tree.heading('address', text='Адрес', command=lambda: base_func.sorting(tree, base[3], 'Адрес'))
    tree.heading('phone', text='Номер телефона', command=lambda: base_func.sorting(tree, base[3], 'Номер'))
    tree.heading('salary', text='Оклад', command=lambda: base_func.sorting(tree, base[3], 'Оклад'))
    tree.heading('dish', text='Наименование блюда', command=lambda: base_func.sorting(tree, base[3], 'Блюдо'))
    tree.heading('recipe', text='Рецепт', command=lambda: base_func.sorting(tree, base[3], 'Рецепт'))
    tree.heading('components', text='Состав', command=lambda: base_func.sorting(tree, base[3], 'Состав'))
    tree.heading('prep_time', text='Время приготовления', command=lambda: base_func.sorting(tree, base[3], 'Время приготовления'))
    tree.heading('price', text='Цена', command=lambda: base_func.sorting(tree, base[3], 'Цена'))
    tree.heading('volume', text='Объем', command=lambda: base_func.sorting(tree, base[3], 'Объем'))
    tree.grid(row=4, column=0, columnspan=7, sticky='nsew', padx=2)
    i = iter(chart.index)
    for item in chart.values:
        tree.insert('', 'end', next(i), values=list(item))

    # Скроллбар
    vscrollbar = tk.Scrollbar(orient='vertical', command=tree.yview)
    tree['yscrollcommand'] = vscrollbar.set
    vscrollbar.grid(row=4, column=6, sticky='nse')

    # Цвет кнопки
    but4.configure(bg=cknop)
    but5.configure(bg=cknop)
    but6.configure(bg=cknop)
    but7.configure(bg="White")

    # Выбор столбцов
    columns = ('Дата', 'Время', 'Стол', 'Стоимость', 'Фамилия',
               'Возраст', 'Паспорт', 'Адрес', 'Телефон', 'Оклад',
               'Наименование блюда', 'Рецепт', 'Состав',
               'Время приготовления', 'Цена', 'Объем')
    column(notebook1, notebook2, columns)


def opening(base, buttons, tree, notebook1, notebook2):
    """
    Открытие базы данных
    Входные данные:
        base - список из таблиц
        buttons - список кнопок
        tree - виджет таблицы
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
    Выходные данные:
        -
    """
    path2 = fd.askopenfilename(initialdir=os.path.join(os.getcwd(), 'Data'),
                               filetypes=[("Pickle (.pickle)", '*.pickle')],
                               defaultextension=".pickle")
    if path2:
        temp = base_func.load_base(path2)
        if temp['error'] == 1:
            mb.showerror('Ошибка', 'Не удалось загрузить базу данных')
        elif temp['error'] == 2:
            mb.showerror('Ошибка', 'Неожиданное содержимое базы данных')
        else:
            base[0] = temp['base'][0]
            base[1] = temp['base'][1]
            base[2] = temp['base'][2]
            base[3] = base_func.merging(base[0], base[1], base[2])
            k = color(buttons[0], buttons[1], buttons[2])
            func = (table_employee, table_orders, table_dishes,
                    table)[k - 1]
            func(buttons, tree, base, notebook1, notebook2)

def menu(root, base, buttons, tree, note):
    """
    Функция menu создаёт меню в главном окне
    Входные данные:
        root - окно tkinter
        base - база данных
        buttons - список кнопок
        tree - виджет таблицы
        note - кортеж Listbox
    Выходные данные:
        -
    """
    mainMenu = tk.Menu(root)
    file_m = tk.Menu(mainMenu, tearoff=0)
    mainMenu.add_cascade(label='Файл', menu=file_m)
    file_m.add_command(label='Открыть файл', command=lambda: opening(base, buttons, tree, note[0], note[1]))
    file_m.add_command(label='Сохранить файл', command=lambda: base_func.saving(base))
    mainMenu.add_command(label='Настройки', command=settings)
    mainMenu.add_command(label='Справка', command=service.help1)
    root.config(menu=mainMenu)


def dob_orders(root, x, tree, database):
    """
    Функция dob_orders создаёт окно добавления и редактирования записей для таблицы "Заказы"
    Входные данные:
        root - окно tkinter
        x - параметр выбора добавления или удаления записи
        tree - виджет таблицы
        base - база данных
    Выходные данные:
        -
    """
    # Создание окна
    root4 = tk.Toplevel(root)
    if x == 1:
        root4.title("Добавление новой записи")
    else:
        root4.title("Изменение записи")
    root4.geometry('400x290+350+200')
    root4.resizable(False, False)
    root4.configure(bg=cfon)

    # Ввод текста
    entr1 = tk.Entry(root4, font=tah, width=33)
    entr2 = tk.Entry(root4, font=tah, width=33)
    entr3 = tk.Entry(root4, font=tah, width=33)
    entr4 = tk.Entry(root4, font=tah, width=33)
    entr5 = tk.Entry(root4, font=tah, width=33)
    entr6 = tk.Entry(root4, font=tah, width=33)


    # Текст
    label1 = tk.Label(root4, text='Код заказа', bg=cfon, fg="White", bd=3, font=tah)
    label2 = tk.Label(root4, text='Код сотрудника', bg=cfon, fg="White", bd=3, font=tah)
    label3 = tk.Label(root4, text='Дата заказа', bg=cfon, fg="White", bd=3, font=tah)
    label4 = tk.Label(root4, text='Время заказа', bg=cfon, fg="White", bd=3, font=tah)
    label5 = tk.Label(root4, text='Номер стола', bg=cfon, fg="White", bd=3, font=tah)
    label6 = tk.Label(root4, text='Стоимость', bg=cfon, fg="White", bd=3, font=tah)

    # Кнопка
    but = tk.Button(root4, text="ОK", bg=cknop, fg="Black", bd=3,
                    font=tah, width=10, height=1)
    but['command'] = lambda: base_func.add_order(tree, database,
                                                    [entr1.get(), entr2.get(),
                                                     entr3.get(), entr4.get(),
                                                     entr5.get(), entr6.get()])
    # Расположение элементов
    but.grid(row=6, column=0, pady=10, padx=20, columnspan=2)
    entr1.grid(row=0, column=1, pady=1)
    entr2.grid(row=1, column=1, pady=1)
    entr3.grid(row=2, column=1, pady=1)
    entr4.grid(row=3, column=1, pady=1)
    entr5.grid(row=4, column=1, pady=1)
    entr6.grid(row=5, column=1, pady=1)
    label1.grid(row=0, column=0, pady=1, padx=5)
    label2.grid(row=1, column=0, pady=1, padx=5)
    label3.grid(row=2, column=0, pady=1, padx=5)
    label4.grid(row=3, column=0, pady=1, padx=5)
    label5.grid(row=4, column=0, pady=1, padx=5)
    label6.grid(row=5, column=0, pady=1, padx=5)
    if x != 1 and len(tree.selection()) != 1:
        root4.destroy()
        mb.showerror('Ошибка', 'Для редактирования записи надо выбрать одну запись')
    elif x != 1:
        num = int(tree.selection()[0])
        entr1.delete(0, tk.END)
        entr1.insert(0, database[0].loc[num]['Код заказа'])
        entr2.delete(0, tk.END)
        entr2.insert(0, database[0].loc[num]['Код сотрудника'])
        entr3.delete(0, tk.END)
        entr3.insert(0, database[0].loc[num]['Дата'])
        entr4.delete(0, tk.END)
        entr4.insert(0, database[0].loc[num]['Время'])
        entr5.delete(0, tk.END)
        entr5.insert(0, database[0].loc[num]['Стол'])
        entr6.delete(0, tk.END)
        entr6.insert(0, database[0].loc[num]['Стоимость'])
        but['command'] = lambda: base_func.edit_employee(root4, tree, database,
                                                         [entr1.get(), entr2.get(),
                                                          entr3.get(), entr4.get(),
                                                          entr5.get(), entr6.get()], num)


def dob_dishes(root, x, tree, base):
    """
    Функция dob_dishes создаёт окно добавления и редактирования записей для таблицы "Блюда"
    Входные данные:
        root - окно tkinter
        x - параметр выбора добавления или удаления записи
        tree - виджет таблицы
        base - база данных
    Выходные данные:
        -
    """
    # Создание окна
    root4 = tk.Toplevel(root)
    if x == 1:
        root4.title("Добавление новой записи")
    else:
        root4.title("Изменение записи")
    root4.geometry('550x300+350+200')
    root4.resizable(False, False)
    root4.configure(bg=cfon)

    # Ввод текста
    entr1 = tk.Entry(root4, font=tah, width=30)
    entr2 = tk.Entry(root4, font=tah, width=30)
    entr3 = tk.Entry(root4, font=tah, width=30)
    entr4 = tk.Entry(root4, font=tah, width=30)
    entr5 = tk.Entry(root4, font=tah, width=30)
    entr6 = tk.Entry(root4, font=tah, width=30)
    entr7 = tk.Entry(root4, font=tah, width=30)
    entr8 = tk.Entry(root4, font=tah, width=30)

    # Текст
    label1 = tk.Label(root4, text='Код блюда', bg=cfon, fg="White", bd=3, font=tah)
    label2 = tk.Label(root4, text='Код заказа', bg=cfon, fg="White", bd=3, font=tah)
    label3 = tk.Label(root4, text='Блюдо', bg=cfon, fg="White", bd=3, font=tah)
    label4 = tk.Label(root4, text='Рецепт', bg=cfon, fg="White", bd=3, font=tah)
    label5 = tk.Label(root4, text='Состав', bg=cfon, fg="White", bd=3, font=tah)
    label6 = tk.Label(root4, text='Время приготовления', bg=cfon, fg="White", bd=3, font=tah)
    label7 = tk.Label(root4, text='Цена', bg=cfon, fg="White", bd=3, font=tah)
    label8 = tk.Label(root4, text='Объем', bg=cfon, fg="White", bd=3, font=tah)

    # Кнопка
    but = tk.Button(root4, text="ОК", bg=cknop, fg="Black", bd=5,
                    font=tah, width=10, height=1,
                    command=lambda: base_func.add_dish(tree, base,
                                                        [entr1.get(), entr2.get(), entr3.get(),
                                                         entr4.get(), entr5.get(), entr6.get(),
                                                         entr7.get(), entr8.get()]))

    # Расположение элементов
    but.grid(row=8, column=0, pady=10, padx=20, columnspan=2)
    entr1.grid(row=0, column=1, pady=1)
    entr2.grid(row=1, column=1, pady=1)
    entr3.grid(row=2, column=1, pady=1)
    entr4.grid(row=3, column=1, pady=1)
    entr5.grid(row=4, column=1, pady=1)
    entr6.grid(row=5, column=1, pady=1)
    entr7.grid(row=6, column=1, pady=1)
    entr8.grid(row=7, column=1, pady=1)

    label1.grid(row=0, column=0, pady=1, padx=5)
    label2.grid(row=1, column=0, pady=1, padx=5)
    label3.grid(row=2, column=0, pady=1, padx=5)
    label4.grid(row=3, column=0, pady=1, padx=5)
    label5.grid(row=4, column=0, pady=1, padx=5)
    label6.grid(row=5, column=0, pady=1, padx=5)
    label7.grid(row=6, column=0, pady=1, padx=5)
    label8.grid(row=7, column=0, pady=1, padx=5)
    if x != 1 and len(tree.selection()) != 1:
        root4.destroy()
        mb.showerror('Ошибка', 'Для редактирования записи надо выбрать одну запись')
    elif x != 1:
        num = int(tree.selection()[0])
        entr1.delete(0, tk.END)
        entr1.insert(0, base[1].loc[num]['Код блюда'])
        entr2.delete(0, tk.END)
        entr2.insert(0, base[1].loc[num]['Код заказа'])
        entr3.delete(0, tk.END)
        entr3.insert(0, base[1].loc[num]['Блюдо'])
        entr4.delete(0, tk.END)
        entr4.insert(0, base[1].loc[num]['Рецепт'])
        entr5.delete(0, tk.END)
        entr5.insert(0, base[1].loc[num]['Состав'])
        entr6.delete(0, tk.END)
        entr6.insert(0, base[1].loc[num]['Время приготовления'])
        entr7.delete(0, tk.END)
        entr7.insert(0, base[1].loc[num]['Цена'])
        entr8.delete(0, tk.END)
        entr8.insert(0, base[1].loc[num]['Объем'])
        but['command'] = lambda: base_func.edit_dishes(root4, tree, base,
                                                       [entr1.get(), entr2.get(), entr3.get(),
                                                       entr4.get(), entr5.get(), entr6.get(),
                                                        entr7.get(), entr8.get()], num)


def dob_employee(root, x, tree, database):
    """
    Функция dob_employee создаёт окно добавления и редактирования записей для таблицы "сотрудники"
    Входные данные:
        root - окно tkinter
        x - параметр выбора добавления или удаления записи
        tree - виджет таблицы
        database - база данных
    Выходные данные:
        -
    """
    # Создание окна
    root4 = tk.Toplevel(root)
    if x == 1:
        root4.title("Добавление новой записи")
    else:
        root4.title("Изменение записи")
    root4.geometry('400x290+350+200')
    root4.resizable(False, False)
    root4.configure(bg=cfon)

    # Ввод текста
    entr1 = tk.Entry(root4, font=tah, width=33)
    entr2 = tk.Entry(root4, font=tah, width=33)
    entr3 = tk.Entry(root4, font=tah, width=33)
    entr4 = tk.Entry(root4, font=tah, width=33)
    entr5 = tk.Entry(root4, font=tah, width=33)
    entr6 = tk.Entry(root4, font=tah, width=33)
    entr7 = tk.Entry(root4, font=tah, width=33)
    entr6.insert(0, '999-999-9999')


    # Текст
    label1 = tk.Label(root4, text='Код сотрудника', bg=cfon, fg="White", bd=3,
                      font=tah)
    label2 = tk.Label(root4, text='Фамилия', bg=cfon, fg="White", bd=3,
                      font=tah)
    label3 = tk.Label(root4, text='Возраст', bg=cfon, fg="White", bd=3,
                      font=tah)
    label4 = tk.Label(root4, text='Паспорт', bg=cfon, fg="White", bd=3,
                      font=tah)
    label5 = tk.Label(root4, text='Адрес', bg=cfon, fg="White", bd=3,
                      font=tah)
    label6 = tk.Label(root4, text='Телефон', bg=cfon, fg="White", bd=3,
                      font=tah)
    label7 = tk.Label(root4, text='Оклад', bg=cfon, fg="White", bd=3,
                      font=tah)

    # Кнопка
    but = tk.Button(root4, text="Ок", bg=cknop, fg="Black", bd=3,
                    font=tah, width=10, height=1)
    but['command'] = lambda: base_func.add_employee(tree, database,
                                                 [entr1.get(), entr2.get(),
                                                  entr3.get(), entr4.get(),
                                                  entr5.get(), entr6.get(),
                                                  entr7.get()])
    # Расположение элементов
    but.grid(row=7, column=0, pady=10, padx=20, columnspan=2)
    entr1.grid(row=0, column=1, pady=1)
    entr2.grid(row=1, column=1, pady=1)
    entr3.grid(row=2, column=1, pady=1)
    entr4.grid(row=3, column=1, pady=1)
    entr5.grid(row=4, column=1, pady=1)
    entr6.grid(row=5, column=1, pady=1)
    entr7.grid(row=6, column=1, pady=1)
    label1.grid(row=0, column=0, pady=1, padx=5)
    label2.grid(row=1, column=0, pady=1, padx=5)
    label3.grid(row=2, column=0, pady=1, padx=5)
    label4.grid(row=3, column=0, pady=1, padx=5)
    label5.grid(row=4, column=0, pady=1, padx=5)
    label6.grid(row=5, column=0, pady=1, padx=5)
    label7.grid(row=6, column=0, pady=1, padx=5)
    if x != 1 and len(tree.selection()) != 1:
        root4.destroy()
        mb.showerror('Ошибка', 'Для редактирования записи надо выбрать одну запись')
    elif x != 1:
        num = int(tree.selection()[0])
        entr1.delete(0, tk.END)
        entr1.insert(0, database[0].loc[num]['Код сотрудника'])
        entr2.delete(0, tk.END)
        entr2.insert(0, database[0].loc[num]['Фамилия'])
        entr3.delete(0, tk.END)
        entr3.insert(0, database[0].loc[num]['Возраст'])
        entr4.delete(0, tk.END)
        entr4.insert(0, database[0].loc[num]['Паспорт'])
        entr5.delete(0, tk.END)
        entr5.insert(0, database[0].loc[num]['Адрес'])
        entr6.delete(0, tk.END)
        entr6.insert(0, database[0].loc[num]['Телефон'])
        entr7.delete(0, tk.END)
        entr7.insert(0, database[0].loc[num]['Оклад'])
        but['command'] = lambda: base_func.edit_employee(root4, tree, database,
                                                        [entr1.get(), entr2.get(),
                                                         entr3.get(), entr4.get(),
                                                         entr5.get(), entr6.get(),
                                                         entr7.get()], num)
def color(but4, but5, but6):
    """
    Функция color узнаёт, какая таблица сейчас открыта
    Входные данные:
        but4, but5, but6 - три кнопки вызова таблиц
    Выходные данные:
        tek - номер открытой таблицы
    """
    if but4['bg'] == "White":
        tek = 1
    elif but5['bg'] == "White":
        tek = 2
    elif but6['bg'] == "White":
        tek = 3
    else:
        tek = 4
    return tek


def knopki(root, combobox, base, notebook1, notebook2):
    """
    Функция knopki создаёт кнопки и таблицу на главном окне
    Входные данные:
        root - окно tkinter
        combobox - раскрывающийся список с видами отчётов
        base - база данных
        notebook1 - список всех столбцов
        notebook2 - список выбранных столбцов
    Выходные данные:
        список кнопок
    """

    def func1(func, param):
        """
        Настройка кнопок и прорисовка окна
        Входные данные:
            func - функция вывода соответствующего окна
            param - номер таблицы
        Выходные данные:
            -
        """
        func([but4, but5, but6, but7], tree, base, notebook1, notebook2)
        if param < 3:
            but2['command'] = lambda: (dob_employee, dob_orders,
                                       dob_dishes)[param](root, 1, tree, base)
            but3['command'] = lambda: (dob_employee, dob_orders,
                                       dob_dishes)[param](root, 0, tree, base)
        else:
            but2['command'] = lambda: mb.showinfo(r'Предупреждение',
                                                  'В полную таблицу нельзя добавлять данные.\
                           Пользуйтесь другими таблицами для добавления.')
            but3['command'] = lambda: mb.showinfo('Предупреждение',
                                                  'В полной таблице нельзя делать изменения.\
                           Пользуйтесь другими таблицами для редактирования')

    def analiz1():
        """
        Вызов функции для построения отчёта
        """
        reports.analyze(combobox.get(), base[color(but4, but5, but6) - 1], notebook2.get(0, 'end'),
                        tree.selection())

    # Кнопки
    tk.Button(root, text="Удалить выбранные записи", bg=cknop, fg="Black", bd=3, font=tah,
              command=lambda: base_func.delete_items(tree, base, color(but4, but5,
                                                           but6) - 1)).grid(row=0, column=0,
                                                                            columnspan=4, pady=1)
    but2 = tk.Button(root, text="Добавить запись", bg=cknop, fg="Black", bd=3,
                     font=tah)
    but3 = tk.Button(root, text="Редактировать запись", bg=cknop, fg="Black", bd=3,
                     font=tah)
    but5 = tk.Button(root, text="Заказы", bg=cknop, fg="Black", bd=3,
                     font=tah, command=lambda: func1(table_orders, 0))
    but6 = tk.Button(root, text="Блюда", bg=cknop, fg="Black", bd=3,
                     font=tah, command=lambda: func1(table_dishes, 1))
    but4 = tk.Button(root, text="Сотрудники", bg=cknop, fg="Black", bd=3,
                     font=tah, command=lambda: func1(table_employee, 2))
    but7 = tk.Button(root, text="Полный список", bg=cknop, fg="Black", bd=3,
                     font=tah, command=lambda: func1(table, 3))
    but8 = tk.Button(root, text="Проанализировать", bg=cknop, fg="Black", bd=3,
                     font=tah, command=analiz1)
    but2.grid(row=1, column=0, columnspan=4, pady=1)
    but3.grid(row=2, column=0, columnspan=4, pady=1)
    but4.grid(row=3, column=0, padx=2, pady=20)
    but5.grid(row=3, column=1, padx=1)
    but6.grid(row=3, column=2, padx=1)
    but7.grid(row=3, column=3, padx=1)
    but8.grid(row=2, column=6, columnspan=4, padx=25)
    # Таблица
    tree = ttk.Treeview(root, selectmode="extended", height=20, show='headings')
    func1(table_employee, 0)
    return [but4, but5, but6, but7, tree]


def main_window():
    """
    Функция main_window создаёт главное окно
    Входные данные:
        -
    Выходные данные:
        -
    """
    # Создание окна
    root = tk.Tk()
    root.title("Главное окно")
    root.geometry('1135x610+60+10')
    root.resizable(False, False)
    root.configure(bg=cfon)
    temp = base_func.load_base(os.path.join(os.getcwd(), 'Data', 'database.pickle'))
    columns = [('Код сотрудника', 'Фамилия', 'Возраст', 'Паспорт',
                'Адрес', 'Телефон', 'Оклад'),
               ('Код заказа', 'Код сотрудника', 'Дата', 'Время',
                'Стол', 'Стоимость'),
               ('Код блюда', 'Код заказа', 'Блюдо', 'Рецепт', 'Состав',
                'Время приготовления', 'Цена', 'Объем')]
    employees = pd.DataFrame(columns=columns[1])
    orders = pd.DataFrame(columns=columns[2])
    dishes = pd.DataFrame(columns=columns[0])
    if temp['error'] == 1:
        mb.showerror('Ошибка', 'Не удалось загрузить базу данных')
    elif temp['error'] == 2:
        mb.showerror('Ошибка', 'Неожиданное содержимое базы данных')
    else:
        employees = temp['base'][0]
        orders = temp['base'][1]
        dishes = temp['base'][2]
    all_tables = base_func.merging(employees, orders, dishes)
    base = [employees, orders, dishes, all_tables]

    # Выбор столбцов
    notebook1 = tk.Listbox(root, height=9, width=18)
    notebook2 = tk.Listbox(root, height=9, width=18, selectmode=tk.EXTENDED)
    note = [notebook1, notebook2]


    # Раскрывающийся список
    combobox = ttk.Combobox(root, state='readonly', width=25, font=tah)
    combobox['values'] = ['Простой текстовый отчёт', 'Текстовый статистический отчёт',
                          'Диаграмма рассеивания', 'Сводная таблица (среднее значение)',
                          'Столбчатая диаграмма', 'Категоризированная гистограмма',
                          'Диаграмма Бокса-Вискера']
    combobox.set('Выберите тип отчета')
    # Кнопки
    buttons = knopki(root, combobox, base, notebook1, notebook2)

    # Меню
    menu(root, base, buttons[:4], buttons[4], note)

    # Надписи
    tk.Label(root, text='Ваш выбор:', bg=cfon, fg="Black", font=tah).grid(row=0, column=5, padx=20)
    tk.Label(root, text='Выберите столбцы:', bg=cfon, fg="Black",
             font=tah).grid(row=0, column=4, padx=20)

    # Расположение элементов
    notebook1.grid(row=1, rowspan=3, column=4, padx=20)
    notebook2.grid(row=1, rowspan=3, column=5, padx=20)
    combobox.grid(row=1, column=6, columnspan=4)

    root.mainloop()


main_window()
sys.path.pop()
