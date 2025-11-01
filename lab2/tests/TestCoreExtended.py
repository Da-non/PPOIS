"""
Дополнительные тесты для модуля core.py для повышения покрытия (исправленная версия)
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.core import Animal, MarineAnimal, Dolphin, Shark
from oceanarium.exceptions import *


class TestMarineAnimalExtended(unittest.TestCase):
    """Расширенные тесты для класса MarineAnimal"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.marine_animal = MarineAnimal("MARINE_EXT", "Тестовое морское животное", "Test Marine", 5, 100.0, 90.0, 20)

    def test_swim_method(self):
        """Тест метода плавания"""
        initial_activity = self.marine_animal.activity_level
        distance = 50.0

        time_taken = self.marine_animal.swim(distance)

        # Проверяем время плавания
        expected_time = distance / self.marine_animal.swimming_speed
        self.assertEqual(time_taken, expected_time)

        # Проверяем снижение активности
        expected_activity = max(0, initial_activity - distance * 0.1)
        self.assertEqual(self.marine_animal.activity_level, expected_activity)

    def test_swim_zero_distance(self):
        """Тест плавания на нулевое расстояние"""
        initial_activity = self.marine_animal.activity_level
        time_taken = self.marine_animal.swim(0.0)

        self.assertEqual(time_taken, 0.0)
        self.assertEqual(self.marine_animal.activity_level, initial_activity)

    def test_swim_large_distance(self):
        """Тест плавания на большое расстояние"""
        large_distance = 2000.0
        self.marine_animal.swim(large_distance)

        # Активность не должна стать отрицательной
        self.assertGreaterEqual(self.marine_animal.activity_level, 0)


