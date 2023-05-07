import tkinter as tk
from datetime import datetime
from random import random
from tkinter import ttk
import matplotlib as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from opcua import *


root = tk.Tk()  # создаем объект Tk для gui
root.title('Печь')  # название окна
root.geometry('1000x700')  # размер окна

columns = ['Параметр', 'Значение']  # столбцы для таблицы
rows = [  # строки для таблицы
    ('Расход агломерата', 0),
    ('Расход окатыша', 0),
    ('Расход руды', 0),
    ('Расход кокса', 0),
    ('Расход дутья', 0),
    ('Расход природного газа', 0),
    ('Температура чугуна', 0),
    ('Температура - линейная регрессия', 0),
    ('Метка времени', 0),
]
graph = ttk.Treeview(columns=columns, height=len(rows), show='headings')  # создаем таблицу
graph.place(relx=0, rely=0, relheight=0.5, relwidth=0.5)  # помещаем таблицу
graph.heading('Параметр', text='Параметр')  # идентифицируем столбцы
graph.heading('Значение', text='Значение')

for p in rows:  # создаем строки
    graph.insert('', tk.END, values=p)

plt.use('TkAgg')  # создаем объект для графика
fig = Figure()  # фигура для графика
fig_canvas = FigureCanvasTkAgg(fig, root)  # объект canvas из tk для графиков
axes = fig.add_subplot()  # добавляем место для графика
xs = []  # массив для иксов
ys = []  # массив для игреков, которые будут выданы моделью
ys_lin = []  # массив для игреков, которые будут выданы формулой из матметодов
count = 0  # счетчик точек на графике
fig_canvas.get_tk_widget().place(relx=0, rely=0.5, relheight=0.5, relwidth=1)  # добавляем график в GUI

RANDOM = False  # случайная генерация входов


# включение/выключение случайной генерации входов
def not_rnd():
    global RANDOM
    RANDOM = not RANDOM


# данные, которые будут вводиться через GUI
input_data = {
    'AgglCons': 0.,
    'PelletCons': 0.,
    'OreCons': 0.,
    'CokeCons': 0.,
    'BlastCons': 0.,
    'NatGasCons': 0.,
}


# получение данных с окошек для ввода из GUI
def write_sp():
    input_data['AgglCons'] = float(ent_AgglCons.get().replace(',', '.'))
    input_data['PelletCons'] = float(ent_PelletCons.get().replace(',', '.'))
    input_data['OreCons'] = float(ent_OreCons.get().replace(',', '.'))
    input_data['CokeCons'] = float(ent_CokeCons.get().replace(',', '.'))
    input_data['BlastCons'] = float(ent_BlastCons.get().replace(',', '.'))
    input_data['NatGasCons'] = float(ent_NatGasCons.get().replace(',', '.'))

# создание окон для ввода и кнопки
AgglCons_label = ttk.Label(text='Расход агломерата (от 747 до 826)')  # надпись
AgglCons_label.place(relx=0.505, rely=0.25 * 0.5 - 0.05)  # помещение надписи
ent_AgglCons = ttk.Entry()  # поле ввода
ent_AgglCons.insert(0, '0')  # значение по умолчанию
ent_AgglCons.place(relx=0.505, rely=0.25 * 0.5)  # помещение поля ввода (далее все то же самое, но для других параметров

PelletCons_label = ttk.Label(text='Расход окатыша (от 544 до 601)')
PelletCons_label.place(relx=0.505, rely=0.5 * 0.5 - 0.05)
ent_PelletCons = ttk.Entry()
ent_PelletCons.insert(0, '0')
ent_PelletCons.place(relx=0.505, rely=0.5 * 0.5)

OreCons_label = ttk.Label(text='Расход руды (от 207 до 228)')
OreCons_label.place(relx=0.505, rely=0.75 * 0.5 - 0.05)
ent_OreCons = ttk.Entry()
ent_OreCons.insert(0, '0')
ent_OreCons.place(relx=0.505, rely=0.75 * 0.5)

CokeCons_label = ttk.Label(text='Расход кокса (от 379 до 418)')
CokeCons_label.place(relx=0.755, rely=0.25 * 0.5 - 0.05)
ent_CokeCons = ttk.Entry()
ent_CokeCons.insert(0, '0')
ent_CokeCons.place(relx=0.755, rely=0.25 * 0.5)

BlastCons_label = ttk.Label(text='Расход дутья (от 108 до 119)')
BlastCons_label.place(relx=0.755, rely=0.5 * 0.5 - 0.05)
ent_BlastCons = ttk.Entry()
ent_BlastCons.insert(0, '0')
ent_BlastCons.place(relx=0.755, rely=0.5 * 0.5)

NatGasCons_label = ttk.Label(text='Расход природного газа (от 1128 до 1246)')
NatGasCons_label.place(relx=0.755, rely=0.5 * 0.5 - 0.05)
ent_NatGasCons = ttk.Entry()
ent_NatGasCons.insert(0, '0')
ent_NatGasCons.place(relx=0.755, rely=0.5 * 0.5)


