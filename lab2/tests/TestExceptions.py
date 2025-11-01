"""
Юнит тесты для модуля exceptions.py
"""

import unittest
from datetime import datetime
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.exceptions import *


class TestOceanariumExceptions(unittest.TestCase):
    """Тесты для всех исключений океанариума"""

    def test_oceanarium_base_exception(self):
        """Тест базового исключения"""
        with self.assertRaises(OceanariumBaseException):
            raise OceanariumBaseException("Тестовая ошибка")

    def test_animal_not_found_exception(self):
        """Тест исключения животное не найдено"""
        animal_id = "ANIMAL001"
        with self.assertRaises(AnimalNotFoundException) as context:
            raise AnimalNotFoundException(animal_id)

        exception = context.exception
        self.assertEqual(exception.animal_id, animal_id)
        self.assertIn(animal_id, str(exception))

    def test_insufficient_funds_exception(self):
        """Тест исключения недостаточно средств"""
        required = 1000.0
        available = 500.0

        with self.assertRaises(InsufficientFundsException) as context:
            raise InsufficientFundsException(required, available)

        exception = context.exception
        self.assertEqual(exception.required_amount, required)
        self.assertEqual(exception.available_amount, available)
        self.assertIn(str(required), str(exception))
        self.assertIn(str(available), str(exception))

    def test_invalid_password_exception(self):
        """Тест исключения неверный пароль"""
        username = "test_user"

        with self.assertRaises(InvalidPasswordException) as context:
            raise InvalidPasswordException(username)

        exception = context.exception
        self.assertEqual(exception.username, username)
        self.assertIn(username, str(exception))

    def test_tank_overflow_exception(self):
        """Тест исключения переполнение резервуара"""
        tank_id = "TANK001"
        capacity = 1000.0
        attempted_volume = 1200.0

        with self.assertRaises(TankOverflowException) as context:
            raise TankOverflowException(tank_id, capacity, attempted_volume)

        exception = context.exception
        self.assertEqual(exception.tank_id, tank_id)
        self.assertEqual(exception.capacity, capacity)
        self.assertEqual(exception.attempted_volume, attempted_volume)
        self.assertIn(tank_id, str(exception))

    def test_equipment_malfunction_exception(self):
        """Тест исключения неисправность оборудования"""
        equipment_name = "Водяной насос"
        error_code = "ERR_1234"

        with self.assertRaises(EquipmentMalfunctionException) as context:
            raise EquipmentMalfunctionException(equipment_name, error_code)

        exception = context.exception
        self.assertEqual(exception.equipment_name, equipment_name)
        self.assertEqual(exception.error_code, error_code)
        self.assertIn(equipment_name, str(exception))
        self.assertIn(error_code, str(exception))

    def test_unauthorized_access_exception(self):
        """Тест исключения неавторизованный доступ"""
        user_role = "visitor"
        required_role = "admin"

        with self.assertRaises(UnauthorizedAccessException) as context:
            raise UnauthorizedAccessException(user_role, required_role)

        exception = context.exception
        self.assertEqual(exception.user_role, user_role)
        self.assertEqual(exception.required_role, required_role)
        self.assertIn(user_role, str(exception))
        self.assertIn(required_role, str(exception))

    def test_feeding_schedule_conflict_exception(self):
        """Тест исключения конфликт расписания кормления"""
        animal_id = "ANIMAL001"
        feeding_time = datetime.now()

        with self.assertRaises(FeedingScheduleConflictException) as context:
            raise FeedingScheduleConflictException(animal_id, feeding_time)

        exception = context.exception
        self.assertEqual(exception.animal_id, animal_id)
        self.assertEqual(exception.feeding_time, feeding_time)
        self.assertIn(animal_id, str(exception))

    def test_invalid_temperature_exception(self):
        """Тест исключения недопустимая температура"""
        current_temp = 35.0
        min_temp = 20.0
        max_temp = 30.0

        with self.assertRaises(InvalidTemperatureException) as context:
            raise InvalidTemperatureException(current_temp, min_temp, max_temp)

        exception = context.exception
        self.assertEqual(exception.current_temp, current_temp)
        self.assertEqual(exception.min_temp, min_temp)
        self.assertEqual(exception.max_temp, max_temp)
        self.assertIn(str(current_temp), str(exception))

    def test_ticket_expired_exception(self):
        """Тест исключения просроченный билет"""
        ticket_id = "TICKET001"
        expiry_date = datetime.now()

        with self.assertRaises(TicketExpiredException) as context:
            raise TicketExpiredException(ticket_id, expiry_date)

        exception = context.exception
        self.assertEqual(exception.ticket_id, ticket_id)
        self.assertEqual(exception.expiry_date, expiry_date)
        self.assertIn(ticket_id, str(exception))

    def test_maintenance_mode_exception(self):
        """Тест исключения режим обслуживания"""
        area_name = "Акулий зал"
        maintenance_end_time = datetime.now()

        with self.assertRaises(MaintenanceModeException) as context:
            raise MaintenanceModeException(area_name, maintenance_end_time)

        exception = context.exception
        self.assertEqual(exception.area_name, area_name)
        self.assertEqual(exception.maintenance_end_time, maintenance_end_time)
        self.assertIn(area_name, str(exception))

    def test_animal_health_exception(self):
        """Тест исключения проблемы со здоровьем животного"""
        animal_id = "ANIMAL001"
        health_issue = "Инфекция"

        with self.assertRaises(AnimalHealthException) as context:
            raise AnimalHealthException(animal_id, health_issue)

        exception = context.exception
        self.assertEqual(exception.animal_id, animal_id)
        self.assertEqual(exception.health_issue, health_issue)
        self.assertIn(animal_id, str(exception))
        self.assertIn(health_issue, str(exception))

    def test_inheritance_chain(self):
        """Тест наследования исключений"""
        # Все исключения должны наследоваться от OceanariumBaseException
        exceptions_to_test = [
            AnimalNotFoundException("test"),
            InsufficientFundsException(100, 50),
            InvalidPasswordException("test"),
            TankOverflowException("tank", 100, 150),
            EquipmentMalfunctionException("pump", "ERR123"),
            UnauthorizedAccessException("user", "admin"),
            FeedingScheduleConflictException("animal", datetime.now()),
            InvalidTemperatureException(35, 20, 30),
            TicketExpiredException("ticket", datetime.now()),
            MaintenanceModeException("area", datetime.now()),
            AnimalHealthException("animal", "issue")
        ]

        for exception in exceptions_to_test:
            self.assertIsInstance(exception, OceanariumBaseException)
            self.assertIsInstance(exception, Exception)


if __name__ == '__main__':
    unittest.main()
