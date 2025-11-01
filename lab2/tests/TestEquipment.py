"""
Юнит тесты для модуля equipment.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.equipment import (
    Equipment, WaterPump, FilterSystem, TemperatureController,
    Tank, MonitoringSystem, SecuritySystem
)
from oceanarium.core import MarineAnimal
from oceanarium.exceptions import *


class TestEquipment(unittest.TestCase):
    """Тесты для абстрактного класса Equipment"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем тестовый класс-наследник
        class TestEquipmentImpl(Equipment):
            def perform_maintenance(self):
                self.last_maintenance = datetime.now()
                self.status = "operational"
                return True

        self.equipment = TestEquipmentImpl("EQ001", "Тестовое оборудование", "TestCorp")

    def test_equipment_initialization(self):
        """Тест инициализации оборудования"""
        self.assertEqual(self.equipment.equipment_id, "EQ001")
        self.assertEqual(self.equipment.name, "Тестовое оборудование")
        self.assertEqual(self.equipment.manufacturer, "TestCorp")
        self.assertEqual(self.equipment.status, "operational")
        self.assertIsNone(self.equipment.last_maintenance)
        self.assertEqual(self.equipment.maintenance_interval_days, 30)


    @patch('random.random')
    def test_check_status_malfunction(self, mock_random):
        """Тест проверки статуса - поломка"""
        mock_random.return_value = 0.005  # Меньше 0.01 для срабатывания поломки
        status = self.equipment.check_status()
        self.assertEqual(status, "malfunction")
        self.assertGreater(len(self.equipment.error_codes), 0)

    def test_reset_error_success(self):
        """Тест успешного сброса ошибки"""
        self.equipment.error_codes = ["ERR_1234"]
        self.equipment.status = "malfunction"
        result = self.equipment.reset_error("ERR_1234")
        self.assertTrue(result)
        self.assertNotIn("ERR_1234", self.equipment.error_codes)
        self.assertEqual(self.equipment.status, "operational")

    def test_reset_error_not_found(self):
        """Тест сброса несуществующей ошибки"""
        result = self.equipment.reset_error("ERR_9999")
        self.assertFalse(result)


class TestWaterPump(unittest.TestCase):
    """Тесты для класса WaterPump"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.pump = WaterPump("PUMP001", "Основной насос", "AquaTech", 500.0)

    def test_pump_initialization(self):
        """Тест инициализации насоса"""
        self.assertEqual(self.pump.flow_rate, 500.0)
        self.assertGreaterEqual(self.pump.pressure, 1.0)
        self.assertLessEqual(self.pump.pressure, 5.0)
        self.assertIn(self.pump.pump_type, ["centrifugal", "submersible", "magnetic_drive"])
        self.assertEqual(self.pump.maintenance_interval_days, 60)

    def test_perform_maintenance(self):
        """Тест технического обслуживания"""
        self.pump.error_codes = ["ERR_1234"]
        self.pump.status = "malfunction"
        result = self.pump.perform_maintenance()
        self.assertTrue(result)
        self.assertEqual(self.pump.status, "operational")
        self.assertEqual(len(self.pump.error_codes), 0)
        self.assertIsNotNone(self.pump.last_maintenance)

    def test_adjust_flow_rate_success(self):
        """Тест успешной регулировки потока"""
        result = self.pump.adjust_flow_rate(400.0)
        self.assertTrue(result)
        self.assertEqual(self.pump.flow_rate, 400.0)

    def test_adjust_flow_rate_exceed_limit(self):
        """Тест превышения лимита потока"""
        result = self.pump.adjust_flow_rate(700.0)  # Больше 500 * 1.2
        self.assertFalse(result)
        self.assertEqual(self.pump.flow_rate, 500.0)  # Не изменился

    def test_check_cavitation_low_pressure(self):
        """Тест кавитации при низком давлении"""
        self.pump.pressure = 0.3
        result = self.pump.check_cavitation()
        self.assertTrue(result)

    def test_check_cavitation_high_speed(self):
        """Тест кавитации при высокой скорости"""
        self.pump.impeller_speed = 2900
        result = self.pump.check_cavitation()
        self.assertTrue(result)


class TestFilterSystem(unittest.TestCase):
    """Тесты для класса FilterSystem"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.filter = FilterSystem("FILTER001", "Биофильтр", "AquaClean", 1000.0)

    def test_filter_initialization(self):
        """Тест инициализации фильтра"""
        self.assertEqual(self.filter.filter_capacity, 1000.0)
        self.assertIn(self.filter.filter_type, ["mechanical", "biological", "chemical", "UV"])
        self.assertGreaterEqual(self.filter.efficiency, 85)
        self.assertLessEqual(self.filter.efficiency, 99)
        self.assertEqual(self.filter.filter_media_age, 0)
        self.assertEqual(self.filter.maintenance_interval_days, 14)

    def test_perform_maintenance(self):
        """Тест технического обслуживания фильтра"""
        self.filter.filter_media_age = 10
        self.filter.efficiency = 80
        result = self.filter.perform_maintenance()
        self.assertTrue(result)
        self.assertEqual(self.filter.filter_media_age, 0)
        self.assertGreaterEqual(self.filter.efficiency, 85)

    def test_backwash_mechanical_filter(self):
        """Тест обратной промывки механического фильтра"""
        self.filter.filter_type = "mechanical"
        initial_efficiency = self.filter.efficiency
        result = self.filter.backwash()
        self.assertTrue(result)
        self.assertGreaterEqual(self.filter.efficiency, initial_efficiency)

    def test_backwash_uv_filter(self):
        """Тест обратной промывки UV фильтра (не поддерживается)"""
        self.filter.filter_type = "UV"
        result = self.filter.backwash()
        self.assertFalse(result)

    def test_replace_filter_media(self):
        """Тест замены фильтрующего материала"""
        self.filter.filter_media_age = 30
        result = self.filter.replace_filter_media()
        self.assertTrue(result)
        self.assertEqual(self.filter.filter_media_age, 0)
        self.assertGreaterEqual(self.filter.efficiency, 90)


