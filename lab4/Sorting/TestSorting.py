"""
@file test_sorting.py
@brief Модульные тесты для алгоритмов сортировки
@details Комплексный набор тестов для функций insertion_sort и counting_sort
"""

import unittest
from sorting import insertion_sort, counting_sort, counting_sort_generic


class TestInsertionSort(unittest.TestCase):
    """Тестовые случаи для функции insertion_sort"""
    
    def test_empty_list(self):
        """Тест сортировки пустого списка"""
        self.assertEqual(insertion_sort([]), [])
    
    def test_single_element(self):
        """Тест сортировки одного элемента"""
        self.assertEqual(insertion_sort([5]), [5])
    
    def test_already_sorted(self):
        """Тест сортировки уже отсортированного списка"""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(insertion_sort(arr), [1, 2, 3, 4, 5])
    
    def test_reverse_sorted(self):
        """Тест сортировки обратно отсортированного списка"""
        arr = [5, 4, 3, 2, 1]
        self.assertEqual(insertion_sort(arr), [1, 2, 3, 4, 5])
    
    def test_random_integers(self):
        """Тест сортировки случайных целых чисел"""
        arr = [64, 34, 25, 12, 22, 11, 90]
        self.assertEqual(insertion_sort(arr), [11, 12, 22, 25, 34, 64, 90])
    
    def test_with_duplicates(self):
        """Тест сортировки списка с дубликатами"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
        self.assertEqual(insertion_sort(arr), expected)
    
    def test_negative_чисел(self):
        """Тест сортировки отрицательных чисел"""
        arr = [-5, -1, -3, -2, -4]
        self.assertEqual(insertion_sort(arr), [-5, -4, -3, -2, -1])
    
    def test_mixed_positive_negative(self):
        """Тест сортировки смешанных положительных и отрицательных чисел"""
        arr = [3, -1, 4, -5, 2, 0]
        self.assertEqual(insertion_sort(arr), [-5, -1, 0, 2, 3, 4])
    
    def test_float_чисел(self):
        """Тест сортировки чисел с плавающей точкой"""
        arr = [3.14, 2.71, 1.41, 1.73, 0.58]
        expected = [0.58, 1.41, 1.73, 2.71, 3.14]
        result = insertion_sort(arr)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertAlmostEqual(result[i], expected[i], places=3)
    
    def test_strings(self):
        """Тест сортировки строк"""
        arr = ["banana", "apple", "cherry", "date"]
        self.assertEqual(insertion_sort(arr), ["apple", "banana", "cherry", "date"])
    
    def test_reverse_order(self):
        """Тест сортировки в порядке убывания"""
        arr = [1, 5, 3, 2, 4]
        self.assertEqual(insertion_sort(arr, reverse=True), [5, 4, 3, 2, 1])
    
    def test_custom_key_function(self):
        """Тест сортировки с пользовательской функцией-ключом"""
        arr = ["a", "bbb", "cc", "dddd"]
        result = insertion_sort(arr, key=len)
        self.assertEqual(result, ["a", "cc", "bbb", "dddd"])
    
    def test_tuples_by_second_element(self):
        """Тест сортировки кортежей по второму элементу"""
        arr = [(1, 5), (2, 3), (3, 1), (4, 4)]
        result = insertion_sort(arr, key=lambda x: x[1])
        self.assertEqual(result, [(3, 1), (2, 3), (4, 4), (1, 5)])
    
    def test_original_list_unchanged(self):
        """Проверьте, не изменен ли исходный список"""
        original = [3, 1, 2]
        arr = original.copy()
        insertion_sort(arr)
        self.assertEqual(arr, [3, 1, 2])  
    
    def test_large_list(self):
        """Тест сортировки большого списка"""
        arr = list(range(100, 0, -1))
        result = insertion_sort(arr)
        self.assertEqual(result, list(range(1, 101)))


class CustomObject:
    """Вспомогательный класс для тестирования пользовательской сортировки объектов"""
    
    def __init__(self, value, name):
        self.value = value
        self.name = name
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __eq__(self, other):
        return self.value == other.value and self.name == other.name


class TestInsertionSortCustomObjects(unittest.TestCase):
    """Тест сортировки  вставками с помощью пользовательских объектов"""
    
    def test_custom_objects_default_comparison(self):
        """Тест сортировки пользовательских объектов using default comparison"""
        objects = [
            CustomObject(3, "c"),
            CustomObject(1, "a"),
            CustomObject(2, "b")
        ]
        result = insertion_sort(objects)
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].value, 2)
        self.assertEqual(result[2].value, 3)
    
    def test_custom_objects_with_key(self):
        """Тест сортировки пользовательских объектов with key function"""
        objects = [
            CustomObject(3, "zebra"),
            CustomObject(1, "apple"),
            CustomObject(2, "banana")
        ]
        result = insertion_sort(objects, key=lambda x: x.name)
        self.assertEqual(result[0].name, "apple")
        self.assertEqual(result[1].name, "banana")
        self.assertEqual(result[2].name, "zebra")


class TestCountingSort(unittest.TestCase):
    """Тестовые случаи для функции counting_sort"""
    
    def test_empty_list(self):
        """Test sorting empty list"""
        self.assertEqual(counting_sort([]), [])
    
    def test_single_element(self):
        """Тест сортировки одного элемента"""
        self.assertEqual(counting_sort([5]), [5])
    
    def test_already_sorted(self):
        """Тест сортировки уже отсортированного списка"""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(counting_sort(arr), [1, 2, 3, 4, 5])
    
    def test_reverse_sorted(self):
        """Тест сортировки обратно отсортированного списка"""
        arr = [5, 4, 3, 2, 1]
        self.assertEqual(counting_sort(arr), [1, 2, 3, 4, 5])
    
    def test_random_integers(self):
        """Тест сортировки случайных целых чисел"""
        arr = [4, 2, 2, 8, 3, 3, 1]
        self.assertEqual(counting_sort(arr), [1, 2, 2, 3, 3, 4, 8])
    
    def test_with_duplicates(self):
        """Тест сортировки с дубликатами"""
        arr = [5, 2, 8, 2, 9, 1, 5, 5, 2, 8, 1]
        expected = [1, 1, 2, 2, 2, 5, 5, 5, 8, 8, 9]
        self.assertEqual(counting_sort(arr), expected)
    
    def test_large_range(self):
        """Тест сортировки с большим диапазоном значений"""
        arr = [100, 25, 50, 75, 10, 90, 30]
        self.assertEqual(counting_sort(arr), [10, 25, 30, 50, 75, 90, 100])
    
    def test_all_same_values(self):
        """Тест сортировки если все значения совпадают"""
        arr = [5, 5, 5, 5, 5]
        self.assertEqual(counting_sort(arr), [5, 5, 5, 5, 5])
    
    def test_two_elements(self):
        """Тест сортировки двух элементов"""
        self.assertEqual(counting_sort([2, 1]), [1, 2])
        self.assertEqual(counting_sort([1, 2]), [1, 2])
    
    def test_reverse_order(self):
        """Тест сортировки в порядке убывания"""
        arr = [1, 5, 3, 2, 4]
        self.assertEqual(counting_sort(arr, reverse=True), [5, 4, 3, 2, 1])
    
    def test_negative_чисел_raises_error(self):
        """Тест что отрицательные числа вызывают ValueError"""
        with self.assertRaisesRegex(ValueError, "non-negative integers"):
            counting_sort([-1, 2, 3])
    
    def test_zeros(self):
        """Тест сортировки с нулями"""
        arr = [0, 5, 0, 3, 0, 1]
        self.assertEqual(counting_sort(arr), [0, 0, 0, 1, 3, 5])
    
    def test_large_list(self):
        """Тест сортировки большого списка"""
        arr = list(range(100, 0, -1))
        result = counting_sort(arr)
        self.assertEqual(result, list(range(1, 101)))
    
    def test_stability(self):
        """Тест стабильности  сортировки при подсчете"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = counting_sort(arr)
        self.assertEqual(result, [1, 1, 2, 3, 4, 5, 6, 9])


