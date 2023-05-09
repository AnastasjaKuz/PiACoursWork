import datetime
import numpy as np
import pandas as pd

# Генерация денных через передаточные функции
def generate_data(DataFrame):
    W1 = lambda p: -19 / (10 * p + 1) * 1 / (2 * p + 1)
    W2 = lambda p: -15 / (225 * p ** 2 + 23 * p + 1)
    W3 = lambda p: -19 / (100 * p ** 2 + 19 * p + 1)
    W4 = lambda p: -14 / (25 * p + 1) * 1 / (3 * p + 1)
    W5 = lambda p: 36 / (7 * p + 1) * 1 / (5 * p + 1)
    W6 = lambda p: 32 / (4.7 * p + 1)

    out = {
        'Выход': [],
    }
    for i in range(length): #Присвоение названий
        flow_aggl = DataFrame['Расход агломерата'][i]
        flow_pellets = DataFrame['Расход окатыша'][i]
        flow_ore = DataFrame['Расход руды'][i]
        flow_coke = DataFrame['Расход кокса'][i]
        flow_blast = DataFrame['Расход дутья'][i]
        flow_gas = DataFrame['Раcход природного газа'][i]
        out['Выход'].append(float(
            f'{((W1(flow_aggl - 786.5)) - (W2(flow_pellets - 572.5)) - (W3(flow_ore - 217.5)) - (W4(flow_coke - 398.5)) + (W5(flow_blast - 113.5)) + (W6(flow_gas - 1187)) + 1470):.3f}'))
        #Решение уравнения из модели

    return out


length = 500 #Задаем длинну столбца

time = datetime.datetime.now() #Создаем временную метку
timearray = [time]
for i in range(length):
    time += datetime.timedelta(minutes=5)
    timearray.append(time)


rng = np.random.default_rng()
data = {
    'Расход агломерата': [float(f'{rng.uniform(747, 826):.3f}') for i in range(length)],
    'Расход окатыша': [float(f'{rng.uniform(544, 601):.3f}') for i in range(length)],
    'Расход руды': [float(f'{rng.uniform(207, 228):.3f}') for i in range(length)],
    'Расход кокса': [float(f'{rng.uniform(379, 418):.3f}') for i in range(length)],
    'Расход дутья': [float(f'{rng.uniform(108, 119):.3f}') for i in range(length)],
    'Раcход природного газа': [float(f'{rng.uniform(1128, 1246):.3f}') for i in range(length)],
}
timepoint = {"Время": time}
data = timepoint | data | generate_data(data)
df = pd.DataFrame(data)
df.to_csv('input_Kuznetsova.csv', index=False) #Создаем файл csv и отправляем туда данные