class TestTemperatureController(unittest.TestCase):
    """Тесты для класса TemperatureController"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.controller = TemperatureController("TEMP001", "Термостат", "TempControl", 2000.0)

    def test_controller_initialization(self):
        """Тест инициализации контроллера температуры"""
        self.assertEqual(self.controller.target_temperature, 24.0)
        self.assertEqual(self.controller.heating_power, 2000.0)
        self.assertEqual(self.controller.cooling_power, 1600.0)  # 80% от heating_power
        self.assertEqual(self.controller.temperature_tolerance, 0.5)
        self.assertEqual(self.controller.maintenance_interval_days, 90)

    def test_set_temperature_valid(self):
        """Тест установки допустимой температуры"""
        result = self.controller.set_temperature(22.0)
        self.assertTrue(result)
        self.assertEqual(self.controller.target_temperature, 22.0)

    def test_set_temperature_invalid_low(self):
        """Тест установки слишком низкой температуры"""
        with self.assertRaises(InvalidTemperatureException):
            self.controller.set_temperature(10.0)

    def test_set_temperature_invalid_high(self):
        """Тест установки слишком высокой температуры"""
        with self.assertRaises(InvalidTemperatureException):
            self.controller.set_temperature(35.0)

    def test_regulate_temperature_heating(self):
        """Тест регулировки температуры (нагрев)"""
        self.controller.current_temperature = 20.0
        self.controller.target_temperature = 24.0
        new_temp = self.controller.regulate_temperature()
        self.assertGreater(new_temp, 20.0)
        self.assertLessEqual(new_temp, 20.5)  # Максимальный шаг нагрева

    def test_regulate_temperature_cooling(self):
        """Тест регулировки температуры (охлаждение)"""
        self.controller.current_temperature = 26.0
        self.controller.target_temperature = 24.0
        new_temp = self.controller.regulate_temperature()
        self.assertLess(new_temp, 26.0)
        self.assertGreaterEqual(new_temp, 25.7)  # Максимальный шаг охлаждения

    def test_regulate_temperature_within_tolerance(self):
        """Тест регулировки при температуре в пределах допуска"""
        self.controller.current_temperature = 24.2
        self.controller.target_temperature = 24.0
        initial_temp = self.controller.current_temperature
        new_temp = self.controller.regulate_temperature()
        self.assertEqual(new_temp, initial_temp)  # Не должна измениться


class TestTank(unittest.TestCase):
    """Тесты для класса Tank"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.tank = Tank("TANK001", 50000.0, "display")
        self.marine_animal = MarineAnimal("ANIMAL001", "Тестовая рыба", "Test fish", 2, 50.0, 90.0, 10)

    def test_tank_initialization(self):
        """Тест инициализации резервуара"""
        self.assertEqual(self.tank.tank_id, "TANK001")
        self.assertEqual(self.tank.capacity, 50000.0)
        self.assertEqual(self.tank.current_volume, 45000.0)  # 90% от capacity
        self.assertEqual(self.tank.tank_type, "display")
        self.assertEqual(len(self.tank.animals), 0)
        self.assertEqual(len(self.tank.equipment), 0)

    def test_get_max_animals(self):
        """Тест расчета максимального количества животных"""
        max_animals = self.tank.get_max_animals()
        expected = max(1, int(50000 / 10000))  # 1 животное на 10000л
        self.assertEqual(max_animals, expected)

    def test_add_animal_success(self):
        """Тест успешного добавления животного"""
        result = self.tank.add_animal(self.marine_animal)
        self.assertTrue(result)
        self.assertEqual(len(self.tank.animals), 1)
        self.assertEqual(self.marine_animal.tank_id, "TANK001")

    def test_add_animal_exceeds_capacity(self):
        """Тест добавления животного при превышении вместимости"""
        # Заполняем резервуар до максимума
        max_animals = self.tank.get_max_animals()
        for i in range(max_animals):
            animal = MarineAnimal(f"ANIMAL{i:03d}", f"Рыба {i}", "Test fish", 2, 50.0, 90.0, 10)
            self.tank.add_animal(animal)

        # Пытаемся добавить еще одно
        extra_animal = MarineAnimal("EXTRA001", "Лишняя рыба", "Test fish", 2, 50.0, 90.0, 10)
        result = self.tank.add_animal(extra_animal)
        self.assertFalse(result)

    def test_remove_animal_success(self):
        """Тест успешного удаления животного"""
        self.tank.add_animal(self.marine_animal)
        result = self.tank.remove_animal("ANIMAL001")
        self.assertTrue(result)
        self.assertEqual(len(self.tank.animals), 0)
        self.assertIsNone(self.marine_animal.tank_id)

    def test_remove_animal_not_found(self):
        """Тест удаления несуществующего животного"""
        with self.assertRaises(AnimalNotFoundException):
            self.tank.remove_animal("NONEXISTENT")

    def test_check_water_quality(self):
        """Тест проверки качества воды"""
        quality = self.tank.check_water_quality()
        self.assertIsInstance(quality, dict)
        expected_keys = ["temperature", "salinity", "ph", "ammonia", "nitrite", "nitrate"]
        for key in expected_keys:
            self.assertIn(key, quality)
            self.assertIsInstance(quality[key], bool)

    def test_clean_tank(self):
        """Тест очистки резервуара"""
        # Устанавливаем плохие параметры воды
        self.tank.water_parameters["ammonia"] = 1.0
        self.tank.water_parameters["nitrite"] = 1.0
        self.tank.water_parameters["nitrate"] = 30.0

        result = self.tank.clean_tank()
        self.assertTrue(result)

        # Проверяем улучшение параметров
        self.assertLess(self.tank.water_parameters["ammonia"], 1.0)
        self.assertLess(self.tank.water_parameters["nitrite"], 1.0)
        self.assertLess(self.tank.water_parameters["nitrate"], 30.0)


