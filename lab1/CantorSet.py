import itertools
class CantorSet:
    """
    @brief Класс неориентированного множества (с поддержкой вложений),
           способного парсить строковое представление вида "{a, b, {c, d}, ...}".
    """

    # Статическая переменная класса
    _instance_count = 0

    def __init__(self, data=None):
        """
        @brief Инициализирует множество. Если передана строка, парсит ее.
        @param data Строка (тип str) для парсинга или другой CantorSet или iterable.
        """
        self._elements = []  # Приватное поле
        CantorSet._instance_count += 1

        if data is None:
            return
        if isinstance(data, CantorSet):
            # копирование
            for e in data._elements:
                self.add(e)
        elif isinstance(data, str):
            # парсинг строки вида "{...}"
            s = data.strip()
            if not s.startswith("{") or not s.endswith("}"):
                raise ValueError("Неправильный формат множества: {}".format(data))
            inner = s[1:-1].strip()
            if inner == "":
                return
            i = 0
            while i < len(inner):
                if inner[i].isspace():
                    i += 1
                    continue
                if inner[i] == '{':
                    # найдем соответствующую закрывающую скобку
                    level = 0
                    start = i
                    while i < len(inner):
                        if inner[i] == '{':
                            level += 1
                        elif inner[i] == '}':
                            level -= 1
                            if level == 0:
                                break
                        i += 1
                    if level != 0:
                        raise ValueError("Несоответствие скобок в множестве")
                    sub_str = inner[start:i+1]
                    sub_set = CantorSet(sub_str)
                    self.add(sub_set)
                    i += 1
                else:
                    # парсим атомарный элемент до запятой или конца
                    start = i
                    while i < len(inner) and inner[i] not in {',', '}'}:
                        i += 1
                    item = inner[start:i].strip()
                    if item != "":
                        self.add(item)
                # пропустить запятые и пробелы
                while i < len(inner) and inner[i] in {',', ' '}:
                    i += 1

        else:
            # инициализация из iterable
            for e in data:
                self.add(e)

    # Управление доступом - свойства только для чтения (константные методы)
    @property
    def elements(self):
        """@brief Получение элементов множества (только чтение)."""
        return self._elements[:]  # Возвращаем копию для защиты

    @property
    def size(self):
        """@brief Получение размера множества (только чтение)."""
        return len(self._elements)

    # Статические методы
    @staticmethod
    def empty():
        """
        @brief Создает пустое множество.
        @return Пустое множество CantorSet.
        """
        return CantorSet()

    @staticmethod
    def singleton(element):
        """
        @brief Создает множество с одним элементом.
        @param element Единственный элемент множества.
        @return Множество, содержащее только заданный элемент.
        """
        result = CantorSet()
        result.add(element)
        return result

    @staticmethod
    def from_list(elements):
        """
        @brief Создает множество из списка элементов.
        @param elements Список элементов.
        @return Множество, содержащее все элементы из списка.
        """
        return CantorSet(elements)

    @classmethod
    def get_instance_count(cls):
        """
        @brief Возвращает количество созданных экземпляров класса.
        @return Количество созданных объектов CantorSet.
        """
        return cls._instance_count

    @classmethod
    def reset_instance_count(cls):
        """
        @brief Сбрасывает счетчик экземпляров (для тестирования).
        """
        cls._instance_count = 0

    # Константные методы - не изменяют состояние объекта
    def is_empty(self):
        """
        @brief Константный метод проверки пустоты множества.
        @return True, если множество не содержит элементов.
        """
        return len(self._elements) == 0

    def contains(self, element):
        """
        @brief Константный метод проверки принадлежности элемента множеству.
        @param element Проверяемый элемент.
        @return True, если элемент принадлежит множеству, иначе False.
        """
        for e in self._elements:
            if isinstance(e, CantorSet) and isinstance(element, CantorSet) and e == element:
                return True
            if not isinstance(e, CantorSet) and not isinstance(element, CantorSet) and e == element:
                return True
        return False

    def get_cardinality(self):
        """
        @brief Константный метод получения мощности множества.
        @return Количество элементов в множестве.
        """
        return len(self._elements)

    def add(self, element):
        """
        @brief Добавляет элемент в множество (если еще не присутствует).
        @param element Добавляемый элемент (строка или CantorSet).
        """
        if isinstance(element, CantorSet):
            # не добавляем дубликаты вложенных множеств
            for e in self._elements:
                if isinstance(e, CantorSet) and e == element:
                    return
            # клонируем вложенное множество
            self._elements.append(CantorSet(element))
        else:
            item = element.strip()
            if item == "":
                return
            # не добавляем дубликат строкового элемента
            for e in self._elements:
                if not isinstance(e, CantorSet) and e == item:
                    return
            self._elements.append(item)

    def remove(self, element):
        """
        @brief Удаляет элемент из множества. Если элемента нет, выбрасывает исключение.
        @param element Удаляемый элемент.
        """
        for i, e in enumerate(self._elements):
            if isinstance(element, CantorSet) and isinstance(e, CantorSet):
                if e == element:
                    del self._elements[i]
                    return
            elif not isinstance(element, CantorSet) and not isinstance(e, CantorSet):
                if e == element:
                    del self._elements[i]
                    return
        raise KeyError("Элемент не найден в множестве: {}".format(element))

    def __getitem__(self, element):
        """
        @brief Проверяет принадлежность элемента множеству.
        @param element Проверяемый элемент.
        @return True, если элемент принадлежит множеству, иначе False.
        """
        return self.contains(element)

    def __eq__(self, other):
        """
        @brief Проверяет равенство двух множеств (без учёта порядка элементов).
        """
        if not isinstance(other, CantorSet):
            return False
        if len(self._elements) != len(other._elements):
            return False
        # каждое элемент в self должен быть в other
        for e in self._elements:
            found = False
            for oe in other._elements:
                if isinstance(e, CantorSet) and isinstance(oe, CantorSet) and e == oe:
                    found = True
                    break
                if not isinstance(e, CantorSet) and not isinstance(oe, CantorSet) and e == oe:
                    found = True
                    break
            if not found:
                return False
        return True

    def __add__(self, other):
        """
        @brief Объединение множеств (возвращает новый объект).
        """
        result = CantorSet(self)
        for e in other._elements:
            result.add(e)
        return result

    def __iadd__(self, other):
        """
        @brief Объединение множеств (in-place).
        """
        for e in other._elements:
            self.add(e)
        return self

    def __mul__(self, other):
        """
        @brief Пересечение множеств (возвращает новый объект).
        """
        result = CantorSet()
        for e in self._elements:
            if other[e]:
                if isinstance(e, CantorSet):
                    result.add(e.clone())
                else:
                    result.add(e)
        return result

    def __imul__(self, other):
        """
        @brief Пересечение множеств (in-place).
        """
        to_keep = []
        for e in self._elements:
            if other[e]:
                to_keep.append(e if not isinstance(e, CantorSet) else CantorSet(e))
        self._elements = to_keep
        return self

    def __sub__(self, other):
        """
        @brief Разность множеств (возвращает новый объект).
        """
        result = CantorSet()
        for e in self._elements:
            if not other[e]:
                result.add(e)
        return result

    def __isub__(self, other):
        """
        @brief Разность множеств (in-place).
        """
        self._elements = [e for e in self._elements if not other[e]]
        return self

    def bullean(self):
        """
        @brief Строит булеан (множество всех подмножеств данного множества).
        @return Список множеств (CantorSet), представляющих все подмножества текущего.
        """
        all_subsets = []
        n = len(self._elements)
        # Используем itertools.combinations для генерации всех подмножеств
        for r in range(n+1):
            for combo in itertools.combinations(range(n), r):
                subset = CantorSet()
                for idx in combo:
                    elem = self._elements[idx]
                    if isinstance(elem, CantorSet):
                        subset.add(elem.clone())
                    else:
                        subset.add(elem)
                all_subsets.append(subset)
        return all_subsets

    def clone(self):
        """
        @brief Клонирует текущее множество (глубокая копия).
        @return Новый объект CantorSet, эквивалентный текущему.
        """
        return CantorSet(self)

    def __repr__(self):
        """
        @brief Строковое представление множества.
        """
        elems_str = []
        for e in self._elements:
            if isinstance(e, CantorSet):
                elems_str.append(repr(e))
            else:
                elems_str.append(str(e))
        return "{" + ", ".join(elems_str) + "}"
