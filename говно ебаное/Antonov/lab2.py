import math
from random import randint
from time import time
from math import log

def print_matrix(array):
    for row in array:
        print(*row)
    print()


def alg_NML(array1, array2):
    array3 = []
    for i in range(len(array1)):
        array3.append([0] * len(array2[0]))
    for n in range(len(array1)):
        for m in range(len(array2[0])):
            result = 0
            for l in range(len(array1[0])):
                result ^= array1[n][l] * array2[l][m]
            array3[n][m] = result
    return array3


def str_of_A_div_str_k(array1, k, str):
    result_array = []
    for i in range(math.ceil(len(array1) / k)):
        result = 0
        for j in range(k):
            if i*k+j < len(array1):
                result+=array1[str][i*k+j]*2**(k-j-1)
        result_array.append(result)
    return result_array

def row_of_B_div_str_k(array2, k, row):
    result_array = []
    for i in range(math.ceil(len(array2) / k)):
        result = 0
        for j in range(k):
            if i*k+j < len(array2[0]):
                result+=array2[i*k+j][row]*2**(k-j-1)
        result_array.append(result)
    return result_array

def alg_NMLK(array1, array2, k_array, k):
    array1_divstr_k = []
    array2_divrow_k = []
    for i in range(len(array1)):
        array1_divstr_k.append(str_of_A_div_str_k(array1,k,i))
        array2_divrow_k.append(row_of_B_div_str_k(array2,k,i))
    array3 = []
    for i in range(len(array1)):
        array3.append([0] * len(array2[0]))
    for n in range(len(array1_divstr_k)):
        for m in range(len(array2_divrow_k)):
            result = 0
            for l in range(len(array1_divstr_k[0])):
                result ^= k_array[array1_divstr_k[n][l]][array2_divrow_k[m][l]]
            array3[n][m] = result
    return array3


def xor(b1, b2, k):
    if k == 0:
        return 0
    return xor(b1 // 2, b2 // 2, k - 1) ^ (b1 % 2 * b2 % 2)


array1 = []
array2 = []
n = 10
k = int(log(n, 2))
k_array = []
for i in range(2**n):
    array1.append([])
    array2.append([])
    for j in range(2**n):
        array1[i].append(randint(0, 1))
        array2[i].append(randint(0, 1))
#print_matrix(array1)
#print_matrix(array2)

for i in range(2 ** k):
    k_array.append([0] * 2 ** k)
    b1 = 0
for i in range(2 ** k):
    b2 = b1
    for j in range(i, 2 ** k):
        k_array[i][j] = xor(b1, b2, k)
        k_array[j][i] = k_array[i][j]
        b2 += 1
    b1 += 1
#print(k_array)
t0 = time()
NML_matrix=alg_NML(array1, array2)
t1 = time()
NMLK_matrix=alg_NMLK(array1,array2,k_array,k)
t2 = time()
#print_matrix(NML_matrix)
#print_matrix(NMLK_matrix)
print(NML_matrix==NML_matrix)
print('alg_NML %f' % (t1 - t0), 'sec')
print('alg_NML/K %f' % (t2 - t1), 'sec')


# Результаты работы для разных n:
# n=3:
# alg_NML 0.000000 sec
# alg_NML/K 0.000000 sec
# n=4:
# alg_NML 0.000999 sec
# alg_NML/K 0.000000 sec
# n=6:
# alg_NML 0.019459 sec
# alg_NML/K 0.012515 sec
# n=8:
# alg_NML 1.387480 sec
# alg_NML/K 0.526501 sec
# n=10:
# alg_NML 96.069805 sec
# alg_NML/K 30.643574 sec