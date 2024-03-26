import random
import time
from math import sqrt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def find_centre_of_clusters(cluster1, cluster2):
    center1 = [0, 0]
    center2 = [0, 0]
    for i in range(len(cluster1)):
        center1[0] += cluster1[i][0]
        center1[1] += cluster1[i][1]
    for i in range(len(cluster2)):
        center2[0] += cluster2[i][0]
        center2[1] += cluster2[i][1]
    center1 = [center1[0] / len(cluster1), center1[1] / len(cluster1)]
    center2 = [center2[0] / len(cluster2), center2[1] / len(cluster2)]
    return [center1, center2]


def d(df, center, point2):
    return sqrt((center[0] - df.iloc[point2, 0]) ** 2 + (center[1] - df.iloc[point2, 1]) ** 2)


# Указываете путь к файлу Excel
excel_file_path = 'Для кластерного анализа (1).xls'
# Указываете список столбцов, которые вы хотите считать
desired_columns = [0, 1]
# Чтение данных с конкретного листа (например, листа с именем 'Лист1') и определенными столбцами
df = pd.read_excel(excel_file_path, sheet_name='Лист1', usecols=desired_columns, header=None)
seed = int(time.time())
random.seed(seed)
n = len(desired_columns)
m = len(df)
# Выводите содержимое DataFrame
# print(df)
plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
plt.title('Двумерный график данных')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
rand = random.randint(0, m)
center_of_cluster1 = [df.iloc[rand, 0], df.iloc[rand, 1]]
rand = random.randint(0, m)
center_of_cluster2 = [df.iloc[rand, 0], df.iloc[rand, 1]]
cluster1 = []
cluster2 = []
centers_of_clusters = [center_of_cluster1, center_of_cluster2]
while True:
    for i in range(m):
        if d(df, centers_of_clusters[0], i) < d(df, centers_of_clusters[1], i):
            cluster1.append([df.iloc[i, 0], df.iloc[i, 1]])
        else:
            cluster2.append([df.iloc[i, 0], df.iloc[i, 1]])
    if find_centre_of_clusters(cluster1, cluster2) == centers_of_clusters:
        break
    centers_of_clusters = find_centre_of_clusters(cluster1, cluster2)
    cluster1 = []
    cluster2 = []
# Преобразование списков в массивы numpy
cluster1 = np.array(cluster1)
cluster2 = np.array(cluster2)
# Создание графика с явными метками для легенды
plt.scatter(cluster1[:, 0], cluster1[:, 1], label='Cluster 1')
plt.scatter(cluster2[:, 0], cluster2[:, 1], label='Cluster 2')
plt.title('Двумерный график данных')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()  # Добавляем легенду
plt.show()
# вывести кластеры
