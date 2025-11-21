"""
@file main_sorting.py
@brief Главный файл, демонстрирующий алгоритмы сортировки
@details Этот файл содержит примеры использования сортировки вставками и сортировки подсчётом
         с различными типами данных, включая пользовательские классы.
"""

from sorting import insertion_sort, counting_sort, counting_sort_generic


class Student:
    """
    @brief Пользовательский класс, представляющий студента
    @details Используется для демонстрации сортировки пользовательских объектов
    """
    
    def __init__(self, name: str, grade: int, age: int):
        """
        @brief Конструктор для класса Student
        @param name Имя студента
        @param grade Оценка студента (0-100)
        @param age Возраст студента
        """
        self.name = name
        self.grade = grade
        self.age = age
    
    def __repr__(self):
        """
        @brief Строковое представление Student
        @return Строка, описывающая студента
        """
        return f"Student(name='{self.name}', grade={self.grade}, age={self.age})"
    
    def __lt__(self, other):
        """
        @brief Сравнение "меньше чем" (для сортировки по умолчанию)
        @param other Другой объект Student
        @return True если оценка этого студента меньше оценки другого
        """
        return self.grade < other.grade
    
    def __le__(self, other):
        """
        @brief Сравнение "меньше или равно"
        @param other Другой объект Student
        @return True если оценка этого студента меньше или равна оценке другого
        """
        return self.grade <= other.grade
    
    def __gt__(self, other):
        """
        @brief Сравнение "больше чем"
        @param other Другой объект Student
        @return True если оценка этого студента больше оценки другого
        """
        return self.grade > other.grade
    
    def __ge__(self, other):
        """
        @brief Сравнение "больше или равно"
        @param other Другой объект Student
        @return True если оценка этого студента больше или равна оценке другого
        """
        return self.grade >= other.grade
    
    def __eq__(self, other):
        """
        @brief Сравнение на равенство
        @param other Другой объект Student
        @return True если у студентов одинаковые имя, оценка и возраст
        """
        return self.name == other.name and self.grade == other.grade and self.age == other.age


def demo_insertion_sort():
    """
    @brief Демонстрирует различные варианты использования сортировки вставками
    """
    print("=" * 60)
    print("ДЕМОНСТРАЦИИ СОРТИРОВКИ ВСТАВКАМИ")
    print("=" * 60)
    
    # Пример 1: Сортировка целых чисел
    print("\n1. Сортировка целых чисел (по возрастанию):")
    int_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Исходный: {int_array}")
    sorted_int = insertion_sort(int_array)
    print(f"   Отсортированный:   {sorted_int}")
    
    # Пример 2: Сортировка целых чисел в обратном порядке
    print("\n2. Сортировка целых чисел (по убыванию):")
    print(f"   Исходный: {int_array}")
    sorted_int_rev = insertion_sort(int_array, reverse=True)
    print(f"   Отсортированный:   {sorted_int_rev}")
    
    # Пример 3: Сортировка чисел с плавающей точкой
    print("\n3. Сортировка чисел с плавающей точкой:")
    float_array = [3.14, 2.71, 1.41, 1.73, 0.58]
    print(f"   Исходный: {float_array}")
    sorted_float = insertion_sort(float_array)
    print(f"   Отсортированный:   {sorted_float}")
    
    # Example 4: Sorting strings
    print("\n4. Сортировка строк (по алфавиту):")
    string_array = ["banana", "apple", "cherry", "date", "elderberry"]
    print(f"   Исходный: {string_array}")
    sorted_str = insertion_sort(string_array)
    print(f"   Отсортированный:   {sorted_str}")
    
    # Example 5: Sorting custom objects
    print("\n5. Сортировка пользовательских объектов Student по оценке:")
    students = [
        Student("Alice", 85, 20),
        Student("Bob", 92, 21),
        Student("Charlie", 78, 19),
        Student("Diana", 95, 22),
        Student("Eve", 88, 20)
    ]
    print("   Исходный:")
    for s in students:
        print(f"      {s}")
    
    sorted_students = insertion_sort(students)
    print("   Отсортированный по оценке:")
    for s in sorted_students:
        print(f"      {s}")
    
    # Example 6: Sorting custom objects by custom key
    print("\n6. Сортировка объектов Student по имени:")
    sorted_by_name = insertion_sort(students, key=lambda s: s.name)
    for s in sorted_by_name:
        print(f"      {s}")
    
    # Example 7: Sorting custom objects by age
    print("\n7. Сортировка объектов Student по возрасту (по убыванию):")
    sorted_by_age = insertion_sort(students, key=lambda s: s.age, reverse=True)
    for s in sorted_by_age:
        print(f"      {s}")


