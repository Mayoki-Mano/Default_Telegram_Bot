import numpy as np
import ctypes
def xor(i, j):
    return 1 if i != j else 0


def dec_to_bin(x):
    bim = list(map(int, bin(x)[2:]))
    return [0] * (48 - len(bim)) + bim


def black_box(x):
    y = x.copy()
    for _ in range(32):
        z = [xor(K[i], y[i]) for i in range(48)]
        y = [z[i] for i in P]
    return y

K=dec_to_bin(1488)

P = [41, 34, 47, 37, 42, 43, 32, 38, 44, 45, 35, 14, 7, 8, 4, 1, 9, 2, 15, 5, 10, 11, 0, 6, 12, 13, 3, 30, 23, 24, 20,
     17, 25, 18, 31, 21, 26, 27, 16, 22, 28, 29, 19, 46, 39, 40, 36, 33]
P_32 = [28, 47, 1, 43, 35, 14, 24, 13, 16, 39, 37, 20, 25, 38, 10, 2, 44, 15, 17, 11, 3, 30, 40, 29, 32, 7, 5, 36, 41,
        6, 26, 18, 12, 31, 33, 27, 19, 46, 8, 45, 0, 23, 21, 4, 9, 22, 42, 34]




libcm = ctypes.CDLL('./libcm.so')
enc = libcm.enc
enc.argtypes = [ctypes.c_uint64]
enc.restype = ctypes.c_uint64
# 097f07940fec1159ed6cffa9

l = enc(0)
m=dec_to_bin(1488)
K_ = black_box(enc(0))
X = m
Y = black_box(X)
X_P32 = [X[i] for i in P_32]
Y_ = [xor(X_P32[i], K_[i]) for i in range(48)]
print(Y)
print(Y_)
print(f'Кол-во различающихся элементов = {sum([abs(Y[i] - Y_[i]) for i in range(48)])}')
