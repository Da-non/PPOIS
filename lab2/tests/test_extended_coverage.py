"""
Дополнительные тесты для достижения максимального покрытия кода
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.core import MarineAnimal
from oceanarium.equipment import MonitoringSystem, SecuritySystem
from oceanarium.management import Jellyfish, Octopus, Stingray, SeaHorse
from oceanarium.finance import BankAccount, CreditCard
from oceanarium.exceptions import *


class TestMonitoringSystemExtended(unittest.TestCase):
    """Расширенные тесты системы мониторинга"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.monitoring = MonitoringSystem("EXT_MON")

    def test_sensor_calibration_tracking(self):
        """Тест отслеживания калибровки датчиков"""
        sensor_id = self.monitoring.add_sensor("temperature", "test_location", "TANK001")
        sensor = self.monitoring.sensors[0]

        # Проверяем дату калибровки
        self.assertIsNotNone(sensor["calibration_date"])
        self.assertLessEqual(
            abs((datetime.now() - sensor["calibration_date"]).total_seconds()),
            60
        )

    def test_alert_lifecycle(self):
        """Тест жизненного цикла предупреждений"""
        self.monitoring.create_alert("SENS001", "temperature", 35.0, "high")

        alert = self.monitoring.alerts[0]
        alert_id = alert["alert_id"]

        # Изначально не подтверждено и не решено
        self.assertFalse(alert["acknowledged"])
        self.assertFalse(alert["resolved"])

        # Подтверждаем предупреждение
        result = self.monitoring.acknowledge_alert(alert_id)
        self.assertTrue(result)
        self.assertTrue(alert["acknowledged"])

    def test_data_logging_integrity(self):
        """Тест целостности журналирования данных"""
        sensor_id = self.monitoring.add_sensor("ph", "test_location", "TANK001")

        # Считываем данные несколько раз
        for i in range(5):
            self.monitoring.read_sensor_data(sensor_id)

        # Проверяем, что все записи сохранены
        self.assertEqual(len(self.monitoring.data_logs), 5)

        # Проверяем структуру записей
        for log_entry in self.monitoring.data_logs:
            self.assertIn("sensor_id", log_entry)
            self.assertIn("value", log_entry)
            self.assertIn("timestamp", log_entry)

    def test_backup_systems(self):
        """Тест резервных систем"""
        # Изначально нет резервных систем
        self.assertEqual(len(self.monitoring.backup_systems), 0)

        # Можно добавить резервные системы
        self.monitoring.backup_systems.append("BACKUP_MON_001")
        self.assertEqual(len(self.monitoring.backup_systems), 1)

    def test_notification_system(self):
        """Тест системы уведомлений"""
        # Изначально нет email-адресов для уведомлений
        self.assertEqual(len(self.monitoring.notification_emails), 0)

        # Добавляем email для уведомлений
        self.monitoring.notification_emails.append("admin@oceanarium.com")
        self.assertEqual(len(self.monitoring.notification_emails), 1)

    @patch('random.uniform')
    def test_sensor_readings_by_type(self, mock_uniform):
        """Тест чтения разных типов датчиков"""
        sensor_types = ["temperature", "ph", "salinity", "oxygen"]
        expected_values = [24.5, 8.1, 35.0, 7.5]

        for sensor_type, expected_value in zip(sensor_types, expected_values):
            mock_uniform.return_value = expected_value
            sensor_id = self.monitoring.add_sensor(sensor_type, "test", "TANK001")

            value = self.monitoring.read_sensor_data(sensor_id)
            self.assertEqual(value, expected_value)


