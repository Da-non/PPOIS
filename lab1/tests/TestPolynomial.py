import unittest
from Polynomial import Polynomial

class TestPolynomial(unittest.TestCase):
    def setUp(self):
        Polynomial.reset_instance_count()

    def test_access_control_properties(self):
        p = Polynomial([1, 2, 3])

        # Доступ к коэффициентам только для чтения
        coeffs = p.coeffs
        self.assertEqual(coeffs, [1, 2, 3])

        # Изменение возвращенного списка не должно влиять на исходный
        coeffs[0] = 999
        self.assertEqual(p.coeffs, [1, 2, 3])  # Оригинал не изменился

        # Доступ к степени только для чтения
        self.assertEqual(p.degree, 2)

    def test_static_methods(self):
        # Статический метод zero()
        zero_poly = Polynomial.zero()
        self.assertEqual(zero_poly.coeffs, [0])
        self.assertEqual(zero_poly.degree, 0)

        # Статический метод one()
        one_poly = Polynomial.one()
        self.assertEqual(one_poly.coeffs, [1])
        self.assertEqual(one_poly.degree, 0)

        # Статический метод monomial()
        mono = Polynomial.monomial(3, 5)  # 5*x^3
        self.assertEqual(mono.coeffs, [0, 0, 0, 5])
        self.assertEqual(mono.degree, 3)

        # Моном с коэффициентом по умолчанию
        mono_default = Polynomial.monomial(2)  # x^2
        self.assertEqual(mono_default.coeffs, [0, 0, 1])

    def test_class_methods_instance_count(self):
        initial_count = Polynomial.get_instance_count()

        p1 = Polynomial([1, 2])
        self.assertEqual(Polynomial.get_instance_count(), initial_count + 1)

        p2 = Polynomial([3, 4, 5])
        self.assertEqual(Polynomial.get_instance_count(), initial_count + 2)

        # Статические методы также создают экземпляры
        zero_poly = Polynomial.zero()
        self.assertEqual(Polynomial.get_instance_count(), initial_count + 3)

    def test_const_methods(self):
        p = Polynomial([1, -2, 3])  # 1 - 2x + 3x^2

        # Константный метод evaluate()
        result = p.evaluate(2)
        self.assertEqual(result, 1 - 2*2 + 3*4)  # 1 - 4 + 12 = 9

        # Константный метод get_coefficient()
        self.assertEqual(p.get_coefficient(0), 1)
        self.assertEqual(p.get_coefficient(1), -2)
        self.assertEqual(p.get_coefficient(2), 3)
        self.assertEqual(p.get_coefficient(5), 0)  # За пределами степени
        self.assertEqual(p.get_coefficient(-1), 0)  # Отрицательная степень

    def test_coeff_access(self):
        p = Polynomial([1, 2, 3])  # 1 + 2x + 3x^2
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 2)
        self.assertEqual(p[2], 3)
        self.assertEqual(p[3], 0)  # степень больше текущей => 0
        self.assertEqual(p[-1], 0) # отрицательная степень => 0

    def test_evaluation(self):
        p = Polynomial([1, -1, 1])  # 1 - x + x^2
        self.assertEqual(p(0), 1)
        self.assertEqual(p(1), 1)   # 1 -1 +1 = 1
        self.assertEqual(p(2), 1 - 2 + 4)  # = 3

    def test_addition(self):
        p1 = Polynomial([1, 2, 3])
        p2 = Polynomial([3, 4])
        s = p1 + p2
        self.assertEqual(s.coeffs, [4, 6, 3])  # (1+3, 2+4, 3+0)
        p1 += p2
        self.assertEqual(p1.coeffs, [4, 6, 3])

    def test_subtraction(self):
        p1 = Polynomial([5, 0, 2])
        p2 = Polynomial([3, 4])
        d = p1 - p2
        self.assertEqual(d.coeffs, [2, -4, 2])  # (5-3, 0-4, 2-0)
        p1 -= p2
        self.assertEqual(p1.coeffs, [2, -4, 2])

    def test_multiplication(self):
        p1 = Polynomial([1, 1])   # (1 + x)
        p2 = Polynomial([1, -1])  # (1 - x)
        m = p1 * p2              # = 1 - x^2
        self.assertEqual(m.coeffs, [1, 0, -1])
        p1 *= p2
        self.assertEqual(p1.coeffs, [1, 0, -1])

    def test_division_by_constant(self):
        p = Polynomial([2, 4, 6])   # 2 + 4x + 6x^2
        q = p / Polynomial([2])     # делим на 2
        self.assertEqual(q.coeffs, [1, 2, 3])
        p /= Polynomial([2])
        self.assertEqual(p.coeffs, [1, 2, 3])

    def test_division_higher_degree(self):
        p = Polynomial([1, 2])      # степень 1
        # делим на x^2 (степень 2)
        q = p / Polynomial([0, 0, 1])
        self.assertEqual(q.coeffs, [0])  # должно получиться 0
        p /= Polynomial([0, 0, 1])
        self.assertEqual(p.coeffs, [0])

    def test_division_polynomials(self):
        # (x^2 - 1) / (x - 1) = x + 1
        p = Polynomial([-1, 0, 1])
        q = Polynomial([-1, 1])
        r = p / q
        self.assertEqual(r.coeffs, [1, 1])
        p /= q
        self.assertEqual(p.coeffs, [1, 1])

    def test_division_with_remainder(self):
        # (2x^3 + 3x^2 + x + 5) / (x + 1)
        p = Polynomial([5, 1, 3, 2])
        q = Polynomial([1, 1])
        r = p / q
        # частное = 0 + 1*x + 2*x^2 (остаток игнорируется)
        self.assertEqual(r.coeffs, [0, 1, 2])
        p /= q
        self.assertEqual(p.coeffs, [0, 1, 2])

    def test_str_repr(self):
        p = Polynomial([0, 0, 0])
        self.assertEqual(repr(p), "0")
        p = Polynomial([1])
        self.assertEqual(repr(p), "1")
        p = Polynomial([1, 0, 2])
        s = repr(p)
        self.assertTrue("1" in s and "2*x^2" in s)

    def test_repr_negative(self):
        p = Polynomial([-1, 1])  # -1 + 1*x
        s = repr(p)
        self.assertTrue(s.startswith("-1"))
        self.assertTrue("x" in s)

    def test_invalid_init(self):
        with self.assertRaises(TypeError):
            _ = Polynomial("not a list")
        with self.assertRaises(ValueError):
            _ = Polynomial([1, 2, 3], degree=1)

    def test_eq_with_trailing_zero(self):
        p1 = Polynomial([1, 2])
        p2 = Polynomial([1, 2, 0])
        self.assertEqual(p1, p2)

    def test_eq_not_equal(self):
        p1 = Polynomial([1, 2])
        p2 = Polynomial([1, 3])
        self.assertNotEqual(p1, p2)

    def test_negative_coeffs(self):
        p1 = Polynomial([-1, -2, 3])
        p2 = Polynomial([1, 2])
        r = p1 + p2
        self.assertEqual(r.coeffs, [0, 0, 3])

    def test_chained_operations(self):
        p = Polynomial([1, 1])
        p += Polynomial([2])       # (1 + x) + 2 = 3 + x
        p *= Polynomial([1, -1])   # (3 + x)*(1 - x) = 3 - 2x - x^2
        self.assertEqual(p.coeffs, [3, -2, -1])

    def test_invalid_coefficients(self):
        # Неправильный тип коэффициентов
        with self.assertRaises(TypeError):
            Polynomial("not a list")

        # Несовпадение степени и длины коэффициентов
        with self.assertRaises(ValueError):
            Polynomial([1, 2, 3], degree=5)

    def test_division_by_zero(self):
        p = Polynomial([1, 2, 3])

        # Деление на нулевой многочлен (константа 0)
        with self.assertRaises(ZeroDivisionError):
            p / Polynomial([0])

        # Деление на пустой/нулевой многочлен
        with self.assertRaises(ZeroDivisionError):
            p / Polynomial([])

if __name__ == "__main__":
    unittest.main()
