import random
import time
import pandas as pd
import matplotlib.pyplot as plt
def find_centre_of_clusters():
    pass

def d(point1,point2):
    return

# Указываете путь к файлу Excel
excel_file_path = 'Для кластерного анализа (1).xls'
# Указываете список столбцов, которые вы хотите считать
desired_columns = [0, 1, 2]
# Чтение данных с конкретного листа (например, листа с именем 'Лист1') и определенными столбцами
df = pd.read_excel(excel_file_path, sheet_name='Лист3', usecols=desired_columns,header=None)
seed = int(time.time())
random.seed(seed)
n = len(desired_columns)
m=len(df)
# Выводите содержимое DataFrame
print(df)
plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
plt.title('Двумерный график данных')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
centre_of_clusters=[]
random_indices = tuple(random.randint(0, m) for i in range(n))

# Используем случайные индексы для выбора элемента из массива
selected_element = df.at[random_indices]
print(selected_element)
print(df.iloc[(1,1,1)])



while True:



    if (find_centre_of_clusters()==centre_of_clusters):
        break
#вывести кластеры
