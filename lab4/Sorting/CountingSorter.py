class CountingSorter:
    """
    Класс, реализующий сортировку подсчётом над массивом неотрицательных целых чисел.

    Контракт:
    - Вход: список неотрицательных целых чисел, параметр reverse
    - Выход: новый отсортированный список
    - Ошибки: ValueError при наличии отрицательных чисел
    - Сложность: O(n + k), память O(k)
    """

    def __init__(self, reverse: bool = False) -> None:
        self.reverse = reverse

    def sort(self, arr: List[int]) -> List[int]:
        if not arr:
            return []

        # Проверить на отрицательные числа
        if any(x < 0 for x in arr):
            raise ValueError("Counting sort requires non-negative integers")

        # Найти диапазон
        max_val = max(arr)
        min_val = min(arr)
        range_val = max_val - min_val + 1

        # Создать массив подсчёта и выходной массив
        count = [0] * range_val
        output = [0] * len(arr)

        # Подсчёт вхождений
        for num in arr:
            count[num - min_val] += 1

        # Префиксные суммы -> позиции
        for i in range(1, range_val):
            count[i] += count[i - 1]

        # Стабильная укладка в выход
        for i in range(len(arr) - 1, -1, -1):
            output[count[arr[i] - min_val] - 1] = arr[i]
            count[arr[i] - min_val] -= 1

        if self.reverse:
            output.reverse()

        return output


def counting_sort(arr: List[int], reverse: bool = False) -> List[int]:
    """
    @brief Сортирует список неотрицательных целых чисел используя алгоритм сортировки подсчётом

    @details Сортировка подсчётом - это алгоритм сортировки целых чисел, который работает путём
             подсчёта количества объектов с каждым отдельным значением ключа, и использования
             арифметических операций с этими подсчётами для определения позиций каждого значения
             ключа в выходной последовательности.

    @param arr Список неотрицательных целых чисел для сортировки
    @param reverse Если True, сортировка по убыванию; иначе по возрастанию
    
    @return Отсортированный список
    
    @throws ValueError если список содержит отрицательные целые числа

    @note Временная сложность: O(n + k), где k - диапазон входных данных
    @note Пространственная сложность: O(k)

    @code
    # Пример использования:
    arr = [4, 2, 2, 8, 3, 3, 1]
    sorted_arr = counting_sort(arr)
    print(sorted_arr)  # [1, 2, 2, 3, 3, 4, 8]
    @endcode
    """
    return CountingSorter(reverse=reverse).sort(arr)
