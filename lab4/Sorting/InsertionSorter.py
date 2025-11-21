from typing import List, TypeVar, Callable, Optional, Any, Generic

T = TypeVar('T')


class InsertionSorter(Generic[T]):
    """
    Класс, реализующий сортировку вставками с поддержкой функции-ключа и порядка сортировки.

    Контракт:
    - Вход: список элементов (сравнимых напрямую или через key), опциональные key и reverse
    - Выход: новый отсортированный список, исходный список не изменяется
    - Стабильность: сохраняет порядок элементов с одинаковым ключом
    - Сложность: O(n^2) худший, O(n) лучший; память O(1)
    """

    def __init__(self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> None:
        self.key = key
        self.reverse = reverse

    def sort(self, arr: List[T]) -> List[T]:
        result = arr.copy()
        n = len(result)

        for i in range(1, n):
            key_item = result[i]
            j = i - 1

            # Извлечь значения для сравнения
            if self.key is None:
                key_val = key_item
                compare_func = lambda x: x
            else:
                key_val = self.key(key_item)
                compare_func = self.key

            # Переместить элементы относительно key_item
            if self.reverse:
                while j >= 0 and compare_func(result[j]) < key_val:
                    result[j + 1] = result[j]
                    j -= 1
            else:
                while j >= 0 and compare_func(result[j]) > key_val:
                    result[j + 1] = result[j]
                    j -= 1

            result[j + 1] = key_item

        return result


def insertion_sort(arr: List[T], key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> List[T]:
    """
    @brief Сортирует список используя алгоритм сортировки вставками

    @details Сортировка вставками - это простой алгоритм сортировки, который строит
             финальный отсортированный массив по одному элементу за раз. Он намного
             менее эффективен на больших списках, чем более продвинутые алгоритмы,
             такие как быстрая сортировка, пирамидальная сортировка или сортировка слиянием.

    @param arr Список для сортировки
    @param key Опциональная функция для извлечения ключа сравнения из каждого элемента
    @param reverse Если True, сортировка по убыванию; иначе по возрастанию
    
    @return Отсортированный список
    
    @note Временная сложность: O(n^2) в худшем случае, O(n) в лучшем случае
    @note Пространственная сложность: O(1)

    @code
    # Пример использования:
    arr = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = insertion_sort(arr)
    print(sorted_arr)  # [11, 12, 22, 25, 34, 64, 90]
    @endcode
    """
    return InsertionSorter(key=key, reverse=reverse).sort(arr)
