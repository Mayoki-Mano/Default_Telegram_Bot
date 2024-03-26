def is_in_class_L(truth_table):
    # Проверка принадлежности к классу L
    n = len(truth_table)
    for i in range(n):
        for j in range(i + 1, n):
            if truth_table[i] != truth_table[j]:
                return False
    return True

def is_in_class_T0(truth_table):
    # Проверка принадлежности к классу T0
    if truth_table[0] == 0:
        return True
    return False

def is_in_class_T1(truth_table):
    # Проверка принадлежности к классу T1
    if truth_table[-1] == 1:
        return True
    return False

def is_in_class_S(truth_table):
    # Проверка принадлежности к классу S
    return not is_in_class_L(truth_table) and not is_in_class_T0(truth_table) and not is_in_class_T1(truth_table)

def count_boolean_functions(n):
    # Подсчет количества булевых функций
    count = 0
    total_functions = 2 ** (2 ** n)  # Общее количество возможных функций
    for i in range(total_functions):
        truth_table = []
        for j in range(2 ** n):
            truth_table.append((i >> j) & 1)
        print(truth_table)
        if is_in_class_S(truth_table):
            count += 1
    return count

n = int(input("Введите количество переменных: "))
count = count_boolean_functions(n)
print(f"Количество булевых функций размерности {n}, не принадлежащих классам L, T0, T1, но принадлежащих классу S: {count}")