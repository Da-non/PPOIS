"""
Дополнительные тесты для модуля management.py для повышения покрытия (исправленная версия)
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.management import Jellyfish, Octopus, Stingray, SeaHorse
from oceanarium.exceptions import *


class TestSeaHorseExtended(unittest.TestCase):
    """Расширенные тесты для класса SeaHorse"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.male_seahorse = SeaHorse("HORSE_M", "Самец", 1, 0.5, "male")
        self.female_seahorse = SeaHorse("HORSE_F", "Самка", 1, 0.5, "female")

    def test_change_color_capable(self):
        """Тест смены цвета у способного морского конька"""
        self.male_seahorse.color_change_ability = True
        initial_stress = self.male_seahorse.stress_level

        result = self.male_seahorse.change_color("blue")
        self.assertTrue(result)
        self.assertEqual(self.male_seahorse.stress_level, max(0, initial_stress - 5))

    def test_change_color_incapable(self):
        """Тест смены цвета у неспособного морского конька"""
        self.male_seahorse.color_change_ability = False

        result = self.male_seahorse.change_color("red")
        self.assertFalse(result)

    def test_carry_eggs_male_within_capacity(self):
        """Тест вынашивания икры самцом в пределах вместимости"""
        egg_count = self.male_seahorse.pouch_capacity // 2
        result = self.male_seahorse.carry_eggs(egg_count)
        self.assertTrue(result)

    def test_carry_eggs_male_exceed_capacity(self):
        """Тест превышения вместимости сумки у самца"""
        egg_count = self.male_seahorse.pouch_capacity + 100
        result = self.male_seahorse.carry_eggs(egg_count)
        self.assertFalse(result)

    def test_carry_eggs_female(self):
        """Тест попытки вынашивания икры самкой"""
        result = self.female_seahorse.carry_eggs(50)
        self.assertFalse(result)


class TestJellyfishExtended(unittest.TestCase):
    """Расширенные тесты для класса Jellyfish"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.jellyfish = Jellyfish("JELLY_EXT", "Расширенная медуза", 3, 8.0)

    def test_bioluminescence_lighting(self):
        """Тест освещения в зависимости от биолюминесценции"""
        habitat_req = self.jellyfish.get_habitat_requirements()

        if self.jellyfish.bioluminescence:
            self.assertEqual(habitat_req["lighting"], "dim")
        else:
            self.assertEqual(habitat_req["lighting"], "moderate")

    def test_regeneration_ability_range(self):
        """Тест диапазона способности к регенерации"""
        self.assertGreaterEqual(self.jellyfish.regeneration_ability, 50)
        self.assertLessEqual(self.jellyfish.regeneration_ability, 95)

    def test_pulsation_rate_range(self):
        """Тест диапазона частоты пульсации"""
        self.assertGreaterEqual(self.jellyfish.pulsation_rate, 20)
        self.assertLessEqual(self.jellyfish.pulsation_rate, 80)


class TestOctopusExtended(unittest.TestCase):
    """Расширенные тесты для класса Octopus"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.octopus = Octopus("OCTO_EXT", "Расширенный осьминог", 4, 20.0)

    def test_ink_capacity_range(self):
        """Тест диапазона запаса чернил"""
        self.assertGreaterEqual(self.octopus.ink_capacity, 10)
        self.assertLessEqual(self.octopus.ink_capacity, 50)

    def test_sucker_strength_range(self):
        """Тест диапазона силы присосок"""
        self.assertGreaterEqual(self.octopus.sucker_strength, 100)
        self.assertLessEqual(self.octopus.sucker_strength, 500)

    def test_arm_count(self):
        """Тест количества щупалец"""
        self.assertEqual(self.octopus.arm_count, 8)

    def test_high_intelligence(self):
        """Тест высокого интеллекта осьминога"""
        self.assertGreaterEqual(self.octopus.intelligence_level, 7)
        self.assertLessEqual(self.octopus.intelligence_level, 10)


class TestStingrayExtended(unittest.TestCase):
    """Расширенные тесты для класса Stingray"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.stingray = Stingray("STING_EXT", "Расширенный скат", 6, 60.0)

    def test_wingspan_range(self):
        """Тест диапазона размаха крыльев"""
        self.assertGreaterEqual(self.stingray.wingspan, 0.5)
        self.assertLessEqual(self.stingray.wingspan, 3.0)

    def test_sting_barb_count_range(self):
        """Тест количества ядовитых шипов"""
        self.assertGreaterEqual(self.stingray.sting_barb_count, 1)
        self.assertLessEqual(self.stingray.sting_barb_count, 3)

    def test_burial_depth_range(self):
        """Тест глубины зарывания"""
        self.assertGreaterEqual(self.stingray.burial_depth, 5)
        self.assertLessEqual(self.stingray.burial_depth, 30)

    def test_electrical_output_range(self):
        """Тест диапазона электрического разряда"""
        self.assertGreaterEqual(self.stingray.electrical_output, 0)
        self.assertLessEqual(self.stingray.electrical_output, 220)


if __name__ == '__main__':
    unittest.main()
