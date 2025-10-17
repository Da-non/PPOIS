class Polynomial:
    """
    @brief Класс многочлена от одной переменной, заданного массивом коэффициентов.
    """

    # Статическая переменная класса (аналог статического поля в C++)
    _instance_count = 0

    def __init__(self, coeffs, degree=None):
        """
        @brief Инициализирует многочлен.
        @param coeffs Список коэффициентов (начиная с константы до старшей степени).
        @param degree Степень многочлена. Должно совпадать с len(coeffs)-1 (если задан).
        """
        if not isinstance(coeffs, (list, tuple)):
            raise TypeError("Коэффициенты должны быть списком или кортежем")
        coeffs = list(coeffs)
        # Удаляем ведущие нули
        while len(coeffs) > 1 and coeffs[-1] == 0:
            coeffs.pop()
        if degree is None:
            self._degree = len(coeffs) - 1  # Приватное поле
        else:
            if degree != len(coeffs) - 1:
                raise ValueError("Несовпадение степени и длины списка коэффициентов")
            self._degree = degree
        self._coeffs = coeffs  # Приватное поле

        # Увеличиваем счетчик созданных экземпляров
        Polynomial._instance_count += 1

    # Управление доступом - свойства только для чтения (константные методы)
    @property
    def coeffs(self):
        """@brief Получение коэффициентов (только чтение)."""
        return self._coeffs[:]  # Возвращаем копию для защиты

    @property
    def degree(self):
        """@brief Получение степени многочлена (только чтение)."""
        return self._degree

    # Статические методы
    @staticmethod
    def zero():
        """
        @brief Создает нулевой многочлен.
        @return Многочлен, равный нулю.
        """
        return Polynomial([0])

    @staticmethod
    def one():
        """
        @brief Создает единичный многочлен (константа 1).
        @return Многочлен, равный единице.
        """
        return Polynomial([1])

    @staticmethod
    def monomial(degree, coeff=1):
        """
        @brief Создает моном x^degree с заданным коэффициентом.
        @param degree Степень монома.
        @param coeff Коэффициент (по умолчанию 1).
        @return Многочлен вида coeff*x^degree.
        """
        coeffs = [0] * (degree + 1)
        coeffs[degree] = coeff
        return Polynomial(coeffs)

    @classmethod
    def get_instance_count(cls):
        """
        @brief Возвращает количество созданных экземпляров класса.
        @return Количество созданных объектов Polynomial.
        """
        return cls._instance_count

    @classmethod
    def reset_instance_count(cls):
        """
        @brief Сбрасывает счетчик экземпляров (для тестирования).
        """
        cls._instance_count = 0

    # Константный метод - не изменяет состояние объекта
    def evaluate(self, x):
        """
        @brief Константный метод вычисления значения многочлена в точке x.
        @param x Значение переменной.
        @return Значение многочлена.
        """
        result = 0
        for exp, coef in enumerate(self._coeffs):
            result += coef * (x ** exp)
        return result

    # Константный метод - возвращает копию коэффициента
    def get_coefficient(self, exp):
        """
        @brief Константный метод получения коэффициента при x^exp.
        @param exp Степень.
        @return Коэффициент при данной степени (или 0, если exp больше степени).
        """
        if exp < 0 or exp > self._degree:
            return 0
        return self._coeffs[exp]

    def __getitem__(self, exp):
        """
        @brief Возвращает коэффициент при x^exp.
        @param exp Степень.
        @return Коэффициент при данной степени (или 0, если exp больше степени).
        """
        return self.get_coefficient(exp)

    def __call__(self, x):
        """
        @brief Вычисляет значение многочлена в точке x.
        @param x Значение переменной.
        @return Значение многочлена.
        """
        return self.evaluate(x)

    def __eq__(self, other):
        """
        @brief Проверяет равенство двух многочленов.
        """
        if not isinstance(other, Polynomial):
            return False
        return self._coeffs == other._coeffs

    def __add__(self, other):
        """
        @brief Сложение двух многочленов (возвращает новый).
        """
        max_deg = max(self._degree, other._degree)
        new_coeffs = []
        for i in range(max_deg+1):
            new_coeffs.append(self[i] + other[i])
        return Polynomial(new_coeffs)

    def __iadd__(self, other):
        """
        @brief Сложение (in-place).
        """
        result = self + other
        self._coeffs = result._coeffs
        self._degree = result._degree
        return self

    def __sub__(self, other):
        """
        @brief Вычитание двух многочленов (возвращает новый).
        """
        max_deg = max(self._degree, other._degree)
        new_coeffs = []
        for i in range(max_deg+1):
            new_coeffs.append(self[i] - other[i])
        return Polynomial(new_coeffs)

    def __isub__(self, other):
        """
        @brief Вычитание (in-place).
        """
        result = self - other
        self._coeffs = result._coeffs
        self._degree = result._degree
        return self

    def __mul__(self, other):
        """
        @brief Умножение двух многочленов (возвращает новый).
        """
        new_coeffs = [0] * (self._degree + other._degree + 1)
        for i, a in enumerate(self._coeffs):
            for j, b in enumerate(other._coeffs):
                new_coeffs[i+j] += a * b
        return Polynomial(new_coeffs)

    def __imul__(self, other):
        """
        @brief Умножение (in-place).
        """
        result = self * other
        self._coeffs = result._coeffs
        self._degree = result._degree
        return self

    def __truediv__(self, other):
        """
        @brief Деление многочленов (возвращает частное, игнорируя остаток).
        """
        if other._degree == 0:
            c = other._coeffs[0]
            if c == 0:
                raise ZeroDivisionError("Деление на нулевой многочлен")
            new_coeffs = [a / c for a in self._coeffs]
            return Polynomial(new_coeffs)
        if other._degree < 0 or other._coeffs == []:
            raise ZeroDivisionError("Деление на нулевой многочлен")
        # стандартное деление столбиком
        A = self._coeffs[:]
        degA = self._degree
        degB = other._degree
        if degA < degB:
            return Polynomial([0])
        B = other._coeffs[:]
        quotient = [0] * (degA - degB + 1)
        while degA >= degB and abs(A[degA]) > 1e-12:
            coef = A[degA] / B[degB]
            shift = degA - degB
            quotient[shift] = coef
            for i in range(degB+1):
                A[i+shift] -= coef * B[i]
            while degA >= 0 and abs(A[degA]) < 1e-12:
                degA -= 1
        return Polynomial(quotient)

    def __itruediv__(self, other):
        """
        @brief Деление (in-place, устанавливает текущее многочлен равным частному).
        """
        result = self / other
        self._coeffs = result._coeffs
        self._degree = result._degree
        return self

    def __repr__(self):
        """
        @brief Строковое представление многочлена.
        """
        terms = []
        for exp, coef in enumerate(self._coeffs):
            if coef == 0:
                continue
            term = str(coef)
            if exp > 0:
                term += "*x"
                if exp > 1:
                    term += f"^{exp}"
            terms.append(term)
        if not terms:
            return "0"
        return " + ".join(terms)

