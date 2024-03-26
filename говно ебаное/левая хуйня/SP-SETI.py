alphabet="абвгдежзийклмнопрстуфхцчшщъыьэюя; .,"
import numpy as np

def create_sbox():
    # Здесь нужно определить S-блок
    # Замените эту функцию своей реализацией S-блока
    # sbox = np.array([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])
    sbox = np.array([14, 7, 8, 4, 1, 9, 2, 15, 5, 10, 11, 0, 6, 12, 13, 3])
    return sbox

def compute_lat(sbox):
    n = len(sbox)
    lat = np.zeros((n, n), dtype=int)

    for a in range(n):
        for b in range(n):
            for x in range(n):
                y = sbox[x]
                delta_a = np.bitwise_and(a, x)
                delta_b = np.bitwise_and(b, y)
                delta = np.bitwise_xor(delta_a, delta_b)
                count = bin(np.sum(delta)).count('1')  # Исправленная строка
                lat[a][b] += (-1) ** count

    return lat

def print_lat(lat):
    n = len(lat)
    print("LAT-таблица:")
    print("  |", end="")
    for i in range(n):
        print(f" {i:2d} ", end="")
    print()
    print("-" * (n * 4 + 3))
    for i in range(n):
        print(f"{i:2d}|", end="")
        for j in range(n):
            print(f" {lat[i][j]:2d} ", end="")
        print()

sbox = create_sbox()
lat = compute_lat(sbox)
lat=lat//2
print_lat(lat)