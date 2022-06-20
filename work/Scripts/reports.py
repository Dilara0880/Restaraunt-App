# -*- coding: utf-8 -*-
# pylint: disable=C0103, E0611
"""
Модуль с функциями формирования отчётов
"""
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from settings import cfon, cknop, font, text_path, graph_path
from filter import get_index
import graph_reports
from Library import save_figure, text_reports, excel

tah = (font, 12)

#Функции сохранения отчётов
def saving_text_report(root, info, name):
    """
    Сохранение текстового отчёта
    Входные данные:
        root - окно tkinter (для закрытия)
        info - таблица pandas.DataFrame
        name - название отчёта
    Выходные данные:
        -
    """
    if text_reports.save(info, text_path, name):
        root.destroy()
    else:
        mb.showwarning('Предупреждение',
                       'Файл не был сохранён. Попробуйте ещё раз')
        root.lift()

def saving_graph_report(root, info, name):
    """
    Сохранение графического отчёта
    Входные данные:
        root - окно tkinter (для закрытия)
        info - график matplotlib.figure
        name - название отчёта
    Выходные данные:
        -
    """
    if save_figure.save(info, name, graph_path):
        root.destroy()
    else:
        mb.showwarning('Предупреждение',
                       'Файл не был сохранён. Попробуйте ещё раз')
        root.lift()

#Формирование отчётов
def statistic(base, columns):
    """
    Формирование статистического отчёта
    Входные данные:
        base - таблица pandas.DataFrame
        columns - выбранные столбцы
    Выходные данные:
        -
    """
    if len(columns) == 1:
        if base[columns[0]].dtype == int or base[columns[0]].dtype == float:
            result = text_reports.kol_statistic(base[[columns[0]]])
            if result['error'] == 1:
                mb.showerror('Ошибка', 'Не удалось провести статистику')
            else:
                analiz(result['stat'], 'Текстовый статистический отчёт')
        else:
            result = text_reports.kach_statistic(base[columns[0]])
            if result['error'] == 1:
                mb.showerror('Ошибка', 'Не удалось провести статистику')
            else:
                analiz(result['stat'], 'Текстовый статистический отчёт')
    else:
        if not False in [x in [int, float] for x in base[columns].dtypes]:
            result = text_reports.kol_statistic(base[columns])
            if result['error'] == 1:
                mb.showerror('Ошибка', 'Не удалось провести статистику')
            else:
                analiz(result['stat'], 'Текстовый статистический отчёт')
        else:
            mb.showerror('Ошибка', 'Неверный тип столбцов.'
                         'Для построения статистического отчёта по нескольким атрибутам '
                         'все атрибуты должны быть количественные')

def pivot(base, columns):
    """
    Формирование сводной таблицы
    Входные данные:
        base - таблица pandas.DataFrame
        columns - выбранные столбцы
    Выходные данные:
        -
    """
    if len(columns) == 2:
        result = text_reports.pivot_table(base, columns[0], columns[1])
        if result['error'] != 0:
            mb.showerror('Ошибка', 'Не удалось построить сводную таблицу.\
                         Убедитесь, что первым в списке столбцов стоит количественный атрибут.')
        else:
            analiz(result['table'], 'Сводная таблица')
    elif len(columns) == 3:
        result = text_reports.pivot_table(base, columns[0], columns[1], columns[2])
        if result['error'] != 0:
            mb.showerror('Ошибка', 'Не удалось построить сводную таблицу.\
                         Убедитесь, что первым в списке столбцов стоит количественный атрибут.')
        else:
            analiz(result['table'], 'Сводная таблица')
    else:
        mb.showerror('Ошибка', 'Неверное количество столбцов')

