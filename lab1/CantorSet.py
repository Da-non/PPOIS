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
        
        self._initialize_from_data(data)

    def _initialize_from_data(self, data):
        """Обрабатывает различные типы входных данных для инициализации."""
        if isinstance(data, CantorSet):
            self._initialize_from_cantor_set(data)
        elif isinstance(data, str):
            self._initialize_from_string(data)
        else:
            self._initialize_from_iterable(data)

    def _initialize_from_cantor_set(self, cantor_set):
        """Инициализирует множество из другого объекта CantorSet."""
        for e in cantor_set._elements:
            self.add(e)

    def _initialize_from_string(self, data_str):
        """Парсит строковое представление множества."""
        s = data_str.strip()
        self._validate_string_format(s)
        
        inner = s[1:-1].strip()
        if inner == "":
            return
            
        self._parse_inner_string(inner)

    def _validate_string_format(self, s):
        """Проверяет корректность формата строки."""
        if not s.startswith("{") or not s.endswith("}"):
            raise ValueError("Неправильный формат множества: {}".format(s))

    def _parse_inner_string(self, inner):
        """Парсит внутреннее содержимое строкового представления."""
        i = 0
        while i < len(inner):
            i = self._skip_whitespace(inner, i)
            if i >= len(inner):
                break
                
            if inner[i] == '{':
                i = self._parse_nested_set(inner, i)
            else:
                i = self._parse_atomic_element(inner, i)
            
            i = self._skip_separators(inner, i)

    def _skip_whitespace(self, inner, i):
        """Пропускает пробельные символы."""
        while i < len(inner) and inner[i].isspace():
            i += 1
        return i

    def _skip_separators(self, inner, i):
        """Пропускает запятые и пробелы."""
        while i < len(inner) and inner[i] in {',', ' '}:
            i += 1
        return i

    def _parse_nested_set(self, inner, i):
        """Парсит вложенное множество."""
        start = i
        i = self._find_matching_brace(inner, i)
        sub_str = inner[start:i+1]
        sub_set = CantorSet(sub_str)
        self.add(sub_set)
        return i + 1

    def _find_matching_brace(self, inner, i):
        """Находит закрывающую скобку, соответствующую открывающей."""
        level = 0
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
        return i

    def _parse_atomic_element(self, inner, i):
        """Парсит атомарный элемент (не множество)."""
        start = i
        while i < len(inner) and inner[i] not in {',', '}'}:
            i += 1
            
        item = inner[start:i].strip()
        if item != "":
            self.add(item)
        return i

    def _initialize_from_iterable(self, data):
        """Инициализирует множество из iterable объекта."""
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
            self._add_cantor_set(element)
        else:
            self._add_atomic_element(element)

    def _add_cantor_set(self, cantor_set):
        """Добавляет вложенное множество."""
        for e in self._elements:
            if isinstance(e, CantorSet) and e == cantor_set:
                return
        self._elements.append(CantorSet(cantor_set))

    def _add_atomic_element(self, element):
        """Добавляет атомарный элемент."""
        item = element.strip()
        if item == "":
            return
            
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
            
        return self._check_elements_equality(other)

    def _check_elements_equality(self, other):
        """Проверяет, что все элементы текущего множества есть в другом."""
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
    