class TestCountingSortGeneric(unittest.TestCase):
    """Тестовые случаи для функции counting_sort_generic"""
    
    def test_empty_list(self):
        """Тест сортировки пустого списка"""
        self.assertEqual(counting_sort_generic([], key=lambda x: x), [])
    
    def test_with_key_function(self):
        """Тест сортировки с помощью ключевой функции"""
        arr = ["a", "bbb", "cc", "dddd"]
        result = counting_sort_generic(arr, key=len)
        self.assertEqual(result, ["a", "cc", "bbb", "dddd"])
    
    def test_custom_objects(self):
        """Тест сортировки пользовательских объектов"""
        objects = [
            CustomObject(3, "c"),
            CustomObject(1, "a"),
            CustomObject(2, "b")
        ]
        result = counting_sort_generic(objects, key=lambda x: x.value)
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].value, 2)
        self.assertEqual(result[2].value, 3)
    
    def test_tuples_by_first_element(self):
        """Тест сортировки кортежей по 1 элементу"""
        arr = [(3, "x"), (1, "y"), (2, "z")]
        result = counting_sort_generic(arr, key=lambda x: x[0])
        self.assertEqual(result, [(1, "y"), (2, "z"), (3, "x")])
    
    def test_negative_key_raises_error(self):
        """Проверьте, что отрицательные ключи вызывают ошибку ValueError"""
        arr = [1, 2, 3]
        with self.assertRaisesRegex(ValueError, "non-negative integers"):
            counting_sort_generic(arr, key=lambda x: x - 5)
    
    def test_reverse_order(self):
        """Тестовая сортировка в порядке убывания"""
        objects = [
            CustomObject(1, "a"),
            CustomObject(3, "c"),
            CustomObject(2, "b")
        ]
        result = counting_sort_generic(objects, key=lambda x: x.value, reverse=True)
        self.assertEqual(result[0].value, 3)
        self.assertEqual(result[1].value, 2)
        self.assertEqual(result[2].value, 1)
    
    def test_with_duplicates(self):
        """Тест сортировки с использованием повторяющихся значений ключей"""
        arr = [(1, "a"), (2, "b"), (1, "c"), (3, "d")]
        result = counting_sort_generic(arr, key=lambda x: x[0])
        self.assertEqual([x[0] for x in result], [1, 1, 2, 3])


