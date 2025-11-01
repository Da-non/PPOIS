"""
Интеграционные тесты для системы океанариума
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.oceanarium import Oceanarium
from oceanarium.core import MarineAnimal
from oceanarium.equipment import Tank, WaterPump, FilterSystem, TemperatureController
from oceanarium.management import Jellyfish, Octopus, Stingray, SeaHorse
from oceanarium.finance import BankAccount, CreditCard
from oceanarium.exceptions import *


class TestOceanariumIntegration(unittest.TestCase):
    """Интеграционные тесты для всей системы океанариума"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.oceanarium = Oceanarium("Интеграционный океанариум", "Тестовый город", 2000)

        # Создаем тестовые резервуары
        self.tank1 = Tank("TANK001", 100000.0, "display")
        self.tank2 = Tank("TANK002", 50000.0, "quarantine")

        # Создаем тестовых животных
        self.jellyfish = Jellyfish("JELLY001", "Медуза", 2, 5.0)
        self.octopus = Octopus("OCTO001", "Осьминог", 3, 15.0)
        self.stingray = Stingray("STING001", "Скат", 5, 50.0)
        self.seahorse = SeaHorse("HORSE001", "Морской конек", 1, 0.5, "male")

    def test_tank_animal_integration(self):
        """Тест интеграции резервуара и животных"""
        # Добавляем животных в резервуар
        result1 = self.tank1.add_animal(self.jellyfish)
        result2 = self.tank1.add_animal(self.octopus)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(len(self.tank1.animals), 2)
        self.assertEqual(self.jellyfish.tank_id, "TANK001")
        self.assertEqual(self.octopus.tank_id, "TANK001")

    def test_tank_equipment_integration(self):
        """Тест интеграции резервуара и оборудования"""
        # Создаем оборудование
        pump = WaterPump("PUMP001", "Основной насос", "AquaTech", 500.0)
        filter_sys = FilterSystem("FILTER001", "Биофильтр", "AquaClean", 1000.0)
        temp_controller = TemperatureController("TEMP001", "Термостат", "TempControl", 2000.0)

        # Добавляем в резервуар
        self.tank1.add_equipment(pump)
        self.tank1.add_equipment(filter_sys)
        self.tank1.add_equipment(temp_controller)

        self.assertEqual(len(self.tank1.equipment), 3)

    def test_monitoring_system_integration(self):
        """Тест интеграции системы мониторинга"""
        monitoring = self.oceanarium.monitoring_system

        # Добавляем датчики для резервуара
        temp_sensor = monitoring.add_sensor("temperature", "center", "TANK001")
        ph_sensor = monitoring.add_sensor("ph", "bottom", "TANK001")
        salinity_sensor = monitoring.add_sensor("salinity", "surface", "TANK001")

        self.assertEqual(len(monitoring.sensors), 3)

        # Считываем данные с датчиков
        temp_data = monitoring.read_sensor_data(temp_sensor)
        ph_data = monitoring.read_sensor_data(ph_sensor)
        salinity_data = monitoring.read_sensor_data(salinity_sensor)

        self.assertIsNotNone(temp_data)
        self.assertIsNotNone(ph_data)
        self.assertIsNotNone(salinity_data)
        self.assertEqual(len(monitoring.data_logs), 3)

    def test_security_system_integration(self):
        """Тест интеграции системы безопасности"""
        security = self.oceanarium.security_system

        # Выдаем карты доступа
        admin_card = security.issue_keycard("ADMIN001", "Администратор", 5)
        staff_card = security.issue_keycard("STAFF001", "Сотрудник", 3)
        visitor_card = security.issue_keycard("VISITOR001", "Посетитель", 1)

        # Проверяем доступ к разным зонам
        admin_access = security.check_access(admin_card, "ADMIN")
        staff_access = security.check_access(staff_card, "ANIMAL_CARE")
        visitor_access = security.check_access(visitor_card, "PUBLIC_AREA")

        self.assertTrue(admin_access)
        self.assertTrue(staff_access)
        self.assertTrue(visitor_access)

        # Проверяем отказ в доступе
        with self.assertRaises(UnauthorizedAccessException):
            security.check_access(visitor_card, "ADMIN")

    def test_financial_system_integration(self):
        """Тест интеграции финансовой системы"""
        bank_account = self.oceanarium.bank_account
        initial_balance = bank_account.balance

        # Пополнение от продажи билетов
        ticket_revenue = 50000.0
        bank_account.deposit(ticket_revenue, "Продажа билетов")

        # Расходы на корм
        food_expense = 10000.0
        bank_account.withdraw(food_expense, "Закупка корма")

        expected_balance = initial_balance + ticket_revenue - food_expense
        self.assertEqual(bank_account.balance, expected_balance)
        self.assertEqual(len(bank_account.transactions), 2)

    def test_animal_feeding_cycle(self):
        """Тест цикла кормления животных"""
        # Добавляем животных в резервуар
        self.tank1.add_animal(self.jellyfish)
        self.tank1.add_animal(self.octopus)

        # Проверяем требования к кормлению
        jellyfish_req = self.jellyfish.get_feeding_requirements()
        octopus_req = self.octopus.get_feeding_requirements()

        self.assertIn("plankton", jellyfish_req)
        self.assertIn("crabs", octopus_req)

        # Кормим животных
        jellyfish_fed = self.jellyfish.feed("plankton", jellyfish_req["plankton"])
        octopus_fed = self.octopus.feed("crabs", octopus_req["crabs"])

        self.assertTrue(jellyfish_fed)
        self.assertTrue(octopus_fed)
        self.assertIsNotNone(self.jellyfish.last_feeding)
        self.assertIsNotNone(self.octopus.last_feeding)

    def test_water_quality_monitoring(self):
        """Тест мониторинга качества воды"""
        # Устанавливаем плохие параметры воды
        self.tank1.water_parameters["temperature"] = 35.0  # Слишком высоко
        self.tank1.water_parameters["ammonia"] = 1.0       # Слишком высоко

        # Проверяем качество воды
        quality_check = self.tank1.check_water_quality()

        self.assertFalse(quality_check["temperature"])
        self.assertFalse(quality_check["ammonia"])

        # Очищаем резервуар
        self.tank1.clean_tank()

        # Проверяем улучшение параметров
        self.assertLess(self.tank1.water_parameters["ammonia"], 1.0)

    def test_equipment_maintenance_cycle(self):
        """Тест цикла обслуживания оборудования"""
        pump = WaterPump("PUMP001", "Основной насос", "AquaTech", 500.0)

        # Симулируем поломку
        pump.status = "malfunction"
        pump.error_codes = ["ERR_1234"]

        self.assertEqual(pump.status, "malfunction")

        # Выполняем обслуживание
        maintenance_result = pump.perform_maintenance()

        self.assertTrue(maintenance_result)
        self.assertEqual(pump.status, "operational")
        self.assertEqual(len(pump.error_codes), 0)

    def test_emergency_response_integration(self):
        """Тест интеграции системы экстренного реагирования"""
        # Активируем режим чрезвычайной ситуации
        self.oceanarium.security_system.activate_emergency_mode()

        self.assertTrue(self.oceanarium.security_system.emergency_mode)

        # Проверяем блокировку зон
        for zone in self.oceanarium.security_system.access_zones.values():
            self.assertTrue(zone["emergency_lockdown"])

    def test_visitor_payment_flow(self):
        """Тест процесса оплаты посетителями"""
        # Создаем кредитную карту
        expiry_date = datetime.now() + timedelta(days=365)
        card = CreditCard("1234567890123456", "Иван Петров", expiry_date, "123")

        # Симулируем покупку билета
        ticket_price = 1500.0
        charge_result = card.charge(ticket_price, "Океанариум билет")

        self.assertTrue(charge_result)
        self.assertEqual(card.current_balance, ticket_price)

        # Пополняем счет океанариума
        self.oceanarium.bank_account.deposit(ticket_price, "Продажа билета")

        # Увеличиваем счетчик посетителей
        self.oceanarium.daily_visitors += 1
        self.oceanarium.monthly_revenue += ticket_price

        self.assertEqual(self.oceanarium.daily_visitors, 1)
        self.assertEqual(self.oceanarium.monthly_revenue, ticket_price)