def graph1(base, columns):
    """
    Анализ результатов построения столбчатой диаграммы
    Входные данные:
        base - таблица pandas.DataFrame
        columns - выбранные столбцы
    Выходные данные:
        -
    """
    if len(columns) == 2:
        temp = graph_reports.diagram(base[columns[0]], base[columns[1]])
        if temp['error'] == 1:
            mb.showinfo('Информация', 'Слишком много данных. График не будет построен.')
        else:
            graph(temp['fig'], 'Кластеризованная столбчатая диаграмма')
    else:
        mb.showerror('Ошибка', 'Неверное количество столбцов')

def graph2(base, columns):
    """
    Анализ результатов построения гистограммы
    Входные данные:
        base - таблица pandas.DataFrame
        columns - выбранные столбцы
    Выходные данные:
        -
    """
    if len(columns) == 2:
        temp = graph_reports.gist(base[columns[0]], base[columns[1]])
        if temp['error'] == 1:
            mb.showerror('Ошибка', 'Неверный тип 2 столбца.\
                        Убедитесь, что второй столбец - количественный атрибут')
        else:
            if temp['error'] == 2:
                mb.showinfo('Информация',
                            'В одной из категорий мало данных для графика, что может\
                                повлиять на вид графика. График будет показан.')
            elif temp['error'] == 3:
                mb.showinfo('Информация',
                            'Много категорий для графика. График будет показан без легенды.')
            fig = temp['fig']
            graph(fig, 'Категоризированная гистограмма')
    else:
        mb.showerror('Ошибка', 'Неверное количество столбцов')

def graph3(base, columns):
    """
    Анализ результатов построения диаграммы Бокса-Вискера
    Входные данные:
        base - таблица pandas.DataFrame
        columns - выбранные столбцы
    Выходные данные:
        -
    """
    if len(columns) == 2:
        temp = graph_reports.boxplot(base[columns[0]], base[columns[1]])
        if temp['error'] == 1:
            mb.showerror('Ошибка', 'Неверный тип 2 столбца.\
 Убедитесь, что второй столбец - количественный атрибут')
        else:
            if temp['error'] == 2:
                mb.showinfo('Информация',
                            'Много категорий для графика. График будет показан без легенды')
            fig = temp['fig']
            graph(fig, 'Категоризированная диаграмма Бокса-Вискера')
    else:
        mb.showerror('Ошибка', 'Неверное количество столбцов')

def graph4(base, columns):
    """
    Анализ результатов построения диаграммы рассеивания
    Входные данные:
        base - таблица pandas.DataFrame
        columns - выбранные столбцы
    Выходные данные:
        -
    """
    if len(columns) == 3:
        temp = graph_reports.scatter(base[columns[0]], base[columns[1]], base[columns[2]])
        if temp['error'] == 1:
            mb.showerror('Ошибка', 'Неверный тип столбцов.\
Убедитесь, что первые 2 столбца - количественные атрибуты')
        else:
            if temp['error'] == 2:
                mb.showinfo('Информация',
                            'Много категорий для графика. График будет показан без легенды')
            fig = temp['fig']
            graph(fig, 'Категоризированная диаграмма рассеивания')
    else:
        mb.showerror('Ошибка', 'Неверное количество столбцов')

#Вывод отчётов
def graph(figure, name):
    """
    Функция graph создаёт окно графических отчётов
    Входные данные:
        figure - фигура matplotlib.figure
        name - название графического отчёта
    Выходные данные:
        -
    """
    #Создание окна
    root5 = tk.Toplevel()
    root5.title("Графический отчёт")
    root5.geometry('700x500+290+90')
    root5.resizable(False, False)
    image = FigureCanvasTkAgg(figure, root5)
    image.draw()
    image.get_tk_widget().configure(width=700, height=450)
    image.get_tk_widget().grid(row=0, column=0)
    tk.Button(root5, text="Сохранить отчёт", bg='White', fg="Black", bd=3, font=tah,
              command=lambda: saving_graph_report(root5, figure, name)).grid(row=1, column=0,
                                                                             pady=10, padx=5)