class TestDolphin(unittest.TestCase):
    """Тесты для класса Dolphin"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.dolphin = Dolphin("DOLPHIN001", "Флиппер", 8, 150.0)

    def test_dolphin_initialization(self):
        """Тест инициализации дельфина"""
        self.assertEqual(self.dolphin.animal_id, "DOLPHIN001")
        self.assertEqual(self.dolphin.name, "Флиппер")
        self.assertEqual(self.dolphin.species, "Dolphin")
        self.assertEqual(self.dolphin.salt_tolerance, 95.0)
        self.assertEqual(self.dolphin.depth_preference, 10)
        self.assertGreaterEqual(self.dolphin.intelligence_level, 7)
        self.assertLessEqual(self.dolphin.intelligence_level, 10)
        self.assertGreaterEqual(self.dolphin.echolocation_range, 100)
        self.assertLessEqual(self.dolphin.echolocation_range, 200)
        self.assertEqual(len(self.dolphin.social_group), 0)
        self.assertEqual(len(self.dolphin.tricks_learned), 0)

    def test_learn_trick_success(self):
        """Тест успешного изучения трюка"""
        result = self.dolphin.learn_trick("jump")
        self.assertTrue(result)
        self.assertIn("jump", self.dolphin.tricks_learned)

    def test_learn_trick_capacity_limit(self):
        """Тест ограничения количества трюков"""
        # Заполняем все слоты для трюков
        for i in range(self.dolphin.intelligence_level):
            self.dolphin.learn_trick(f"trick_{i}")

        # Попытка изучить еще один трюк
        result = self.dolphin.learn_trick("extra_trick")
        self.assertFalse(result)

    def test_perform_trick_known(self):
        """Тест выполнения известного трюка"""
        self.dolphin.learn_trick("backflip")
        initial_activity = self.dolphin.activity_level

        result = self.dolphin.perform_trick("backflip")
        self.assertTrue(result)
        self.assertEqual(self.dolphin.activity_level, initial_activity + 5)

    def test_perform_trick_unknown(self):
        """Тест выполнения неизвестного трюка"""
        result = self.dolphin.perform_trick("unknown_trick")
        self.assertFalse(result)

    def test_echolocate_within_range(self):
        """Тест эхолокации в пределах досягаемости"""
        distance = self.dolphin.echolocation_range * 0.5
        result = self.dolphin.echolocate(distance)
        self.assertTrue(result)

    def test_echolocate_out_of_range(self):
        """Тест эхолокации вне досягаемости"""
        distance = self.dolphin.echolocation_range * 2
        result = self.dolphin.echolocate(distance)
        self.assertFalse(result)

    def test_communicate_with_group_member(self):
        """Тест общения с членом группы"""
        other_dolphin = Dolphin("DOLPHIN002", "Эхо", 6, 140.0)
        self.dolphin.social_group.append(other_dolphin.animal_id)
        initial_stress = self.dolphin.stress_level

        result = self.dolphin.communicate(other_dolphin)
        self.assertTrue(result)
        self.assertEqual(self.dolphin.stress_level, max(0, initial_stress - 5))

    def test_communicate_with_stranger(self):
        """Тест общения с незнакомым дельфином"""
        other_dolphin = Dolphin("DOLPHIN002", "Незнакомец", 6, 140.0)

        result = self.dolphin.communicate(other_dolphin)
        self.assertFalse(result)

    def test_communication_frequency_range(self):
        """Тест диапазона частоты общения"""
        self.assertGreaterEqual(self.dolphin.communication_frequency, 20)
        self.assertLessEqual(self.dolphin.communication_frequency, 150)


class TestShark(unittest.TestCase):
    """Тесты для класса Shark"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.shark = Shark("SHARK001", "Брюс", 10, 200.0)

    def test_shark_initialization(self):
        """Тест инициализации акулы"""
        self.assertEqual(self.shark.animal_id, "SHARK001")
        self.assertEqual(self.shark.name, "Брюс")
        self.assertEqual(self.shark.species, "Shark")
        self.assertEqual(self.shark.salt_tolerance, 98.0)
        self.assertEqual(self.shark.depth_preference, 50)
        self.assertGreaterEqual(self.shark.aggression_level, 5)
        self.assertLessEqual(self.shark.aggression_level, 10)
        self.assertGreaterEqual(self.shark.hunting_success_rate, 60)
        self.assertLessEqual(self.shark.hunting_success_rate, 90)
        self.assertGreaterEqual(self.shark.teeth_count, 200)
        self.assertLessEqual(self.shark.teeth_count, 300)

    def test_bite_force_calculation(self):
        """Тест расчета силы укуса"""
        expected_bite_force = self.shark.weight * 10
        self.assertEqual(self.shark.bite_force, expected_bite_force)

    def test_electrical_sense_range(self):
        """Тест диапазона электрического чувства"""
        self.assertGreaterEqual(self.shark.electrical_sense_range, 1)
        self.assertLessEqual(self.shark.electrical_sense_range, 5)

    @patch('random.random')
    def test_hunt_successful(self, mock_random):
        """Тест успешной охоты"""
        mock_random.return_value = 0.5  # 50%, что меньше success_rate
        initial_activity = self.shark.activity_level
        initial_stress = self.shark.stress_level

        result = self.shark.hunt("fish")
        self.assertTrue(result)
        self.assertEqual(self.shark.activity_level, initial_activity + 15)
        self.assertEqual(self.shark.stress_level, max(0, initial_stress - 10))

    @patch('random.random')
    def test_hunt_unsuccessful(self, mock_random):
        """Тест неудачной охоты"""
        mock_random.return_value = 0.95  # 95%, что больше любого success_rate
        initial_activity = self.shark.activity_level
        initial_stress = self.shark.stress_level

        result = self.shark.hunt("fish")
        self.assertFalse(result)
        self.assertEqual(self.shark.activity_level, initial_activity)
        self.assertEqual(self.shark.stress_level, initial_stress)

    def test_detect_electrical_field_within_range(self):
        """Тест обнаружения электрического поля в пределах досягаемости"""
        distance = self.shark.electrical_sense_range * 0.5
        result = self.shark.detect_electrical_field(distance)
        self.assertTrue(result)

    def test_detect_electrical_field_out_of_range(self):
        """Тест обнаружения электрического поля вне досягаемости"""
        distance = self.shark.electrical_sense_range * 2
        result = self.shark.detect_electrical_field(distance)
        self.assertFalse(result)

    @patch('random.randint')
    def test_shed_teeth(self, mock_randint):
        """Тест смены зубов"""
        mock_randint.return_value = 5
        initial_teeth = self.shark.teeth_count

        shed_count = self.shark.shed_teeth()
        self.assertEqual(shed_count, 5)
        # Новые зубы вырастают
        self.assertGreaterEqual(self.shark.teeth_count, initial_teeth)


if __name__ == '__main__':
    unittest.main()
