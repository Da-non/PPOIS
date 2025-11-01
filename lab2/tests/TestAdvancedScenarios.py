"""
Дополнительные тесты для повышения покрытия кода
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.core import MarineAnimal
from oceanarium.equipment import Equipment, WaterPump, FilterSystem, TemperatureController, Tank
from oceanarium.management import Jellyfish, Octopus, Stingray, SeaHorse
from oceanarium.finance import BankAccount, CreditCard
from oceanarium.exceptions import *


class TestAdvancedScenarios(unittest.TestCase):
    """Тесты для продвинутых сценариев использования"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.tank = Tank("ADV_TANK", 100000.0, "display")
        self.account = BankAccount("ADV001", "Продвинутый счет", 50000.0)

    def test_tank_capacity_limits(self):
        """Тест ограничений вместимости резервуара"""
        # Заполняем резервуар до максимума
        max_animals = self.tank.get_max_animals()
        animals_added = 0

        for i in range(max_animals + 5):  # Пытаемся добавить больше максимума
            animal = Jellyfish(f"JELLY{i:03d}", f"Медуза {i}", 2, 5.0)
            result = self.tank.add_animal(animal)
            if result:
                animals_added += 1

        self.assertEqual(animals_added, max_animals)
        self.assertEqual(len(self.tank.animals), max_animals)

    def test_water_parameter_ranges(self):
        """Тест диапазонов параметров воды"""
        # Тестируем граничные значения
        test_parameters = [
            ("temperature", 19.9, False),  # Ниже минимума
            ("temperature", 20.0, True),   # Минимум
            ("temperature", 28.0, True),   # Максимум
            ("temperature", 28.1, False),  # Выше максимума
            ("ph", 7.7, False),            # Ниже минимума
            ("ph", 7.8, True),             # Минимум
            ("ph", 8.4, True),             # Максимум
            ("ph", 8.5, False),            # Выше максимума
        ]

        for param, value, expected in test_parameters:
            self.tank.water_parameters[param] = value
            quality = self.tank.check_water_quality()
            self.assertEqual(quality[param], expected,
                           f"Параметр {param} со значением {value} должен быть {expected}")

    def test_equipment_power_consumption(self):
        """Тест потребления энергии оборудованием"""
        pump = WaterPump("PUMP001", "Насос", "TestCorp", 500.0)
        filter_sys = FilterSystem("FILTER001", "Фильтр", "TestCorp", 1000.0)
        temp_controller = TemperatureController("TEMP001", "Терморегулятор", "TestCorp", 2000.0)

        # Проверяем, что потребление энергии в разумных пределах
        self.assertGreaterEqual(pump.power_consumption, 100)
        self.assertLessEqual(pump.power_consumption, 500)
        self.assertGreaterEqual(filter_sys.power_consumption, 100)
        self.assertLessEqual(filter_sys.power_consumption, 500)
