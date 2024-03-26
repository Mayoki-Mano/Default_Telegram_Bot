import ctypes


def inverse_permutation(permutation):
    size = len(permutation)
    inverse = [0] * size
    for i, index in enumerate(permutation):
        inverse[index] = i
    return inverse


def do_shift(shift, data_bytes):
    shifted_data = (data_bytes >> shift) | (data_bytes << (48 - shift)) & 0xFFFFFFFFFFFF
    return shifted_data


def do_permutation(data_bytes, permutation):
    subblocks = [(data_bytes >> i) & 0xFFFF for i in range(0, 48, 16)]
    permuted_subblocks = [0] * 3
    for i in range(3):
        permuted_subblocks[i] = 0xFFFF
        for j, bit_position in enumerate(permutation):
            permuted_subblocks[i] &= ((((subblocks[i] >> 15 - j) & 0x1) << 15 - bit_position) ^ 0xFFFF)
        permuted_subblocks[i] = permuted_subblocks[i] ^ 0xFFFF
    result = (permuted_subblocks[2] << 32) | (permuted_subblocks[1] << 16) | permuted_subblocks[0]
    return result


def reversed_sp(data_bytes, inversed_permutation):
    return do_permutation(do_shift(11, data_bytes), inversed_permutation)


def encode(M):
    return enc(ctypes.c_uint64(string_to_number(M)))


def string_to_number(input_string):
    return int(input_string.encode('ascii').hex(), 16)


libcm = ctypes.CDLL('./libcm.so')  # Путь к вашей библиотеке
enc = libcm.enc
enc.argtypes = [ctypes.c_uint64]
enc.restype = ctypes.c_uint64

permutation = [14, 7, 8, 4, 1, 9, 2, 15, 5, 10, 11, 0, 6, 12, 13, 3]
inversed_permutation = inverse_permutation(permutation)
# Iccdsw Hesrjv
# Imvvea Iivrmb
# Izbrfd Huejyk
# Jicsud Iuucks Jydaor Isrvin Jzgfka Iodxkh
M = 'Jzgfka'
M_ = 'Iodxkh'
bytesM = string_to_number(M)
bytesM_ = string_to_number(M_)
C = encode(M)
C_ = encode(M_)
kLast = reversed_sp(C_, inversed_permutation) ^ C
kFirst = reversed_sp(bytesM_, inversed_permutation) ^ bytesM

print(kLast)
print(kFirst)