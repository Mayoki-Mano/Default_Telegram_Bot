from random import randint
from time import time

def multiply_n2(A, B):
    size = len(A)
    result = [0] * (2 * size - 1)
    for i in range(size):
        for j in range(size):
            result[i + j] += A[i] * B[j]
    return result


def sum_array(A, B):
    for i in range(len(B)):
        A[i] += B[i]
    return A


def sub_array(A, B):
    for i in range(len(A)):
        A[i] = A[i] - B[i]
    return A


def mul_n2(A, B):
    array3 = [0] * ((max(len(A), len(B))) + 1)
    array3[0] = A[0] * B[0]
    array3[1] = A[1] * B[0] + A[0] * B[1]
    array3[2] = A[1] * B[1]
    return array3


def find_AB(A0B0, A1B1, mltply, n):
    array3 = [0] * 2 ** (n + 2)
    for i in range(len(A0B0)):
        array3[i] += A0B0[i]
        array3[i + 2 ** n] += mltply[i]
        array3[i + 2 ** (n + 1)] += A1B1[i]
    return array3


def alg_Karacuba(A, B, n):
    if (n == 0):
        return mul_n2(A, B)
    A0 = [0] * 2 ** n
    B0 = [0] * 2 ** n
    A1 = [0] * 2 ** n
    B1 = [0] * 2 ** n
    for i in range(2 ** n):
        A0[i] = A[i]
        B0[i] = B[i]
        A1[i] = A[i + 2 ** n]
        B1[i] = B[i + 2 ** n]
    A0B0 = alg_Karacuba(A0, B0, n - 1)
    A1B1 = alg_Karacuba(A1, B1, n - 1)
    mltply = sub_array(sub_array(alg_Karacuba(sum_array(A0, A1), sum_array(B0, B1), n - 1), A0B0), A1B1)
    return find_AB(A0B0, A1B1, mltply, n)


n = 15
# создание random многочленов степени 2^n
A = []
B = []
for i in range(2 ** n):
    A.append(randint(1, 100))
    B.append(randint(1, 100))
print(A)
print(B)
t0 = time()
result1 = multiply_n2(A, B)
t1 = time()
print(result1)
t2 = time()
result2 = alg_Karacuba(A, B, n - 1)
result2.pop()
t3 = time()
print(result2)
print(result1 == result2)
print('alg_N2 %f' % (t1 - t0), 'sec')
print('alg_Karacuba %f' % (t3 - t2), 'sec')

# Результаты тестов для n:
# n=3:
# alg_N2 0.000000 sec
# alg_Karacuba 0.000000 sec
# n=5:
# alg_N2 0.001000 sec
# alg_Karacuba 0.000000 sec
# n=10:
# alg_N2 0.096542 sec
# alg_Karacuba 0.100407 sec
# n=15:
# alg_N2 107.257924 sec
# alg_Karacuba 25.498069 sec
# n=20: UNKNOWN
