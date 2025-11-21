from typing import List, TypeVar, Callable, Optional, Any, Generic

T = TypeVar('T')
class CountingSorterGeneric(Generic[T]):
    """
    Универсальная (generic) сортировка подсчётом для пользовательских объектов с целочисленным ключом.

    Контракт:
    - Вход: список объектов, функция key: obj -> int (неотрицательный), параметр reverse
    - Выход: новый список тех же объектов, отсортированный по ключу
    - Ошибки: ValueError, если key возвращает отрицательные значения
    - Стабильность: Да
    """

    def __init__(self, key: Callable[[T], int], reverse: bool = False) -> None:
        self.key = key
        self.reverse = reverse

    def sort(self, arr: List[T]) -> List[T]:
        if not arr:
            return []

        keys = [self.key(item) for item in arr]

        # Проверить на отрицательные числа
        if any(k < 0 for k in keys):
            raise ValueError("Key function must return non-negative integers")

        indices = list(range(len(arr)))
        max_key = max(keys)
        min_key = min(keys)
        range_val = max_key - min_key + 1

        count = [0] * range_val
        output_indices = [0] * len(indices)

        for i in indices:
            count[keys[i] - min_key] += 1

        for i in range(1, range_val):
            count[i] += count[i - 1]

        for i in range(len(indices) - 1, -1, -1):
            output_indices[count[keys[i] - min_key] - 1] = i
            count[keys[i] - min_key] -= 1

        result = [arr[i] for i in output_indices]

        if self.reverse:
            result.reverse()

        return result


def counting_sort_generic(arr: List[T], key: Callable[[T], int], reverse: bool = False) -> List[T]:
    """
    @brief Универсальная сортировка подсчётом, которая работает с пользовательскими объектами

    @details Это обёртка вокруг counting_sort, которая позволяет сортировать пользовательские объекты
             путём предоставления функции-ключа, которая извлекает целочисленное значение.

    @param arr Список объектов для сортировки
    @param key Функция, которая извлекает неотрицательное целое число из каждого объекта
    @param reverse Если True, сортировка по убыванию; иначе по возрастанию

    @return Отсортированный список

    @throws ValueError если функция-ключ возвращает отрицательные целые числа

    @code
    # Пример использования с пользовательским классом:
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]
    sorted_people = counting_sort_generic(people, key=lambda p: p.age)
    @endcode
    """
    return CountingSorterGeneric(key=key, reverse=reverse).sort(arr)

