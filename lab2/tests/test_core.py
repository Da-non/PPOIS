"""
Юнит тесты для модуля core.py
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.core import Animal, MarineAnimal
from oceanarium.exceptions import *


class TestAnimal(unittest.TestCase):
    """Тесты для абстрактного класса Animal"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем тестовый класс-наследник для тестирования
        class TestAnimalImpl(Animal):
            def get_feeding_requirements(self):
                return {"fish": 2.0, "frequency": 2}

            def get_habitat_requirements(self):
                return {"temperature": 24, "salinity": 35}

        self.animal = TestAnimalImpl("TEST001", "Тестовое животное", "Test species", 5, 150.0)

    def test_animal_initialization(self):
        """Тест инициализации животного"""
        self.assertEqual(self.animal.animal_id, "TEST001")
        self.assertEqual(self.animal.name, "Тестовое животное")
        self.assertEqual(self.animal.species, "Test species")
        self.assertEqual(self.animal.age, 5)
        self.assertEqual(self.animal.weight, 150.0)
        self.assertEqual(self.animal.health_status, "healthy")
        self.assertIsNone(self.animal.last_feeding)
        self.assertIsNone(self.animal.tank_id)
        self.assertEqual(self.animal.activity_level, 100)
        self.assertEqual(self.animal.stress_level, 0)
        self.assertEqual(self.animal.breeding_status, "not_breeding")

    def test_feed_success(self):
        """Тест успешного кормления"""
        result = self.animal.feed("fish", 2.0)
        self.assertTrue(result)
        self.assertIsNotNone(self.animal.last_feeding)
        self.assertEqual(self.animal.activity_level, 100)  # max cap

    def test_feed_too_soon(self):
        """Тест кормления слишком рано"""
        # Первое кормление
        self.animal.feed("fish", 2.0)
        # Попытка покормить сразу после
        result = self.animal.feed("fish", 2.0)
        self.assertFalse(result)

    def test_feed_after_time_passed(self):
        """Тест кормления после прошествии времени"""
        # Устанавливаем время последнего кормления 4 часа назад
        self.animal.last_feeding = datetime.now() - timedelta(hours=4)
        result = self.animal.feed("fish", 2.0)
        self.assertTrue(result)

    def test_check_health_healthy(self):
        """Тест проверки здорового состояния"""
        result = self.animal.check_health()
        self.assertEqual(result, "healthy")
        self.assertEqual(self.animal.health_status, "healthy")

    def test_check_health_stressed(self):
        """Тест проверки стрессового состояния"""
        self.animal.stress_level = 85
        result = self.animal.check_health()
        self.assertEqual(result, "stressed")
        self.assertEqual(self.animal.health_status, "stressed")

    def test_check_health_lethargic(self):
        """Тест проверки вялого состояния"""
        self.animal.activity_level = 25
        result = self.animal.check_health()
        self.assertEqual(result, "lethargic")
        self.assertEqual(self.animal.health_status, "lethargic")

    def test_move_to_tank(self):
        """Тест перемещения в резервуар"""
        initial_stress = self.animal.stress_level
        self.animal.move_to_tank("TANK001")
        self.assertEqual(self.animal.tank_id, "TANK001")
        self.assertEqual(self.animal.stress_level, initial_stress + 5)

    def test_birth_date_calculation(self):
        """Тест расчета даты рождения"""
        expected_birth_year = datetime.now().year - self.animal.age
        self.assertEqual(self.animal.birth_date.year, expected_birth_year)

    def test_medical_records_initialization(self):
        """Тест инициализации медицинских записей"""
        self.assertEqual(len(self.animal.medical_records), 0)
        self.assertIsInstance(self.animal.medical_records, list)

    def test_feeding_schedule_initialization(self):
        """Тест инициализации расписания кормления"""
        self.assertEqual(len(self.animal.feeding_schedule), 0)
        self.assertIsInstance(self.animal.feeding_schedule, dict)


class TestMarineAnimal(unittest.TestCase):
    """Тесты для класса MarineAnimal"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.marine_animal = MarineAnimal(
            "MARINE001", "Морская черепаха", "Chelonia mydas",
            10, 200.0, 85.0, 15
        )

    def test_marine_animal_initialization(self):
        """Тест инициализации морского животного"""
        self.assertEqual(self.marine_animal.animal_id, "MARINE001")
        self.assertEqual(self.marine_animal.name, "Морская черепаха")
        self.assertEqual(self.marine_animal.species, "Chelonia mydas")
        self.assertEqual(self.marine_animal.salt_tolerance, 85.0)
        self.assertEqual(self.marine_animal.depth_preference, 15)
        self.assertGreater(self.marine_animal.swimming_speed, 0)
        self.assertLessEqual(self.marine_animal.swimming_speed, 15.0)

    def test_oxygen_consumption_calculation(self):
        """Тест расчета потребления кислорода"""
        expected_consumption = self.marine_animal.weight * 0.1
        self.assertEqual(self.marine_animal.oxygen_consumption, expected_consumption)

    def test_territorial_radius_range(self):
        """Тест диапазона территориального радиуса"""
        self.assertGreaterEqual(self.marine_animal.territorial_radius, 5)
        self.assertLessEqual(self.marine_animal.territorial_radius, 50)

    def test_get_feeding_requirements(self):
        """Тест получения требований кормления"""
        requirements = self.marine_animal.get_feeding_requirements()
        self.assertIsInstance(requirements, dict)
        self.assertIn("fish", requirements)
        self.assertIn("krill", requirements)
        self.assertIn("seaweed", requirements)

    def test_get_habitat_requirements(self):
        """Тест получения требований среды обитания"""
        requirements = self.marine_animal.get_habitat_requirements()
        self.assertIsInstance(requirements, dict)
        self.assertEqual(requirements["water_type"], "saltwater")
        self.assertIn("temperature_range", requirements)
        self.assertIn("salinity", requirements)
        self.assertIn("depth", requirements)

    def test_inheritance_from_animal(self):
        """Тест наследования от класса Animal"""
        self.assertIsInstance(self.marine_animal, Animal)
        self.assertTrue(hasattr(self.marine_animal, 'feed'))
        self.assertTrue(hasattr(self.marine_animal, 'check_health'))
        self.assertTrue(hasattr(self.marine_animal, 'move_to_tank'))


if __name__ == '__main__':
    unittest.main()