class TestEdgeCases(unittest.TestCase):
    """Тестовые случаи для граничных условий for both sorting functions"""
    
    def test_insertion_sort_preserves_type(self):
        """Проверьте, что сортировка при вставке сохраняет типы данных"""
        arr = [1.5, 1.1, 1.9, 1.3]
        result = insertion_sort(arr)
        self.assertTrue(all(isinstance(x, float) for x in result))
    
    def test_counting_sort_with_zero_and_positives(self):
        """Тест сортировки с нулем и положительными числами"""
        arr = [0, 1, 0, 2, 0, 3]
        self.assertEqual(counting_sort(arr), [0, 0, 0, 1, 2, 3])
    
    def test_both_sorts_consistent_on_integers(self):
        """Проверьте, дают ли оба вида одинаковый результат для корректных входных данных"""
        arr = [5, 2, 8, 1, 9, 3]
        expected = [1, 2, 3, 5, 8, 9]
        self.assertEqual(insertion_sort(arr), expected)
        self.assertEqual(counting_sort(arr), expected)
    
    def test_insertion_sort_stable(self):
        """Проверьте, стабильна ли сортировка вставок"""
        arr = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
        result = insertion_sort(arr, key=lambda x: x[0])
        self.assertEqual(result[0], (1, "b"))
        self.assertEqual(result[1], (1, "d"))
        self.assertEqual(result[2], (2, "a"))
        self.assertEqual(result[3], (2, "c"))


if __name__ == "__main__":
    unittest.main()