btn_write = ttk.Button(text='Записать значения', command=write_sp)  # кнопка, которая записывает значения
btn_write.place(relx=0.755, rely=0.75 * 0.5)  # помещение кнопки

btn_rnd = ttk.Button(text=f'Рандом', command=not_rnd)  # кнопка для включения/выключения случайной генерации
btn_rnd.place(relx=0.01, rely=0.37)  # помещение кнопки

def linreg(arr):  # формула линейной регрессии с матметодов
    return 1455.526883 - 0.01238368 * arr[1] - 0.02459228 * arr[2] - 0.00954799 * arr[3] \
           - 0.07605182 * arr[4] - 0.00789575 * arr[5]

def create_data():  # отправка данных на сервер
    # отправка данных на сервер в зависимости от того, включена ли случайная генерация
    AgglCons_now = random.uniform(mins['Расход агломерата'], maxs['Расход агломерата']) if RANDOM else input_data['AgglCons']
    PelletCons_now = random.uniform(mins['Расход окатыша'], maxs['Расход окатыша']) if RANDOM else input_data['PelletCons']
    OreCons_now = random.uniform(mins['Расход руды'], maxs['Расход руды']) if RANDOM else input_data['OreCons']
    CokeCons_now = random.uniform(mins['Расход кокса'], maxs['Расход кокса']) if RANDOM else input_data['OreCons']
    BlastCons_now = random.uniform(mins['Расход дутья'], maxs['Расход дутья']) if RANDOM else input_data['BlastCons']
    NatGasCons_now = random.uniform(mins['Расход природного газа'], maxs['Расход природного газа']) if RANDOM \
        else input_data['NatGasCons']

    time_now = datetime.datetime.now()

    # получение значения выхода от модели
    in_now = np.array([AgglCons_now, PelletCons_now, OreCons_now, CokeCons_now, BlastCons_now, NatGasCons_now])
    IronTemp_now = IronTemp_bagging(in_now)
    Algorithm.AgglCons.set_value(AgglCons_now)  # запись всех значений на сервер
    Algorithm.PelletCons.set_value(PelletCons_now)
    Algorithm.OreCons.set_value(AgglCons_now)
    Algorithm.OreCons.set_value(OreCons_now)
    Algorithm.BlastCons.set_value(BlastCons_now)
    Algorithm.NatGasCons.set_value(NatGasCons_now)
    Algorithm.IronTemp.set_value(IronTemp_now)
    Algorithm.TIME.set_value(time_now)
    root.after(500, read_data)  # запуск следующей функции, которая читает данные с сервера и выводит их в GUI

def read_data():  # чтение данных с сервера и вывод их в gui
    global count, xs, ys
    # чтение данных с сервера
    AgglCons_now = client.get_node(Algorithm.AgglCons).get_value()
    PelletCons_now = client.get_node(Algorithm.PelletCons).get_value()
    OreCons_now = client.get_node(Algorithm.OreCons).get_value()
    CokeCons_now = client.get_node(Algorithm.CokeCons).get_value()
    BlastCons_now = client.get_node(Algorithm.BlastCons).get_value()
    NatGasCons_now = client.get_node(Algorithm.NatGasCons).get_value()
    IronTemp_now = client.get_node(Algorithm.IronTemp).get_value()
    time_now = client.get_node(Algorithm.TIME).get_value()
    # получение температуры по матметодам
    temp_now_lin = linreg([AgglCons_now, PelletCons_now, OreCons_now, CokeCons_now, BlastCons_now, NatGasCons_now])
    # добавление всех значений в таблицу
    graph.set('I001', 1, round(AgglCons_now, 2))
    graph.set('I002', 1, round(PelletCons_now, 2))
    graph.set('I003', 1, round(OreCons_now, 2))
    graph.set('I004', 1, round(CokeCons_now, 2))
    graph.set('I005', 1, round(BlastCons_now, 2))
    graph.set('I006', 1, round(NatGasCons_now, 2))
    graph.set('I007', 1, round(IronTemp_now, 2))
    graph.set('I008', 1, round(IronTemp_now_lin, 2))
    graph.set('I009', 1, str(time_now)[:-7])

    if count > 30:
        # если на график больше точек, чем 30 удаляем первые игреки и иксы, чтоб график постоянно обновлялся
        ys.pop(0)
        ys_lin.pop(0)
        xs.pop(0)
    xs.append(time_now)  # добавляем в массив с иксами время
    ys.append(IronTemp_now)  # добавляем в массив с игреками значение
    ys_lin.append(IronTemp_now_lin)  # добавляем в другой массив с игреками другое значение
    count += 1  # увеличиваем значение количества точек на графике
    axes.clear()  # очищаем график
    axes.plot(xs, ys, label='Модель')  # добавляем на него один график
    axes.plot(xs, ys_lin, label='Линейная регрессия')  # добавляем на него другой график
    axes.legend(loc='upper left')
    fig_canvas.draw()  # показываем график
    root.after(500, create_data)  # через интервал запускаем функцию, которая записывает данные на сервер


root.after(0, create_data)  # первый раз запускаем функцию, которая записывает данные на сервер
root.mainloop()  # запускаем gui