class TestSecuritySystemExtended(unittest.TestCase):
    """Расширенные тесты системы безопасности"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.security = SecuritySystem("EXT_SEC")

    def test_keycard_expiration(self):
        """Тест истечения срока действия карт"""
        # Выдаем карту
        card_id = self.security.issue_keycard("USER001", "Тестовый пользователь", 3)
        keycard = self.security.key_cards[0]

        # Устанавливаем истекший срок
        keycard["expires_date"] = datetime.now() - timedelta(days=1)

        # Создаем зону доступа
        self.security.create_access_zone("TEST_ZONE", "Тестовая зона", 2)

        # Попытка доступа с просроченной картой
        result = self.security.check_access(card_id, "TEST_ZONE")
        self.assertFalse(result)

    def test_zone_occupancy_tracking(self):
        """Тест отслеживания заполненности зон"""
        self.security.create_access_zone("TRACK_ZONE", "Отслеживаемая зона", 2)
        card_id = self.security.issue_keycard("USER001", "Пользователь", 3)

        # Предоставляем доступ
        self.security.check_access(card_id, "TRACK_ZONE")

        # Проверяем, что пользователь добавлен в зону
        occupants = self.security.access_zones["TRACK_ZONE"]["current_occupants"]
        self.assertIn("USER001", occupants)

    def test_access_attempts_logging(self):
        """Тест журналирования попыток доступа"""
        self.security.create_access_zone("LOG_ZONE", "Журналируемая зона", 2)
        card_id = self.security.issue_keycard("USER001", "Пользователь", 3)

        # Несколько попыток доступа
        for i in range(3):
            self.security.check_access(card_id, "LOG_ZONE")

        # Проверяем журнал
        access_events = [log for log in self.security.security_logs
                        if log["event_type"] == "access_granted"]
        self.assertEqual(len(access_events), 3)

    def test_camera_and_sensor_systems(self):
        """Тест камер и датчиков движения"""
        # Изначально нет камер и датчиков
        self.assertEqual(len(self.security.cameras), 0)
        self.assertEqual(len(self.security.motion_sensors), 0)

        # Можно добавить оборудование
        self.security.cameras.append({"id": "CAM001", "location": "Entrance"})
        self.security.motion_sensors.append({"id": "MOTION001", "zone": "Hall"})

        self.assertEqual(len(self.security.cameras), 1)
        self.assertEqual(len(self.security.motion_sensors), 1)

    def test_alarm_system(self):
        """Тест системы сигнализации"""
        # Изначально сигнализация отключена
        self.assertEqual(self.security.alarm_status, "disarmed")

        # Можно изменить статус
        self.security.alarm_status = "armed"
        self.assertEqual(self.security.alarm_status, "armed")


class TestAnimalBehaviorExtended(unittest.TestCase):
    """Расширенные тесты поведения животных"""

    def test_jellyfish_regeneration(self):
        """Тест способности к регенерации медузы"""
        jellyfish = Jellyfish("REGEN_JELLY", "Регенерирующая медуза", 2, 5.0)

        # Проверяем способность к регенерации
        self.assertGreaterEqual(jellyfish.regeneration_ability, 50)
        self.assertLessEqual(jellyfish.regeneration_ability, 95)

    def test_octopus_ink_capacity_regeneration(self):
        """Тест восстановления чернильного запаса осьминога"""
        octopus = Octopus("INK_OCTO", "Чернильный осьминог", 3, 15.0)

        initial_capacity = octopus.ink_capacity

        # Используем чернила
        octopus.release_ink()
        self.assertLess(octopus.ink_capacity, initial_capacity)

        # В реальной системе чернила бы постепенно восстанавливались
        # Здесь можно добавить метод restore_ink()

    def test_stingray_burial_behavior(self):
        """Тест поведения зарывания ската"""
        stingray = Stingray("BURY_RAY", "Зарывающийся скат", 5, 50.0)

        initial_stress = stingray.stress_level
        initial_activity = stingray.activity_level

        # Зарываемся в песок
        result = stingray.bury_in_sand()

        self.assertTrue(result)
        self.assertLessEqual(stingray.stress_level, initial_stress)
        self.assertLess(stingray.activity_level, initial_activity)

    def test_seahorse_grip_strength_variation(self):
        """Тест вариации силы хватки морского конька"""
        seahorse = SeaHorse("GRIP_HORSE", "Сильный конек", 1, 0.5, "male")

        # Сила хватки должна быть в разумных пределах
        self.assertGreaterEqual(seahorse.grip_strength, 10)
        self.assertLessEqual(seahorse.grip_strength, 50)

        # Тестируем хватание объектов разной прочности
        weak_object = 5.0
        strong_object = 100.0

        self.assertTrue(seahorse.grip_with_tail(weak_object))
        self.assertFalse(seahorse.grip_with_tail(strong_object))


class TestFinancialSystemExtended(unittest.TestCase):
    """Расширенные тесты финансовой системы"""

    def test_transaction_uuid_uniqueness(self):
        """Тест уникальности UUID транзакций"""
        account = BankAccount("UUID_TEST", "Тестовый счет", 10000.0)

        # Выполняем несколько транзакций
        for i in range(10):
            account.deposit(100.0, f"Депозит {i}")

        # Проверяем уникальность ID транзакций
        transaction_ids = [t["id"] for t in account.transactions]
        unique_ids = set(transaction_ids)

        self.assertEqual(len(transaction_ids), len(unique_ids))

    def test_account_creation_date(self):
        """Тест даты создания счета"""
        account = BankAccount("DATE_TEST", "Тестовый счет", 5000.0)

        # Дата создания должна быть недавней
        time_diff = abs((datetime.now() - account.created_date).total_seconds())
        self.assertLess(time_diff, 60)

    def test_credit_card_interest_rate(self):
        """Тест процентной ставки кредитной карты"""
        expiry_date = datetime.now() + timedelta(days=365)
        card = CreditCard("1234567890123456", "Тестовый держатель", expiry_date, "123")

        # Процентная ставка должна быть в разумных пределах
        self.assertGreaterEqual(card.interest_rate, 12)
        self.assertLessEqual(card.interest_rate, 24)

    def test_credit_card_payment_due_date(self):
        """Тест даты платежа по кредитной карте"""
        expiry_date = datetime.now() + timedelta(days=365)
        card = CreditCard("1234567890123456", "Тестовый держатель", expiry_date, "123")

        # Дата платежа должна быть через 30 дней
        expected_due_date = datetime.now() + timedelta(days=30)
        time_diff = abs((card.payment_due_date - expected_due_date).total_seconds())
        self.assertLess(time_diff, 3600)  # В пределах часа

    def test_bank_account_currency(self):
        """Тест валюты банковского счета"""
        account = BankAccount("CURR_TEST", "Валютный тест", 1000.0)

        # По умолчанию должна быть RUB
        self.assertEqual(account.currency, "RUB")

        # Можно изменить валюту
        account.currency = "USD"
        self.assertEqual(account.currency, "USD")


class TestExceptionDetails(unittest.TestCase):
    """Тесты деталей исключений"""

    def test_exception_string_representations(self):
        """Тест строковых представлений исключений"""
        exceptions = [
            AnimalNotFoundException("ANIMAL001"),
            InsufficientFundsException(1000.0, 500.0),
            InvalidPasswordException("test_user"),
            TankOverflowException("TANK001", 1000.0, 1200.0),
            EquipmentMalfunctionException("Pump", "ERR123"),
            UnauthorizedAccessException("user", "admin"),
            FeedingScheduleConflictException("ANIMAL001", datetime.now()),
            InvalidTemperatureException(35.0, 20.0, 30.0),
            TicketExpiredException("TICKET001", datetime.now()),
            MaintenanceModeException("Hall", datetime.now()),
            AnimalHealthException("ANIMAL001", "Infection")
        ]

        for exception in exceptions:
            # Все исключения должны иметь не пустое строковое представление
            self.assertGreater(len(str(exception)), 0)
            self.assertIsInstance(str(exception), str)

    def test_exception_attributes_access(self):
        """Тест доступа к атрибутам исключений"""
        # Тестируем доступ к специфичным атрибутам
        animal_ex = AnimalNotFoundException("TEST_ANIMAL")
        self.assertEqual(animal_ex.animal_id, "TEST_ANIMAL")

        funds_ex = InsufficientFundsException(1000.0, 500.0)
        self.assertEqual(funds_ex.required_amount, 1000.0)
        self.assertEqual(funds_ex.available_amount, 500.0)

        temp_ex = InvalidTemperatureException(35.0, 20.0, 30.0)
        self.assertEqual(temp_ex.current_temp, 35.0)
        self.assertEqual(temp_ex.min_temp, 20.0)
        self.assertEqual(temp_ex.max_temp, 30.0)


if __name__ == '__main__':
    unittest.main()
