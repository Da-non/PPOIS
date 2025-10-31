"""
Юнит тесты для модуля oceanarium.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.oceanarium import Oceanarium
from oceanarium.equipment import Tank, MonitoringSystem, SecuritySystem
from oceanarium.finance import BankAccount
from oceanarium.exceptions import *


class TestOceanarium(unittest.TestCase):
    """Тесты для класса Oceanarium"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.oceanarium = Oceanarium("Морской мир", "Москва", 5000)

    def test_oceanarium_initialization(self):
        """Тест инициализации океанариума"""
        self.assertEqual(self.oceanarium.name, "Морской мир")
        self.assertEqual(self.oceanarium.location, "Москва")
        self.assertEqual(self.oceanarium.capacity, 5000)
        self.assertEqual(self.oceanarium.operational_status, "open")
        self.assertEqual(self.oceanarium.daily_visitors, 0)
        self.assertEqual(self.oceanarium.monthly_revenue, 0.0)

    def test_opening_hours_initialization(self):
        """Тест инициализации часов работы"""
        expected_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in expected_days:
            self.assertIn(day, self.oceanarium.opening_hours)
            self.assertIn("open", self.oceanarium.opening_hours[day])
            self.assertIn("close", self.oceanarium.opening_hours[day])

    def test_collections_initialization(self):
        """Тест инициализации коллекций"""
        self.assertIsInstance(self.oceanarium.animals, dict)
        self.assertIsInstance(self.oceanarium.tanks, dict)
        self.assertIsInstance(self.oceanarium.staff, dict)
        self.assertIsInstance(self.oceanarium.visitors, dict)
        self.assertIsInstance(self.oceanarium.equipment, dict)
        self.assertEqual(len(self.oceanarium.animals), 0)
        self.assertEqual(len(self.oceanarium.tanks), 0)

    def test_systems_initialization(self):
        """Тест инициализации систем управления"""
        self.assertIsNotNone(self.oceanarium.monitoring_system)
        self.assertIsNotNone(self.oceanarium.security_system)
        self.assertIsNotNone(self.oceanarium.payment_processor)
        self.assertIsInstance(self.oceanarium.bank_account, BankAccount)
        self.assertEqual(self.oceanarium.bank_account.holder_name, "Морской мир")

    def test_security_zones_initialization(self):
        """Тест инициализации зон безопасности"""
        expected_zones = ["PUBLIC_AREA", "STAFF_AREA", "ANIMAL_CARE", "RESTRICTED", "ADMIN"]
        for zone_id in expected_zones:
            self.assertIn(zone_id, self.oceanarium.security_system.access_zones)

    def test_weekend_hours(self):
        """Тест расширенных часов работы в выходные"""
        self.assertEqual(self.oceanarium.opening_hours["friday"]["close"], "20:00")
        self.assertEqual(self.oceanarium.opening_hours["saturday"]["open"], "08:00")
        self.assertEqual(self.oceanarium.opening_hours["saturday"]["close"], "20:00")
        self.assertEqual(self.oceanarium.opening_hours["sunday"]["open"], "08:00")

    def test_bank_account_setup(self):
        """Тест настройки банковского счета"""
        self.assertEqual(self.oceanarium.bank_account.balance, 1000000.0)
        self.assertEqual(self.oceanarium.bank_account.account_number, "OCN_MAIN_001")

    def test_initial_collections_empty(self):
        """Тест пустых начальных коллекций"""
        collections = [
            self.oceanarium.animals,
            self.oceanarium.tanks,
            self.oceanarium.staff,
            self.oceanarium.visitors,
            self.oceanarium.equipment,
            self.oceanarium.food_suppliers,
            self.oceanarium.educational_programs
        ]

        for collection in collections:
            self.assertEqual(len(collection), 0)

    def test_ticket_offices_initialization(self):
        """Тест инициализации кассовых офисов"""
        self.assertIsInstance(self.oceanarium.ticket_offices, list)
        self.assertEqual(len(self.oceanarium.ticket_offices), 0)

    def test_operational_status_default(self):
        """Тест статуса работы по умолчанию"""
        self.assertEqual(self.oceanarium.operational_status, "open")

    def test_inspection_date_set(self):
        """Тест установки даты последней инспекции"""
        self.assertIsNotNone(self.oceanarium.last_inspection_date)
        # Проверяем, что дата недавняя (в пределах минуты)
        time_diff = abs((datetime.now() - self.oceanarium.last_inspection_date).total_seconds())
        self.assertLess(time_diff, 60)


class TestOceanariumMethods(unittest.TestCase):
    """Тесты для методов класса Oceanarium"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.oceanarium = Oceanarium("Тестовый океанариум", "Тестовый город", 1000)

    def test_capacity_limit(self):
        """Тест ограничения вместимости"""
        self.assertEqual(self.oceanarium.capacity, 1000)
        # Можно добавить логику проверки превышения лимита в будущем

    def test_multiple_oceanarium_instances(self):
        """Тест создания нескольких экземпляров океанариума"""
        oceanarium2 = Oceanarium("Второй океанариум", "Другой город", 2000)

        self.assertNotEqual(self.oceanarium.name, oceanarium2.name)
        self.assertNotEqual(self.oceanarium.location, oceanarium2.location)
        self.assertNotEqual(self.oceanarium.capacity, oceanarium2.capacity)

        # Проверяем различие в именах владельцев счетов
        self.assertNotEqual(
            self.oceanarium.bank_account.holder_name,
            oceanarium2.bank_account.holder_name
        )

    def test_revenue_tracking(self):
        """Тест отслеживания доходов"""
        initial_revenue = self.oceanarium.monthly_revenue
        self.assertEqual(initial_revenue, 0.0)

        # Можно добавить методы увеличения дохода в будущем
        self.oceanarium.monthly_revenue += 1000.0
        self.assertEqual(self.oceanarium.monthly_revenue, 1000.0)

    def test_visitor_tracking(self):
        """Тест отслеживания посетителей"""
        initial_visitors = self.oceanarium.daily_visitors
        self.assertEqual(initial_visitors, 0)

        # Можно добавить методы учета посетителей в будущем
        self.oceanarium.daily_visitors += 50
        self.assertEqual(self.oceanarium.daily_visitors, 50)


if __name__ == '__main__':
    unittest.main()
