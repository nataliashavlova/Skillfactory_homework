array_input = input("Введите последовательность целых чисел через пробел: ")
# проверка введенных данных на удовлетворение условиям (введены числа) и преобразование в список чисел последовательности
while True:
    try:
        array = list(map (int, array_input.split()))
        break
    except ValueError:
        print("Вы ввели не числа. Пожалуйста, повторите ввод, используя только цифры.")
        array_input = input("Введите последовательность целых чисел через пробел: ")

# введение с клавиатуры произвольного числа для последующего сравнения
number_input = input("Введите любое число: ")

# проверка введенных данных на удовлетворение условию (число) и преобразование в число
while True:
    try:
        number = int(number_input)
        break
    except ValueError:
        print("Вы ввели не число. Пожалуйста, повторите ввод, используя только цифры.")
        number_input = input("Введите любое число: ")

# объявление функции сортировки по возрастанию, используя алгоритм быстрой сортировки
def array_qsort (array, left, right):
    middle = (left + right) // 2
    p = array[middle]
    i, j = left, right
    while i <= j:
        while array[i] < p:
            i += 1
        while array[j] > p:
            j -= 1
        if i <= j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1

    if j > left:
        array_qsort(array, left, j)
    if right > i:
        array_qsort(array, i, right)

# применение сортировки к введенному массиву цифр и вывод результата сортировки
array_qsort(array, 0, len(array)-1)
print("\nВведенный массив отсортирован. Полученный массив:\n", array)

# объявление функции поиска элемента по условию: элемент меньше, чем введенное с клавиатуры число,
# а за ним идет элемент, больший либо равный введенному с клавиатуры числу
def element_search (array, number, left, right):
    if left > right:
        return f"Условия задачи не выполнены: в массиве нет элемента, который был бы < введенного числа {number} и после которого следовал бы элемент >= {number}"

    middle = (right+left) // 2
    if array[middle] < number and array[middle+1] >= number:
        return f"Элемент массива (число {array[middle]}) на позиции {middle} удовлетворяет условиям (< введенного числа {number}, а следующий за ним элемент (число {array[middle+1]}) >= {number})"
    elif number < array[middle]:
        return element_search (array, number, left, middle-1)
    else:
        return element_search (array, number, middle+1, right)

# выполнение поиска элемента в массиве, соответствующего условию, и если оно не выполнено - вывод соответствующего сообщения
try:
    print(element_search(array, number, 0, len(array)-1))
except IndexError:
    print(f"Условия задачи не выполнены: введенное число {number} находится за пределами введенного массива")