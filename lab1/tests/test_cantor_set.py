import unittest
from cantor_set import CantorSet


class TestCantorSet(unittest.TestCase):
    def setUp(self):
        """Сброс счетчика экземпляров перед каждым тестом"""
        CantorSet.reset_instance_count()

    def test_access_control_properties(self):
        s = CantorSet("{a, b, c}")

        # Доступ к элементам только для чтения
        elements = s.elements
        self.assertEqual(len(elements), 3)
        self.assertTrue("a" in elements)

        # Изменение возвращенного списка не должно влиять на исходный
        elements.append("new_element")
        self.assertEqual(len(s.elements), 3)  # Оригинал не изменился

        # Доступ к размеру только для чтения
        self.assertEqual(s.size, 3)

    def test_static_methods(self):
        # Статический метод empty()
        empty_set = CantorSet.empty()
        self.assertTrue(empty_set.is_empty())
        self.assertEqual(empty_set.size, 0)

        # Статический метод singleton()
        single_set = CantorSet.singleton("x")
        self.assertEqual(single_set.size, 1)
        self.assertTrue(single_set["x"])

        # Статический метод from_list()
        list_set = CantorSet.from_list(["a", "b", "c"])
        self.assertEqual(list_set.size, 3)
        self.assertTrue(list_set["a"] and list_set["b"] and list_set["c"])

    def test_class_methods_instance_count(self):
        initial_count = CantorSet.get_instance_count()

        s1 = CantorSet("{a}")
        self.assertEqual(CantorSet.get_instance_count(), initial_count + 1)

        s2 = CantorSet("{b, c}")
        self.assertEqual(CantorSet.get_instance_count(), initial_count + 2)

        # Статические методы также создают экземпляры
        empty_set = CantorSet.empty()
        self.assertEqual(CantorSet.get_instance_count(), initial_count + 3)

    def test_const_methods(self):
        s = CantorSet("{a, b, {c}}")

        # Константный метод contains()
        self.assertTrue(s.contains("a"))
        self.assertTrue(s.contains("b"))
        self.assertFalse(s.contains("x"))

        # Константный метод get_cardinality()
        self.assertEqual(s.get_cardinality(), 3)

        # Константный метод is_empty()
        self.assertFalse(s.is_empty())
        empty_s = CantorSet.empty()
        self.assertTrue(empty_s.is_empty())

    def test_empty_parse(self):
        s = CantorSet("{}")
        self.assertTrue(s.is_empty())
        self.assertEqual(len(s.elements), 0)

    def test_simple_parse(self):
        s = CantorSet("{a, b, c}")
        self.assertFalse(s.is_empty())
        self.assertTrue(s["a"])
        self.assertTrue("a" in s.elements)
        self.assertTrue(s["b"] and s["c"])
        self.assertFalse(s["d"])

    def test_nested_parse(self):
        s = CantorSet("{a, {b, c}, {}}")
        self.assertTrue("a" in s.elements)
        # находим вложенное множество с элементами b и c
        nested_with_bc = None
        for e in s.elements:
            if isinstance(e, CantorSet) and not e.is_empty():
                if "b" in e.elements and "c" in e.elements:
                    nested_with_bc = e
                    break
        self.assertIsNotNone(nested_with_bc)
        self.assertTrue(nested_with_bc["b"] and nested_with_bc["c"])
        # проверяем, что есть пустое множество внутри
        found_empty = any(isinstance(e, CantorSet) and e.is_empty() for e in s.elements)
        self.assertTrue(found_empty)

    def test_add_remove(self):
        s = CantorSet("{a}")
        s.add("b")
        self.assertTrue(s["b"])
        s.remove("a")
        self.assertFalse(s["a"])
        with self.assertRaises(KeyError):
            s.remove("x")

    def test_add_nested(self):
        inner = CantorSet("{x, y}")
        s = CantorSet()
        s.add(inner)
        self.assertTrue(inner.clone() in s.elements)
        s.add(inner)  # попытка добавить дубликат
        self.assertEqual(len(s.elements), 1)

    def test_union_and_eq(self):
        s1 = CantorSet("{a, b}")
        s2 = CantorSet("{b, c}")
        u = s1 + s2
        self.assertTrue(u["a"] and u["b"] and u["c"])
        s1 += s2
        self.assertTrue(s1["a"] and s1["c"])
        s3 = CantorSet("{c, b, a}")
        self.assertEqual(u, s3)  # сравнение без учета порядка
        self.assertEqual(u, s1)

    def test_intersection(self):
        s1 = CantorSet("{a, b, c}")
        s2 = CantorSet("{b, c, d}")
        inter = s1 * s2
        self.assertTrue(inter["b"] and inter["c"])
        self.assertFalse(inter["a"] or inter["d"])
        s1 *= s2
        self.assertEqual(s1, inter)

    def test_difference(self):
        s1 = CantorSet("{a, b, c}")
        s2 = CantorSet("{b, d}")
        diff = s1 - s2
        self.assertTrue(diff["a"] and diff["c"])
        self.assertFalse(diff["b"] or diff["d"])
        s1 -= s2
        self.assertEqual(s1, diff)

    def test_bulean(self):
        s = CantorSet("{a, b}")
        P = s.bullean()
        # мощность булеана 2^2 = 4
        self.assertEqual(len(P), 4)
        empty = CantorSet("{}")
        full = CantorSet("{a, b}")
        # проверяем наличие пустого множества и полного
        self.assertTrue(any(x.is_empty() for x in P))
        self.assertTrue(full in P or any((not x.is_empty() and "a" in x.elements and "b" in x.elements) for x in P))

    def test_repr_and_clone(self):
        s1 = CantorSet("{a, b, {c}}")
        s2 = s1.clone()
        self.assertEqual(s1, s2)
        self.assertEqual(repr(s1), repr(s2))
        self.assertTrue("a" in repr(s1) and "b" in repr(s1) and "{c}" in repr(s1))

    def test_init_from_iterable(self):
        s = CantorSet(['x', 'y', 'z'])
        self.assertTrue(s['x'] and s['z'] and s['y'])
        self.assertEqual(len(s.elements), 3)
        # init from another CantorSet
        t = CantorSet(s)
        self.assertEqual(t, s)
        t.add('w')
        self.assertFalse('w' in s.elements)
        self.assertTrue('w' in t.elements)

    def test_nested_intersection_and_difference(self):
        inner = CantorSet("{b}")
        s1 = CantorSet("{a, {b}}")
        s2 = CantorSet("{{b}}")
        inter = s1 * s2
        # пересечение должно содержать вложенное множество {b}
        self.assertTrue(any(isinstance(e, CantorSet) and e['b'] for e in inter.elements))
        diff = s1 - s2
        # разности должна убрать вложенное {b}, оставив 'a'
        self.assertTrue(diff['a'])
        self.assertFalse(any(isinstance(e, CantorSet) for e in diff.elements))

    def test_invalid_format_errors(self):
        # Неправильный формат - без скобок
        with self.assertRaises(ValueError):
            CantorSet("a, b, c")

        # Несоответствие скобок
        with self.assertRaises(ValueError):
            CantorSet("{a, {b, c}")

    def test_empty_elements_handling(self):
        # Пустые элементы должны игнорироваться
        s = CantorSet("{a,  , b}")
        self.assertTrue(s["a"])
        self.assertTrue(s["b"])
        self.assertEqual(len(s.elements), 2)

        # Добавление пустой строки
        s.add("")
        self.assertEqual(len(s.elements), 2)  # не должно измениться

    def test_equality_edge_cases(self):
        """Тест для покрытия граничных случаев равенства"""
        s1 = CantorSet("{a}")

        # Сравнение с не-CantorSet
        self.assertFalse(s1 == "not a set")

        # Сравнение множеств разной длины
        s2 = CantorSet("{a, b}")
        self.assertFalse(s1 == s2)

    def test_remove_nested_set(self):
        inner = CantorSet("{x}")
        s = CantorSet()
        s.add(inner)
        s.remove(inner)
        self.assertEqual(len(s.elements), 0)

if __name__ == "__main__":
    unittest.main()
