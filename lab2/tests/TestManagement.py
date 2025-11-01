"""
Юнит тесты для модуля management.py
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.management import Jellyfish, Octopus, Stingray, SeaHorse
from oceanarium.core import MarineAnimal
from oceanarium.exceptions import *


class TestJellyfish(unittest.TestCase):
    """Тесты для класса Jellyfish"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.jellyfish = Jellyfish("JELLY001", "Медуза Аурелия", 2, 5.0)

    def test_jellyfish_initialization(self):
        """Тест инициализации медузы"""
        self.assertEqual(self.jellyfish.animal_id, "JELLY001")
        self.assertEqual(self.jellyfish.name, "Медуза Аурелия")
        self.assertEqual(self.jellyfish.species, "Jellyfish")
        self.assertEqual(self.jellyfish.salt_tolerance, 100.0)
        self.assertEqual(self.jellyfish.depth_preference, 5)
        self.assertGreaterEqual(self.jellyfish.tentacle_length, 10)
        self.assertLessEqual(self.jellyfish.tentacle_length, 100)
        self.assertGreaterEqual(self.jellyfish.toxicity_level, 1)
        self.assertLessEqual(self.jellyfish.toxicity_level, 8)

    def test_inheritance_from_marine_animal(self):
        """Тест наследования от MarineAnimal"""
        self.assertIsInstance(self.jellyfish, MarineAnimal)

    def test_get_feeding_requirements(self):
        """Тест получения требований кормления"""
        requirements = self.jellyfish.get_feeding_requirements()
        self.assertIsInstance(requirements, dict)
        self.assertIn("plankton", requirements)
        self.assertIn("small_fish", requirements)

        # Проверяем правильность расчета (2% от веса)
        expected_base = self.jellyfish.weight * 0.02
        self.assertAlmostEqual(requirements["plankton"], expected_base * 0.8, places=2)
        self.assertAlmostEqual(requirements["small_fish"], expected_base * 0.2, places=2)

    def test_get_habitat_requirements(self):
        """Тест получения требований среды обитания"""
        requirements = self.jellyfish.get_habitat_requirements()
        self.assertIsInstance(requirements, dict)
        self.assertEqual(requirements["water_type"], "saltwater")
        self.assertEqual(requirements["temperature_range"], (18, 28))
        self.assertEqual(requirements["current_strength"], "gentle")
        self.assertIn(requirements["lighting"], ["dim", "moderate"])

    def test_pulsate(self):
        """Тест пульсации медузы"""
        initial_activity = self.jellyfish.activity_level
        rate = self.jellyfish.pulsate()

        self.assertEqual(rate, self.jellyfish.pulsation_rate)
        self.assertEqual(self.jellyfish.activity_level, initial_activity + 2)

    def test_sting_within_range(self):
        """Тест жаления в пределах досягаемости"""
        # Устанавливаем токсичность больше 3 для срабатывания
        self.jellyfish.toxicity_level = 5
        distance = self.jellyfish.tentacle_length / 200  # В два раза меньше длины щупалец

        result = self.jellyfish.sting(distance)
        self.assertTrue(result)

    def test_sting_out_of_range(self):
        """Тест жаления вне досягаемости"""
        distance = self.jellyfish.tentacle_length / 50  # Больше длины щупалец
        result = self.jellyfish.sting(distance)
        self.assertFalse(result)

    def test_sting_low_toxicity(self):
        """Тест жаления с низкой токсичностью"""
        self.jellyfish.toxicity_level = 2  # Меньше 3
        distance = 0.01  # Близко
        result = self.jellyfish.sting(distance)
        self.assertFalse(result)


