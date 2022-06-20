# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Библиотека, содержащая универсальные модули:
checking - проверка значений
excel - работа с Excel
filename - создание имени файла
save_figure - сохранение фигуры matplotlib
text_reports - текстовые отчёты
"""
from Library import checking
from Library import excel
from Library import filename
from Library import save_figure
from Library import text_reports
__all__ = ["checking", "excel", "filename", "save_figure", "text_reports"]