def comb(root, columns, var1, var2, table1):
    """
    Функция comb создаёт списки и кнопку в окне простого текстового отчёта
    Входные данные:
        root - окно tkinter
        columns - выбранные столбцы
        var1 - значение первого Radiobutton
        var2 - значение первого Radiobutton
        table1 - таблица pandas.DataFrame
    Выходные данные:
        -
    """
    combobox1 = ttk.Combobox(root, state='readonly', values=list(columns), width=20, font=tah)
    combobox1.set('')
    combobox2 = ttk.Combobox(root, state='readonly',
                             values=['равно', 'не равно', 'больше или равно', 'больше',
                                     'меньше или равно', 'меньше'], width=20, font=tah)
    combobox2.set('')

    entr1 = tk.Entry(root, font=tah, width=20)
    combobox1.place(x=10, y=5)
    combobox2.place(x=225, y=5)
    entr1.place(x=440, y=5)

    combobox3 = ttk.Combobox(root, state='readonly', values=list(columns), width=20, font=tah)
    combobox3.set('')
    combobox4 = ttk.Combobox(root, state='readonly',
                             values=['равно', 'не равно', 'больше или равно', 'больше',
                                     'меньше или равно', 'меньше'], width=20, font=tah)
    combobox4.set('')
    entr2 = tk.Entry(root, font=tah, width=20)
    combobox3.place(x=10, y=65)
    combobox4.place(x=225, y=65)
    entr2.place(x=440, y=65)

    combobox5 = ttk.Combobox(root, state='readonly', values=list(columns), width=20, font=tah)
    combobox5.set('')
    combobox6 = ttk.Combobox(root, state='readonly',
                             values=['равно', 'не равно', 'больше или равно', 'больше',
                                     'меньше или равно', 'меньше'], width=20, font=tah)
    combobox6.set('')
    def f():
        """
        Функция передачи информации в анализирующую функцию
        """
        conditions = [[combobox1.get(), combobox2.get(), entr1.get()], var1.get(),
                      [combobox3.get(), combobox4.get(), entr2.get()], var2.get(),
                      [combobox5.get(), combobox6.get(), entr3.get()]]
        root.destroy()
        temp = get_index(conditions, table1)
        if temp['error'] == 0:
            analiz(table1[columns][temp['index']], 'Простой текстовый отчёт')
        elif temp['error'] == 1:
            mb.showinfo('Информация',
                        'Первое условие некорректно.\
 Будут показаны все строки.')
            analiz(table1[columns], 'Простой текстовый отчёт')
        elif temp['error'] == 2:
            mb.showinfo('Инфорация', 'Второе условие некорректно. '
                        'Второе и третье условия были проигнорированы.')
            analiz(table1[columns][temp['index']], 'Простой текстовый отчёт')
        else:
            mb.showinfo('Информация', 'Третье условие некорректно и было проигнорировано.')
            analiz(table1[columns][temp['index']], 'Простой текстовый отчёт')
    entr3 = tk.Entry(root, font=tah, width=20)
    combobox5.place(x=10, y=125)
    combobox6.place(x=225, y=125)
    entr3.place(x=440, y=125)
    tk.Button(root, text="Сформировать отчёт", bg=cknop, fg="Black", bd=3,
              font=tah, command=f).place(x=225, y=160)