class TestAnimalCompatibility(unittest.TestCase):
    """Тесты совместимости животных"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.tank = Tank("COMPAT_TANK", 200000.0, "display")

    def test_compatible_animals(self):
        """Тест совместимых животных"""
        jellyfish1 = Jellyfish("JELLY001", "Медуза 1", 2, 5.0)
        jellyfish2 = Jellyfish("JELLY002", "Медуза 2", 3, 7.0)

        # Медузы должны быть совместимы друг с другом
        result1 = self.tank.add_animal(jellyfish1)
        result2 = self.tank.add_animal(jellyfish2)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(len(self.tank.animals), 2)

    def test_habitat_requirements_consistency(self):
        """Тест согласованности требований среды обитания"""
        animals = [
            Jellyfish("JELLY001", "Медуза", 2, 5.0),
            Octopus("OCTO001", "Осьминог", 3, 15.0),
            Stingray("STING001", "Скат", 5, 50.0),
            SeaHorse("HORSE001", "Морской конек", 1, 0.5, "male")
        ]

        # Все морские животные должны требовать соленую воду
        for animal in animals:
            habitat_req = animal.get_habitat_requirements()
            self.assertEqual(habitat_req["water_type"], "saltwater")

    def test_feeding_schedule_conflicts(self):
        """Тест конфликтов расписания кормления"""
        jellyfish = Jellyfish("JELLY001", "Медуза", 2, 5.0)

        # Первое кормление
        first_feeding = jellyfish.feed("plankton", 1.0)
        self.assertTrue(first_feeding)

        # Попытка покормить сразу же (должна провалиться)
        second_feeding = jellyfish.feed("plankton", 1.0)
        self.assertFalse(second_feeding)


class TestSystemFailures(unittest.TestCase):
    """Тесты отказов системы и обработки ошибок"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.oceanarium = Oceanarium("Тестовый океанариум", "Тест", 1000)

    def test_insufficient_funds_handling(self):
        """Тест обработки недостатка средств"""
        account = BankAccount("TEST001", "Тестовый счет", 1000.0)

        with self.assertRaises(InsufficientFundsException):
            account.withdraw(2000.0, "Превышение баланса")

    def test_equipment_malfunction_handling(self):
        """Тест обработки поломки оборудования"""
        pump = WaterPump("PUMP001", "Тестовый насос", "TestCorp", 500.0)

        # Симулируем поломку
        pump.status = "malfunction"
        pump.error_codes = ["ERR_CRITICAL"]

        # Проверяем обнаружение поломки
        self.assertEqual(pump.check_status(), "malfunction")
        self.assertIn("ERR_CRITICAL", pump.error_codes)

    def test_invalid_temperature_handling(self):
        """Тест обработки недопустимой температуры"""
        controller = TemperatureController("TEMP001", "Контроллер", "TempCorp", 1000.0)

        with self.assertRaises(InvalidTemperatureException):
            controller.set_temperature(50.0)  # Слишком высоко

    def test_animal_not_found_handling(self):
        """Тест обработки отсутствующего животного"""
        tank = Tank("TANK001", 50000.0, "display")

        with self.assertRaises(AnimalNotFoundException):
            tank.remove_animal("NONEXISTENT")

    def test_unauthorized_access_handling(self):
        """Тест обработки неавторизованного доступа"""
        security = self.oceanarium.security_system

        # Создаем пользователя с низкими правами
        low_access_card = security.issue_keycard("USER001", "Пользователь", 1)

        # Пытаемся получить доступ к административной зоне
        with self.assertRaises(UnauthorizedAccessException):
            security.check_access(low_access_card, "ADMIN")


if __name__ == '__main__':
    unittest.main()
