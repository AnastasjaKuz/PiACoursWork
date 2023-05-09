import numpy as np
import datetime
import time
from random import uniform
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from opcua import *
import pandas as pd
import matplotlib.pyplot as plt

# Считывание  данных
data = pd.read_csv('input_Kuznetsova.csv')

X = data.iloc[:, 1:7].values
Y = data.iloc[:, 7].values

# Создание и тренировка модели. Для обучения выделено 30% данных
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=30)
model = BaggingRegressor() # Выбираем модель
model.fit(X_train, Y_train) # Тренируем модель


def IronTemp_bagging(x):
    a = np.array([x])
    prediction_a = model.predict(a)
    prediction_value = prediction_a[0]
    return prediction_value

# Вывод значений корреляции и детерминаци
print(f"Корреляция: {np.corrcoef(Y, model.predict(X))[0, 1]:.3}")
print(f"Детерменация: {r2_score(Y, model.predict(X)):.3}")

print(type(model.predict(X)))

# Создание сервера
# Настройка адреса сервера
server = Server()
url = 'opc.tcp://127.0.0.1:12345'
server.set_endpoint(url)

# Название сервера, создание узла данных
name = "OPC_Server"
addspace = server.register_namespace(name)
node = server.get_objects_node()

# Создание узлов через словарь
parameters = {
    "AgglomerateConsumption": 0,
    "PelletsConsumption": 0,
    "OreConsumption": 0,
    "CokeConsumption": 0,
    "BlastConsumption": 0,
    "NaturalGasConsumption": 0,
    "IronTemperature": 0,
    "Time": 0,
}

Params = node.add_variable(addspace, "Params", 0)
for param, value in parameters.items():
    parameters[param] = Params.add_variable(addspace, param, value)
    parameters[param].set_writable()

# Запуск сервера
server.start()

client = Client(url)  # создаем клиента
client.connect()

maxs = data.max()  # максимальные значения
mins = data.min()  # минимальные значения

