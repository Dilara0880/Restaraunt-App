# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Модуль с функцией сохранения фигуры matplotlib
"""
import os
import tkinter.filedialog as fd
from Library.filename import time_filename

def save(fig, name, way):
    """
    Функция сохранения графика в файл
    Входные параметры:
    Фигура
    Название файла
    Путь
    Выходные параметры:
    True/False
    """
    if os.path.exists(way):
        filename = fd.asksaveasfilename(initialdir=way,
                                        initialfile=(time_filename(name) + '.png'),
                                        filetypes=[("PNG images (.png)", '*.png')],
                                        defaultextension=".png")
        if filename.endswith('.png'):
            try:
                f = open(filename, 'w')
                f.close()
                fig.savefig(filename, fmt='png')
                x = True
            except IOError:
                x = False
        else:
            x = False
    else:
        x = False
    return x