def demo_counting_sort():
    """
    @brief Demonstrates various uses of counting sort
    """
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИИ СОРТИРОВКИ ПОДСЧЁТОМ")
    print("=" * 60)
    
    # Example 1: Sorting small integers
    print("\n1. Сортировка малых целых чисел (по возрастанию):")
    int_array = [4, 2, 2, 8, 3, 3, 1]
    print(f"   Исходный: {int_array}")
    sorted_int = counting_sort(int_array)
    print(f"   Отсортированный:   {sorted_int}")
    
    # Example 2: Sorting in reverse
    print("\n2. Сортировка целых чисел (по убыванию):")
    print(f"   Исходный: {int_array}")
    sorted_int_rev = counting_sort(int_array, reverse=True)
    print(f"   Отсортированный:   {sorted_int_rev}")
    
    # Example 3: Sorting with duplicates
    print("\n3. Сортировка массива с множеством дубликатов:")
    dup_array = [5, 2, 8, 2, 9, 1, 5, 5, 2, 8, 1]
    print(f"   Исходный: {dup_array}")
    sorted_dup = counting_sort(dup_array)
    print(f"   Отсортированный:   {sorted_dup}")
    
    # Example 4: Sorting large range
    print("\n4. Сортировка больших чисел:")
    large_array = [100, 25, 50, 75, 10, 90, 30]
    print(f"   Исходный: {large_array}")
    sorted_large = counting_sort(large_array)
    print(f"   Отсортированный:   {sorted_large}")
    
    # Example 5: Generic counting sort with custom objects
    print("\n5. Сортировка объектов Student по возрасту используя сортировку подсчётом:")
    students = [
        Student("Alice", 85, 20),
        Student("Bob", 92, 21),
        Student("Charlie", 78, 19),
        Student("Diana", 95, 22),
        Student("Eve", 88, 20)
    ]
    print("   Исходный:")
    for s in students:
        print(f"      {s}")
    
    sorted_students = counting_sort_generic(students, key=lambda s: s.age)
    print("   Sorted by age:")
    for s in sorted_students:
        print(f"      {s}")
    
    # Example 6: Sorting by grade
    print("\n6. Sorting Student objects by grade using counting sort:")
    sorted_by_grade = counting_sort_generic(students, key=lambda s: s.grade)
    for s in sorted_by_grade:
        print(f"      {s}")
    
    # Example 7: Edge case - empty array
    print("\n7. Edge case - empty array:")
    empty = []
    print(f"   Исходный: {empty}")
    sorted_empty = counting_sort(empty)
    print(f"   Отсортированный:   {sorted_empty}")
    
    # Example 8: Single element
    print("\n8. Edge case - single element:")
    single = [42]
    print(f"   Исходный: {single}")
    sorted_single = counting_sort(single)
    print(f"   Отсортированный:   {sorted_single}")


def demo_performance_comparison():
    """
    @brief Compares the performance characteristics of both algorithms
    """
    print("\n" + "=" * 60)
    print("ALGORITHM CHARACTERISTICS")
    print("=" * 60)
    
    print("\nInsertion Sort:")
    print("  - Time Complexity: O(n²) worst case, O(n) best case")
    print("  - Space Complexity: O(1)")
    print("  - Стабильная: Да")
    print("  - На месте: Да")
    print("  - Лучше всего для: Малых массивов, почти отсортированных данных")
    print("  - Работает с: Любыми сравнимыми типами данных")
    
    print("\nCounting Sort:")
    print("  - Time Complexity: O(n + k) where k is range")
    print("  - Space Complexity: O(k)")
    print("  - Стабильная: Да")
    print("  - На месте: Нет")
    print("  - Лучше всего для: Малого диапазона целых чисел")
    print("  - Работает с: Неотрицательными целыми числами (или через функцию-ключ)")


def main():
    """
    @brief Main function to run all demonstrations
    """
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "ДЕМОНСТРАЦИЯ АЛГОРИТМОВ СОРТИРОВКИ" + " " * 16 + "║")
    print("║" + " " * 15 + "Variant 6: Insertion & Counting Sort" + " " * 7 + "║")
    print("╚" + "=" * 58 + "╝")
    
    demo_insertion_sort()
    demo_counting_sort()
    demo_performance_comparison()
    
    print("\n" + "=" * 60)
    print("Все демонстрации успешно завершены!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