class TestOctopus(unittest.TestCase):
    """Тесты для класса Octopus"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.octopus = Octopus("OCTO001", "Осьминог Павел", 3, 15.0)

    def test_octopus_initialization(self):
        """Тест инициализации осьминога"""
        self.assertEqual(self.octopus.animal_id, "OCTO001")
        self.assertEqual(self.octopus.name, "Осьминог Павел")
        self.assertEqual(self.octopus.species, "Octopus")
        self.assertEqual(self.octopus.arm_count, 8)
        self.assertGreaterEqual(self.octopus.intelligence_level, 7)
        self.assertLessEqual(self.octopus.intelligence_level, 10)
        self.assertGreaterEqual(self.octopus.camouflage_ability, 80)
        self.assertLessEqual(self.octopus.camouflage_ability, 95)

    def test_get_feeding_requirements(self):
        """Тест получения требований кормления"""
        requirements = self.octopus.get_feeding_requirements()
        self.assertIsInstance(requirements, dict)
        self.assertIn("crabs", requirements)
        self.assertIn("fish", requirements)
        self.assertIn("shrimp", requirements)

        # Проверяем правильность расчета (8% от веса)
        expected_base = self.octopus.weight * 0.08
        total_food = sum(requirements.values())
        self.assertAlmostEqual(total_food, expected_base, places=2)

    def test_get_habitat_requirements(self):
        """Тест получения требований среды обитания"""
        requirements = self.octopus.get_habitat_requirements()
        self.assertEqual(requirements["water_type"], "saltwater")
        self.assertEqual(requirements["temperature_range"], (15, 25))
        self.assertTrue(requirements["hiding_places"])
        self.assertEqual(requirements["substrate"], "rocky")

    @patch('random.random')
    def test_camouflage_success(self, mock_random):
        """Тест успешной маскировки"""
        mock_random.return_value = 0.5  # 50%
        self.octopus.camouflage_ability = 80  # 80%
        initial_stress = self.octopus.stress_level

        result = self.octopus.camouflage()
        self.assertTrue(result)
        self.assertEqual(self.octopus.stress_level, max(0, initial_stress - 10))

    @patch('random.random')
    def test_camouflage_failure(self, mock_random):
        """Тест неудачной маскировки"""
        mock_random.return_value = 0.9  # 90%
        self.octopus.camouflage_ability = 80  # 80%

        result = self.octopus.camouflage()
        self.assertFalse(result)

    def test_release_ink_success(self):
        """Тест успешного выпуска чернил"""
        self.octopus.ink_capacity = 20
        initial_capacity = self.octopus.ink_capacity

        released = self.octopus.release_ink()
        self.assertEqual(released, 10)  # Максимум 10 мл
        self.assertEqual(self.octopus.ink_capacity, initial_capacity - 10)

    def test_release_ink_insufficient(self):
        """Тест выпуска чернил при недостатке"""
        self.octopus.ink_capacity = 3  # Меньше 5
        released = self.octopus.release_ink()
        self.assertEqual(released, 0)

    def test_solve_puzzle_success(self):
        """Тест успешного решения головоломки"""
        self.octopus.intelligence_level = 8
        result = self.octopus.solve_puzzle(7)
        self.assertTrue(result)

    def test_solve_puzzle_failure(self):
        """Тест неудачного решения головоломки"""
        self.octopus.intelligence_level = 6
        result = self.octopus.solve_puzzle(8)
        self.assertFalse(result)


class TestStingray(unittest.TestCase):
    """Тесты для класса Stingray"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.stingray = Stingray("STING001", "Скат Манта", 5, 50.0)

    def test_stingray_initialization(self):
        """Тест инициализации ската"""
        self.assertEqual(self.stingray.animal_id, "STING001")
        self.assertEqual(self.stingray.name, "Скат Манта")
        self.assertEqual(self.stingray.species, "Stingray")
        self.assertGreaterEqual(self.stingray.wingspan, 0.5)
        self.assertLessEqual(self.stingray.wingspan, 3.0)
        self.assertGreaterEqual(self.stingray.sting_barb_count, 1)
        self.assertLessEqual(self.stingray.sting_barb_count, 3)

    def test_get_feeding_requirements(self):
        """Тест получения требований кормления"""
        requirements = self.stingray.get_feeding_requirements()
        self.assertIn("mollusks", requirements)
        self.assertIn("worms", requirements)
        self.assertIn("small_fish", requirements)

        # Проверяем правильность расчета (6% от веса)
        expected_base = self.stingray.weight * 0.06
        total_food = sum(requirements.values())
        self.assertAlmostEqual(total_food, expected_base, places=2)

    def test_get_habitat_requirements(self):
        """Тест получения требований среды обитания"""
        requirements = self.stingray.get_habitat_requirements()
        self.assertEqual(requirements["water_type"], "saltwater")
        self.assertEqual(requirements["substrate"], "sandy")
        self.assertEqual(requirements["depth_minimum"], 2)

    def test_bury_in_sand(self):
        """Тест зарывания в песок"""
        initial_stress = self.stingray.stress_level
        initial_activity = self.stingray.activity_level

        result = self.stingray.bury_in_sand()
        self.assertTrue(result)
        self.assertEqual(self.stingray.stress_level, max(0, initial_stress - 15))
        self.assertEqual(self.stingray.activity_level, initial_activity - 5)

    def test_electric_shock_capable(self):
        """Тест электрического разряда у электрического ската"""
        self.stingray.electrical_output = 100  # Способен к разряду
        result = self.stingray.electric_shock(50)
        self.assertTrue(result)

    def test_electric_shock_incapable(self):
        """Тест отсутствия электрического разряда"""
        self.stingray.electrical_output = 0  # Не способен к разряду
        result = self.stingray.electric_shock(50)
        self.assertFalse(result)

    def test_electric_shock_voltage_too_high(self):
        """Тест превышения возможного напряжения"""
        self.stingray.electrical_output = 50
        result = self.stingray.electric_shock(100)  # Больше возможного
        self.assertFalse(result)


