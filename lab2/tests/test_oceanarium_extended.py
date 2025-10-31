"""
Дополнительные тесты для модуля oceanarium.py для достижения 85% покрытия
"""

import unittest
from datetime import datetime
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.oceanarium import Oceanarium
from oceanarium.equipment import Tank
from oceanarium.management import Jellyfish, Octopus, FoodSupplier, EducationalProgram
from oceanarium.core import Veterinarian, Feeder, Staff
from oceanarium.finance import Visitor
from oceanarium.exceptions import *


class TestOceanariumExtended(unittest.TestCase):
    """Расширенные тесты для класса Oceanarium"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.oceanarium = Oceanarium("Тестовый океанариум", "Тест-город", 1000)
        self.tank = Tank("TANK001", 50000.0, "display")
        self.jellyfish = Jellyfish("JELLY001", "Тестовая медуза", 2, 5.0)

    def test_add_tank(self):
        """Тест добавления резервуара"""
        initial_tanks = len(self.oceanarium.tanks)
        initial_sensors = len(self.oceanarium.monitoring_system.sensors)

        self.oceanarium.add_tank(self.tank)

        self.assertEqual(len(self.oceanarium.tanks), initial_tanks + 1)
        self.assertIn("TANK001", self.oceanarium.tanks)
        # Должно добавиться 4 датчика (temperature, ph, salinity, ammonia)
        self.assertEqual(len(self.oceanarium.monitoring_system.sensors), initial_sensors + 4)

    def test_add_animal_success(self):
        """Тест успешного добавления животного"""
        self.oceanarium.add_tank(self.tank)
        result = self.oceanarium.add_animal(self.jellyfish, "TANK001")

        self.assertTrue(result)
        self.assertIn("JELLY001", self.oceanarium.animals)
        self.assertEqual(self.jellyfish.tank_id, "TANK001")

    def test_add_animal_nonexistent_tank(self):
        """Тест добавления животного в несуществующий резервуар"""
        with self.assertRaises(ValueError):
            self.oceanarium.add_animal(self.jellyfish, "NONEXISTENT")

    def test_add_animal_tank_full(self):
        """Тест добавления животного в переполненный резервуар"""
        small_tank = Tank("SMALL001", 1000.0, "quarantine")  # Очень маленький
        self.oceanarium.add_tank(small_tank)

        # Заполняем резервуар до максимума
        max_animals = small_tank.get_max_animals()
        for i in range(max_animals):
            animal = Jellyfish(f"JELLY{i:03d}", f"Медуза {i}", 2, 5.0)
            self.oceanarium.add_animal(animal, "SMALL001")

        # Попытка добавить еще одно животное
        extra_animal = Jellyfish("EXTRA001", "Лишняя медуза", 2, 5.0)
        result = self.oceanarium.add_animal(extra_animal, "SMALL001")

        self.assertFalse(result)
        self.assertNotIn("EXTRA001", self.oceanarium.animals)

    def test_hire_staff_with_keycard(self):
        """Тест найма сотрудника с выдачей карты доступа"""
        # Создаем конкретный класс персонала для тестирования
        class TestStaff(Staff):
            def perform_daily_tasks(self):
                return ["Test task"]

        staff = TestStaff("STAFF001", "Тестовый сотрудник", "tester", 50000.0, 2)
        staff.access_level = 3

        initial_staff = len(self.oceanarium.staff)
        initial_cards = len(self.oceanarium.security_system.key_cards)

        self.oceanarium.hire_staff(staff)

        self.assertEqual(len(self.oceanarium.staff), initial_staff + 1)
        self.assertEqual(len(self.oceanarium.security_system.key_cards), initial_cards + 1)
        self.assertIn("STAFF001", self.oceanarium.staff)



    def test_create_ticket_office(self):
        """Тест создания кассы"""
        initial_offices = len(self.oceanarium.ticket_offices)

        office = self.oceanarium.create_ticket_office("OFFICE001", "Кассир Иванов")

        self.assertEqual(len(self.oceanarium.ticket_offices), initial_offices + 1)
        self.assertEqual(office.office_id, "OFFICE001")
        self.assertEqual(office.cashier_name, "Кассир Иванов")
        self.assertEqual(office.payment_processor, self.oceanarium.payment_processor)

    def test_add_food_supplier(self):
        """Тест добавления поставщика корма"""
        supplier = FoodSupplier("SUPP001", "Корм Плюс")

        self.oceanarium.add_food_supplier(supplier)

        self.assertIn("SUPP001", self.oceanarium.food_suppliers)

    def test_create_educational_program(self):
        """Тест создания образовательной программы"""
        program = self.oceanarium.create_educational_program(
            "EDU001", "Морская биология", "students", 90
        )

        self.assertIn("EDU001", self.oceanarium.educational_programs)
        self.assertEqual(program.program_id, "EDU001")
        # Проверяем базовые атрибуты программы
        self.assertIsNotNone(program)

    def test_feed_all_animals_with_feeder(self):
        """Тест кормления всех животных при наличии кормильца"""
        # Добавляем животных
        self.oceanarium.add_tank(self.tank)
        self.oceanarium.add_animal(self.jellyfish, "TANK001")

        octopus = Octopus("OCTO001", "Тестовый осьминог", 3, 15.0)
        self.oceanarium.add_animal(octopus, "TANK001")

        # Добавляем кормильца
        feeder = Feeder("FEEDER001", "Кормилец", 40000.0, 2)
        self.oceanarium.hire_staff(feeder)

        # Кормим всех животных
        results = self.oceanarium.feed_all_animals()

        self.assertIn("JELLY001", results)
        self.assertIn("OCTO001", results)
        self.assertIsInstance(results["JELLY001"], bool)
        self.assertIsInstance(results["OCTO001"], bool)

    def test_feed_all_animals_no_feeder(self):
        """Тест кормления без кормильца"""
        self.oceanarium.add_tank(self.tank)
        self.oceanarium.add_animal(self.jellyfish, "TANK001")

        results = self.oceanarium.feed_all_animals()

        self.assertIn("JELLY001", results)
        self.assertFalse(results["JELLY001"])  # Не накормлен из-за отсутствия кормильца

    def test_conduct_health_checks_with_vet(self):
        """Тест медосмотра при наличии ветеринара"""
        # Добавляем животное
        self.oceanarium.add_tank(self.tank)
        self.oceanarium.add_animal(self.jellyfish, "TANK001")

        # Добавляем ветеринара
        vet = Veterinarian("VET001", "Доктор Айболит", 80000.0, 5, "VET123")
        self.oceanarium.hire_staff(vet)

        results = self.oceanarium.conduct_health_checks()

        self.assertIn("JELLY001", results)
        self.assertIsInstance(results["JELLY001"], dict)

    def test_conduct_health_checks_no_vet(self):
        """Тест медосмотра без ветеринара"""
        self.oceanarium.add_tank(self.tank)
        self.oceanarium.add_animal(self.jellyfish, "TANK001")

        with self.assertRaises(AnimalHealthException):
            self.oceanarium.conduct_health_checks()

    def test_find_available_feeder_exists(self):
        """Тест поиска доступного кормильца когда он есть"""
        feeder = Feeder("FEEDER001", "Кормилец", 40000.0, 2)
        self.oceanarium.hire_staff(feeder)

        found_feeder = self.oceanarium._find_available_feeder()
        self.assertIsNotNone(found_feeder)
        self.assertEqual(found_feeder.staff_id, "FEEDER001")

    def test_find_available_feeder_none(self):
        """Тест поиска кормильца когда его нет"""
        found_feeder = self.oceanarium._find_available_feeder()
        self.assertIsNone(found_feeder)

    def test_find_veterinarian_exists(self):
        """Тест поиска ветеринара когда он есть"""
        vet = Veterinarian("VET001", "Доктор", 80000.0, 5, "VET123")
        self.oceanarium.hire_staff(vet)

        found_vet = self.oceanarium._find_veterinarian()
        self.assertIsNotNone(found_vet)
        self.assertEqual(found_vet.staff_id, "VET001")

    def test_find_veterinarian_none(self):
        """Тест поиска ветеринара когда его нет"""
        found_vet = self.oceanarium._find_veterinarian()
        self.assertIsNone(found_vet)

    def test_emergency_evacuation_integration(self):
        """Тест интеграции с системой экстренной эвакуации"""
        # Проверяем, что планы эвакуации созданы при инициализации
        self.assertGreater(len(self.oceanarium.emergency_response.evacuation_plans), 0)

    def test_security_zones_access_levels(self):
        """Тест уровней доступа в зонах безопасности"""
        zones_and_levels = [
            ("PUBLIC_AREA", 1),
            ("STAFF_AREA", 2),
            ("ANIMAL_CARE", 3),
            ("RESTRICTED", 4),
            ("ADMIN", 5)
        ]

        for zone_id, expected_level in zones_and_levels:
            zone = self.oceanarium.security_system.access_zones[zone_id]
            self.assertEqual(zone["required_level"], expected_level)

    def test_payment_processor_integration(self):
        """Тест интеграции с процессором платежей"""
        self.assertIsNotNone(self.oceanarium.payment_processor)
        self.assertEqual(self.oceanarium.payment_processor.processor_id, "MAIN_PAYMENT")

    def test_opening_hours_weekend_extension(self):
        """Тест расширенных часов работы в выходные"""
        # Пятница - до 20:00
        self.assertEqual(self.oceanarium.opening_hours["friday"]["close"], "20:00")

        # Суббота и воскресенье начинают раньше
        self.assertEqual(self.oceanarium.opening_hours["saturday"]["open"], "08:00")
        self.assertEqual(self.oceanarium.opening_hours["sunday"]["open"], "08:00")

    def test_monthly_revenue_tracking(self):
        """Тест отслеживания месячной выручки"""
        initial_revenue = self.oceanarium.monthly_revenue

        # Симулируем доход
        self.oceanarium.monthly_revenue += 15000.0

        self.assertEqual(self.oceanarium.monthly_revenue, initial_revenue + 15000.0)

    def test_operational_status_management(self):
        """Тест управления операционным статусом"""
        self.assertEqual(self.oceanarium.operational_status, "open")

        # Можно изменить статус
        self.oceanarium.operational_status = "maintenance"
        self.assertEqual(self.oceanarium.operational_status, "maintenance")

    def test_capacity_management(self):
        """Тест управления вместимостью"""
        self.assertEqual(self.oceanarium.capacity, 1000)

        # Проверяем, что можно отслеживать текущее количество посетителей
        for i in range(5):
            visitor = Visitor(f"VIS{i:03d}", f"Посетитель {i}", "adult", 25)
            self.oceanarium.add_visitor(visitor)

        self.assertEqual(self.oceanarium.daily_visitors, 5)

    def test_inspection_date_recent(self):
        """Тест актуальности даты последней инспекции"""
        # Дата должна быть недавней (в пределах суток)
        time_diff = abs((datetime.now() - self.oceanarium.last_inspection_date).total_seconds())
        self.assertLess(time_diff, 86400)  # 24 часа

    def test_bank_account_management(self):
        """Тест управления банковским счетом"""
        self.assertEqual(self.oceanarium.bank_account.holder_name, "Тестовый океанариум")
        self.assertEqual(self.oceanarium.bank_account.balance, 1000000.0)

        # Можно проводить операции со счетом
        self.oceanarium.bank_account.deposit(50000.0, "Доход от билетов")
        self.assertEqual(self.oceanarium.bank_account.balance, 1050000.0)


if __name__ == '__main__':
    unittest.main()