def create_PTO(columns, table1):
    """
    Функция create_PTO создаёт окно простого текстого отчёта
    Входные данные:
        columns - выбранные столбцы
        table1 - таблица pandas.DataFrame
    Выходные данные:
        -
    """
    #Создание окна
    root = tk.Toplevel()
    root.title("Простой текстовый отчёт")
    root.geometry('635x200+300+220')
    root.resizable(False, False)
    root.configure(bg=cfon)

    #Флажок
    var1 = tk.StringVar()
    var1.set('И')
    tk.Radiobutton(root, variable=var1, value='ИЛИ', bg=cfon,
                   activebackground=cfon).place(x=360, y=35)
    radio = tk.Radiobutton(root, variable=var1, value='И', bg=cfon, activebackground=cfon)
    radio.place(x=280, y=35)
    radio.select()
    tk.Label(root, text='И', bg=cfon, fg="White",
             font=tah).place(x=260, y=35)
    tk.Label(root, text='ИЛИ', bg=cfon, fg="White",
             font=tah).place(x=320, y=35)
    var2 = tk.StringVar()
    var2.set('И')
    tk.Radiobutton(root, variable=var2, value='ИЛИ', bg=cfon,
                   activebackground=cfon).place(x=360, y=95)
    radio = tk.Radiobutton(root, variable=var2, value='И', bg=cfon, activebackground=cfon)
    radio.place(x=280, y=95)
    radio.select()
    tk.Label(root, text='И', bg=cfon, fg="White",
             font=tah).place(x=260, y=95)
    tk.Label(root, text='ИЛИ', bg=cfon, fg="White",
             font=tah).place(x=320, y=95)
    #Списки и кнопка
    comb(root, columns, var1, var2, table1)

def analiz(info, name):
    """
    Функция analiz создаёт окно текстовых отчётов
    Входные данные:
        info - таблица pandas.DataFrame
        name - название отчёта
    Выходные данные:
        -
    """
    #Создание окна
    root5 = tk.Toplevel()
    root5.title(name)
    root5.geometry('600x300+330+200')
    root5.resizable(False, False)
    tree = ttk.Treeview(root5, height=len(info), show='headings')
    tree['columns'] = list(info.columns)
    for column in tree['columns']:
        tree.heading(column, text=column)
        tree.column(column, width=7*excel.w_column(info[column]), anchor=tk.CENTER)
    i = iter(info.index)
    for value in info.values:
        tree.insert('', 'end', next(i), values=list(value))
    tree.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=2)
    #Скроллбары
    scrollbar = tk.Scrollbar(root5, orient='horizontal', command=tree.xview)
    tree['xscrollcommand'] = scrollbar.set
    vscrollbar = tk.Scrollbar(root5, orient='vert', command=tree.yview)
    tree['yscrollcommand'] = vscrollbar.set
    vscrollbar.grid(row=0, column=1, sticky='nse')
    scrollbar.grid(row=0, column=0, sticky='sew')
    root5.rowconfigure(0, weight=1)
    root5.columnconfigure(0, weight=1)
    tk.Button(root5, text="Сохранить отчёт", bg="White", fg="Black", bd=3, font=tah,
              command=lambda: saving_text_report(root5, info, name)).grid(row=2, column=0, pady=10,
                                                                          padx=5, columnspan=2)

#Функция выбора
def analyze(name, base, columns, rows=0):
    """
    Функция выбора отчёта
    Входные данные:
        name - название отчёта
        base - таблица pandas.DataFrame
        columns - выбранные столбцы
        rows - выбранные строки
    Выходные данные:
        -
    """
    columns = list(columns)
    if not columns:
        mb.showerror('Ошибка', 'Не выбрано ни одного столбца')
    else:
        new_base = base[columns].replace('—', np.nan)
        if rows:
            new_base = new_base.loc[list(map(int, rows))]
        new_base.dropna()
        if len(new_base) == 0:
            mb.showerror('Ошибка', 'Невозможно провести анализ')
        else:
            if name == 'Простой текстовый отчёт':
                create_PTO(columns, new_base)
            elif name == 'Текстовый статистический отчёт':
                statistic(new_base, columns)
            elif name == 'Сводная таблица (среднее значение)':
                pivot(new_base, columns)
            elif name == 'Категоризированная гистограмма':
                graph2(new_base, columns)
            elif name == 'Категоризированная диаграмма Бокса-Вискера':
                graph3(new_base, columns)
            elif name == 'Категоризированная диаграмма рассеивания':
                graph4(new_base, columns)
            else:
                graph1(new_base, columns)