class TestMonitoringSystem(unittest.TestCase):
    """Тесты для класса MonitoringSystem"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.monitoring = MonitoringSystem("MON001")

    def test_monitoring_initialization(self):
        """Тест инициализации системы мониторинга"""
        self.assertEqual(self.monitoring.system_id, "MON001")
        self.assertEqual(len(self.monitoring.sensors), 0)
        self.assertEqual(len(self.monitoring.alerts), 0)
        self.assertEqual(len(self.monitoring.data_logs), 0)
        self.assertEqual(self.monitoring.monitoring_frequency, 60)

    def test_add_sensor(self):
        """Тест добавления датчика"""
        sensor_id = self.monitoring.add_sensor("temperature", "tank_center", "TANK001")
        self.assertIsNotNone(sensor_id)
        self.assertEqual(len(self.monitoring.sensors), 1)

        sensor = self.monitoring.sensors[0]
        self.assertEqual(sensor["type"], "temperature")
        self.assertEqual(sensor["location"], "tank_center")
        self.assertEqual(sensor["tank_id"], "TANK001")
        self.assertEqual(sensor["status"], "active")

    @patch('random.uniform')
    def test_read_sensor_data_temperature(self, mock_uniform):
        """Тест чтения данных с датчика температуры"""
        mock_uniform.return_value = 24.5
        sensor_id = self.monitoring.add_sensor("temperature", "tank_center", "TANK001")

        value = self.monitoring.read_sensor_data(sensor_id)
        self.assertEqual(value, 24.5)
        self.assertEqual(len(self.monitoring.data_logs), 1)

    def test_read_sensor_data_nonexistent(self):
        """Тест чтения данных с несуществующего датчика"""
        value = self.monitoring.read_sensor_data("NONEXISTENT")
        self.assertIsNone(value)

    @patch('random.uniform')
    def test_check_alert_thresholds_high_temperature(self, mock_uniform):
        """Тест срабатывания предупреждения при высокой температуре"""
        mock_uniform.return_value = 30.0  # Выше максимума (28)
        sensor_id = self.monitoring.add_sensor("temperature", "tank_center", "TANK001")

        self.monitoring.read_sensor_data(sensor_id)
        self.assertGreater(len(self.monitoring.alerts), 0)

        alert = self.monitoring.alerts[0]
        self.assertEqual(alert["severity"], "high")
        self.assertEqual(alert["parameter"], "temperature")

    def test_acknowledge_alert(self):
        """Тест подтверждения предупреждения"""
        # Создаем предупреждение
        self.monitoring.create_alert("SENS_001", "temperature", 30.0, "high")
        alert_id = self.monitoring.alerts[0]["alert_id"]

        result = self.monitoring.acknowledge_alert(alert_id)
        self.assertTrue(result)
        self.assertTrue(self.monitoring.alerts[0]["acknowledged"])


class TestSecuritySystem(unittest.TestCase):
    """Тесты для класса SecuritySystem"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.security = SecuritySystem("SEC001")

    def test_security_initialization(self):
        """Тест инициализации системы безопасности"""
        self.assertEqual(self.security.system_id, "SEC001")
        self.assertEqual(len(self.security.access_zones), 0)
        self.assertEqual(len(self.security.key_cards), 0)
        self.assertEqual(len(self.security.security_logs), 0)
        self.assertFalse(self.security.emergency_mode)

    def test_create_access_zone(self):
        """Тест создания зоны доступа"""
        self.security.create_access_zone("ZONE001", "Служебная зона", 3)
        self.assertIn("ZONE001", self.security.access_zones)

        zone = self.security.access_zones["ZONE001"]
        self.assertEqual(zone["name"], "Служебная зона")
        self.assertEqual(zone["required_level"], 3)
        self.assertEqual(len(zone["current_occupants"]), 0)

    def test_issue_keycard(self):
        """Тест выдачи карты доступа"""
        card_id = self.security.issue_keycard("USER001", "Иван Иванов", 5)
        self.assertIsNotNone(card_id)
        self.assertEqual(len(self.security.key_cards), 1)

        keycard = self.security.key_cards[0]
        self.assertEqual(keycard["user_id"], "USER001")
        self.assertEqual(keycard["user_name"], "Иван Иванов")
        self.assertEqual(keycard["access_level"], 5)
        self.assertTrue(keycard["active"])

    def test_check_access_success(self):
        """Тест успешной проверки доступа"""
        # Создаем зону и карту
        self.security.create_access_zone("ZONE001", "Служебная зона", 3)
        card_id = self.security.issue_keycard("USER001", "Иван Иванов", 5)

        result = self.security.check_access(card_id, "ZONE001")
        self.assertTrue(result)
        self.assertIn("USER001", self.security.access_zones["ZONE001"]["current_occupants"])

    def test_check_access_insufficient_level(self):
        """Тест отказа доступа из-за недостаточного уровня"""
        self.security.create_access_zone("ZONE001", "Высокоуровневая зона", 8)
        card_id = self.security.issue_keycard("USER001", "Иван Иванов", 3)

        with self.assertRaises(UnauthorizedAccessException):
            self.security.check_access(card_id, "ZONE001")

    def test_check_access_inactive_card(self):
        """Тест отказа доступа с неактивной картой"""
        self.security.create_access_zone("ZONE001", "Служебная зона", 3)
        card_id = self.security.issue_keycard("USER001", "Иван Иванов", 5)

        # Деактивируем карту
        self.security.key_cards[0]["active"] = False

        result = self.security.check_access(card_id, "ZONE001")
        self.assertFalse(result)

    def test_activate_emergency_mode(self):
        """Тест активации режима чрезвычайной ситуации"""
        self.security.create_access_zone("ZONE001", "Служебная зона", 3)

        self.security.activate_emergency_mode()
        self.assertTrue(self.security.emergency_mode)
        self.assertTrue(self.security.access_zones["ZONE001"]["emergency_lockdown"])
        self.assertGreater(len(self.security.security_logs), 0)

    def test_log_security_event(self):
        """Тест записи события безопасности"""
        self.security.log_security_event("test_event", "Тестовое событие", "ZONE001")
        self.assertEqual(len(self.security.security_logs), 1)

        log_entry = self.security.security_logs[0]
        self.assertEqual(log_entry["event_type"], "test_event")
        self.assertEqual(log_entry["description"], "Тестовое событие")
        self.assertEqual(log_entry["zone_id"], "ZONE001")


if __name__ == '__main__':
    unittest.main()