class TestSeaHorse(unittest.TestCase):
    """Тесты для класса SeaHorse"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.male_seahorse = SeaHorse("HORSE001", "Морской конек Гиппо", 1, 0.5, "male")
        self.female_seahorse = SeaHorse("HORSE002", "Морской конек Кампа", 1, 0.5, "female")

    def test_seahorse_initialization_male(self):
        """Тест инициализации самца морского конька"""
        self.assertEqual(self.male_seahorse.gender, "male")
        self.assertGreater(self.male_seahorse.pouch_capacity, 0)
        self.assertGreaterEqual(self.male_seahorse.pouch_capacity, 100)
        self.assertLessEqual(self.male_seahorse.pouch_capacity, 2000)

    def test_seahorse_initialization_female(self):
        """Тест инициализации самки морского конька"""
        self.assertEqual(self.female_seahorse.gender, "female")
        self.assertEqual(self.female_seahorse.pouch_capacity, 0)

    def test_get_feeding_requirements(self):
        """Тест получения требований кормления"""
        requirements = self.male_seahorse.get_feeding_requirements()
        self.assertIn("brine_shrimp", requirements)
        self.assertIn("copepods", requirements)

        # Высокий метаболизм - 15% от веса
        expected_base = self.male_seahorse.weight * 0.15
        total_food = sum(requirements.values())
        self.assertAlmostEqual(total_food, expected_base, places=2)

    def test_get_habitat_requirements(self):
        """Тест получения требований среды обитания"""
        requirements = self.male_seahorse.get_habitat_requirements()
        self.assertEqual(requirements["water_type"], "saltwater")
        self.assertEqual(requirements["temperature_range"], (22, 26))
        self.assertEqual(requirements["vegetation"], "sea_grass")
        self.assertEqual(requirements["current_strength"], "gentle")

    def test_grip_with_tail_success(self):
        """Тест успешного хватания хвостом"""
        self.male_seahorse.grip_strength = 30
        result = self.male_seahorse.grip_with_tail(25)
        self.assertTrue(result)

    def test_grip_with_tail_failure(self):
        """Тест неудачного хватания хвостом"""
        self.male_seahorse.grip_strength = 20
        result = self.male_seahorse.grip_with_tail(30)
        self.assertFalse(result)

    def test_species_attributes(self):
        """Тест видовых атрибутов"""
        self.assertEqual(self.male_seahorse.species, "Sea Horse")
        self.assertEqual(self.male_seahorse.salt_tolerance, 88.0)
        self.assertEqual(self.male_seahorse.depth_preference, 15)
        self.assertGreaterEqual(self.male_seahorse.tail_length, 5)
        self.assertLessEqual(self.male_seahorse.tail_length, 15)


if __name__ == '__main__':
    unittest.main()
