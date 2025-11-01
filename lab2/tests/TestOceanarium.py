"""
Тесты для модуля oceanarium.py
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.oceanarium import (
    Oceanarium, AquariumShow, ConservationProgram, WaterTreatmentSystem,
    BreedingProgram, VisitorCenter, ResearchLaboratory, AnimalHospital,
    UnderwaterTunnel, MarineEcosystem, EducationalCenter, AquacultureFacility,
    MarineConservation, OceanographicResearch
)
from oceanarium.exceptions import AnimalHealthException


class TestNewClasses(unittest.TestCase):
    """Тесты для новых классов Oceanarium"""

    def test_aquarium_show_initialization(self):
        """Тест инициализации шоу"""
        show = AquariumShow("show_001", "Дельфинье шоу", 45)
        
        self.assertEqual(show.show_id, "show_001")
        self.assertEqual(show.name, "Дельфинье шоу")
        self.assertEqual(show.duration, 45)
        self.assertEqual(show.schedule, [])
        self.assertEqual(show.animals_involved, [])
        self.assertEqual(show.trainers_required, [])
        self.assertEqual(show.equipment_needed, [])

    def test_conservation_program_initialization(self):
        """Тест инициализации программы сохранения"""
        program = ConservationProgram("cons_001", "Дельфины", "Защита популяции")
        
        self.assertEqual(program.program_id, "cons_001")
        self.assertEqual(program.species, "Дельфины")
        self.assertEqual(program.goal, "Защита популяции")
        self.assertEqual(program.budget, 0.0)
        self.assertEqual(program.researchers, [])
        self.assertEqual(program.success_rate, 0.0)

    def test_water_treatment_system_initialization(self):
        """Тест инициализации системы очистки воды"""
        system = WaterTreatmentSystem("water_001", 1000.0)
        
        self.assertEqual(system.system_id, "water_001")
        self.assertEqual(system.capacity, 1000.0)
        self.assertEqual(system.filtration_level, 95.0)
        self.assertEqual(system.chemical_balance, {})
        self.assertEqual(system.maintenance_schedule, [])

    def test_breeding_program_initialization(self):
        """Тест инициализации программы разведения"""
        program = BreedingProgram("breed_001", "Акулы")
        
        self.assertEqual(program.program_id, "breed_001")
        self.assertEqual(program.target_species, "Акулы")
        self.assertEqual(program.breeding_pairs, [])
        self.assertEqual(program.successful_births, 0)
        self.assertEqual(program.genetic_diversity, 85.0)

    def test_visitor_center_initialization(self):
        """Тест инициализации центра для посетителей"""
        center = VisitorCenter("center_001", 200)
        
        self.assertEqual(center.center_id, "center_001")
        self.assertEqual(center.capacity, 200)
        self.assertEqual(center.facilities, [])
        self.assertEqual(center.daily_visitors, 0)
        self.assertEqual(center.guided_tours, [])

    def test_research_laboratory_initialization(self):
        """Тест инициализации исследовательской лаборатории"""
        lab = ResearchLaboratory("lab_001", "Морская биология")
        
        self.assertEqual(lab.lab_id, "lab_001")
        self.assertEqual(lab.specialization, "Морская биология")
        self.assertEqual(lab.equipment, [])
        self.assertEqual(lab.research_projects, [])
        self.assertEqual(lab.publications, [])

    def test_animal_hospital_initialization(self):
        """Тест инициализации ветеринарной больницы"""
        hospital = AnimalHospital("hospital_001", 10)
        
        self.assertEqual(hospital.hospital_id, "hospital_001")
        self.assertEqual(hospital.capacity, 10)
        self.assertEqual(hospital.quarantine_units, [])
        self.assertEqual(hospital.surgical_rooms, [])
        self.assertEqual(hospital.patients, [])

    def test_underwater_tunnel_initialization(self):
        """Тест инициализации подводного туннеля"""
        tunnel = UnderwaterTunnel("tunnel_001", 50.5)
        
        self.assertEqual(tunnel.tunnel_id, "tunnel_001")
        self.assertEqual(tunnel.length, 50.5)
        self.assertEqual(tunnel.viewing_windows, [])
        self.assertEqual(tunnel.cleaning_schedule, [])
        self.assertEqual(tunnel.visitor_capacity, 50)

    def test_marine_ecosystem_initialization(self):
        """Тест инициализации морской экосистемы"""
        ecosystem = MarineEcosystem("eco_001", "Коралловый риф")
        
        self.assertEqual(ecosystem.ecosystem_id, "eco_001")
        self.assertEqual(ecosystem.biome_type, "Коралловый риф")
        self.assertEqual(ecosystem.species_diversity, [])
        self.assertEqual(ecosystem.environmental_params, {})
        self.assertEqual(ecosystem.conservation_status, "stable")

    def test_educational_center_initialization(self):
        """Тест инициализации образовательного центра"""
        center = EducationalCenter("edu_001", 5)
        
        self.assertEqual(center.center_id, "edu_001")
        self.assertEqual(center.classrooms, 5)
        self.assertEqual(center.workshops, [])
        self.assertEqual(center.student_groups, [])
        self.assertEqual(center.educational_materials, [])

    def test_aquaculture_facility_initialization(self):
        """Тест инициализации аквакультурного предприятия"""
        facility = AquacultureFacility("aqua_001", "Рыбоводство")
        
        self.assertEqual(facility.facility_id, "aqua_001")
        self.assertEqual(facility.production_type, "Рыбоводство")
        self.assertEqual(facility.production_capacity, 0.0)
        self.assertEqual(facility.species_cultured, [])
        self.assertEqual(facility.harvest_schedule, [])

    def test_marine_conservation_initialization(self):
        """Тест инициализации отдела консервации"""
        conservation = MarineConservation("dept_001", ["Защита видов", "Исследования"])
        
        self.assertEqual(conservation.department_id, "dept_001")
        self.assertEqual(conservation.focus_areas, ["Защита видов", "Исследования"])
        self.assertEqual(conservation.conservation_projects, [])
        self.assertEqual(conservation.research_grants, [])
        self.assertEqual(conservation.community_outreach, [])

    def test_oceanographic_research_initialization(self):
        """Тест инициализации океанографических исследований"""
        research = OceanographicResearch("research_001", "Тихий океан")
        
        self.assertEqual(research.research_id, "research_001")
        self.assertEqual(research.ocean_region, "Тихий океан")
        self.assertEqual(research.research_vessels, [])
        self.assertEqual(research.data_collection, [])
        self.assertEqual(research.scientific_discoveries, [])


class TestOceanariumExtended(unittest.TestCase):
    """Расширенные тесты основного класса Oceanarium"""

    def setUp(self):
        self.oceanarium = Oceanarium("Тестовый океанариум", "Москва", 1000)

    def test_oceanarium_initial_state(self):
        """Тест начального состояния океанариума"""
        self.assertEqual(self.oceanarium.name, "Тестовый океанариум")
        self.assertEqual(self.oceanarium.location, "Москва")
        self.assertEqual(self.oceanarium.capacity, 1000)
        self.assertEqual(self.oceanarium.operational_status, "open")
        self.assertEqual(self.oceanarium.daily_visitors, 0)

    def test_add_animal_success(self):
        """Тест успешного добавления животного"""
        mock_animal = Mock()
        mock_animal.animal_id = "animal_001"
        
        mock_tank = Mock()
        mock_tank.tank_id = "tank_001"
        mock_tank.add_animal.return_value = True
        
        self.oceanarium.tanks["tank_001"] = mock_tank
        
        result = self.oceanarium.add_animal(mock_animal, "tank_001")
        
        self.assertTrue(result)
        self.assertIn("animal_001", self.oceanarium.animals)
        mock_tank.add_animal.assert_called_once_with(mock_animal)

    def test_add_animal_tank_not_found(self):
        """Тест добавления животного в несуществующий резервуар"""
        mock_animal = Mock()
        mock_animal.animal_id = "animal_001"
        
        with self.assertRaises(ValueError):
            self.oceanarium.add_animal(mock_animal, "nonexistent_tank")

    def test_hire_staff(self):
        """Тест найма сотрудника"""
        mock_staff = Mock()
        mock_staff.staff_id = "staff_001"
        mock_staff.name = "Иван Иванов"
        mock_staff.access_level = 2
        
        # Мокаем метод issue_keycard
        with patch.object(self.oceanarium.security_system, 'issue_keycard') as mock_issue:
            self.oceanarium.hire_staff(mock_staff)
            
            self.assertIn("staff_001", self.oceanarium.staff)
            # Проверяем что вызвали метод выдачи карты доступа
            mock_issue.assert_called_once_with(
                mock_staff.staff_id,
                mock_staff.name,
                mock_staff.access_level
            )

    def test_add_visitor(self):
        """Тест добавления посетителя"""
        mock_visitor = Mock()
        mock_visitor.visitor_id = "visitor_001"
        
        self.oceanarium.add_visitor(mock_visitor)
        
        self.assertIn("visitor_001", self.oceanarium.visitors)
        self.assertEqual(self.oceanarium.daily_visitors, 1)

    def test_create_ticket_office(self):
        """Тест создания кассы"""
        office = self.oceanarium.create_ticket_office("office_001", "Кассир")
        
        self.assertEqual(office.office_id, "office_001")
        self.assertEqual(len(self.oceanarium.ticket_offices), 1)

    def test_feed_all_animals_with_feeder(self):
        """Тест кормления животных с доступным кормильцем"""
        mock_animal = Mock()
        mock_animal.animal_id = "animal_001"
        mock_animal.get_feeding_requirements.return_value = {"рыба": 5.0}
        
        # Создаем настоящий экземпляр Feeder вместо Mock
        from oceanarium.core import Feeder
        mock_feeder = Mock(spec=Feeder)
        mock_feeder.feed_animal.return_value = True
        mock_feeder.staff_id = "feeder_001"
        
        self.oceanarium.animals["animal_001"] = mock_animal
        self.oceanarium.staff["feeder_001"] = mock_feeder
        
        results = self.oceanarium.feed_all_animals()
        
        self.assertTrue(results["animal_001"])
        mock_feeder.feed_animal.assert_called_once()

    def test_feed_all_animals_no_feeder(self):
        """Тест кормления животных без кормильца"""
        mock_animal = Mock()
        mock_animal.animal_id = "animal_001"
        
        self.oceanarium.animals["animal_001"] = mock_animal
        
        results = self.oceanarium.feed_all_animals()
        
        self.assertFalse(results["animal_001"])

    def test_conduct_health_checks_with_vet(self):
        """Тест медицинских осмотров с ветеринаром"""
        mock_animal = Mock()
        mock_animal.animal_id = "animal_001"
        
        # Создаем настоящий экземпляр Veterinarian вместо Mock
        from oceanarium.core import Veterinarian
        mock_vet = Mock(spec=Veterinarian)
        mock_vet.examine_animal.return_value = {"status": "healthy"}
        mock_vet.staff_id = "vet_001"
        
        self.oceanarium.animals["animal_001"] = mock_animal
        self.oceanarium.staff["vet_001"] = mock_vet
        
        results = self.oceanarium.conduct_health_checks()
        
        self.assertIn("animal_001", results)
        mock_vet.examine_animal.assert_called_once_with(mock_animal)

    def test_conduct_health_checks_no_vet(self):
        """Тест медицинских осмотров без ветеринара"""
        mock_animal = Mock()
        mock_animal.animal_id = "animal_001"
        
        self.oceanarium.animals["animal_001"] = mock_animal
        
        with self.assertRaises(AnimalHealthException):
            self.oceanarium.conduct_health_checks()

    def test_monitor_water_quality(self):
        """Тест мониторинга качества воды"""
        mock_tank = Mock()
        mock_tank.tank_id = "tank_001"
        mock_tank.check_water_quality.return_value = {
            "temperature": True, "ph": False, "salinity": True
        }
        
        self.oceanarium.tanks["tank_001"] = mock_tank
        
        results = self.oceanarium.monitor_water_quality()
        
        self.assertIn("tank_001", results)
        mock_tank.check_water_quality.assert_called_once()

    def test_generate_daily_report(self):
        """Тест генерации ежедневного отчета"""
        # Настраиваем минимальные данные для отчета
        mock_tank = Mock()
        mock_tank.tank_id = "tank_001"
        mock_tank.animals = [Mock()]
        mock_tank.check_water_quality.return_value = {"temp": True}
        mock_tank.last_cleaned = datetime.now()
        
        self.oceanarium.tanks["tank_001"] = mock_tank
        self.oceanarium.animals = {"animal1": Mock(), "animal2": Mock()}
        self.oceanarium.daily_visitors = 100
        
        report = self.oceanarium.generate_daily_report()
        
        self.assertEqual(report["visitor_count"], 100)
        self.assertEqual(report["animal_count"], 2)
        self.assertIn("tank_001", report["tank_status"])

    def test_close_and_open_for_day(self):
        """Тест закрытия и открытия на день"""
        # Создаем мок кассы
        mock_office = Mock()
        mock_office.daily_sales = []
        mock_office.end_shift.return_value = {"total_sales": 0.0}
        self.oceanarium.ticket_offices = [mock_office]
        
        # Закрываем
        closing_report = self.oceanarium.close_for_day()
        self.assertEqual(self.oceanarium.operational_status, "closed")
        self.assertEqual(self.oceanarium.daily_visitors, 0)
        
        # Открываем
        self.oceanarium.open_for_day()
        self.assertEqual(self.oceanarium.operational_status, "open")

    def test_get_occupancy_rate(self):
        """Тест расчета заполненности"""
        rate = self.oceanarium.get_occupancy_rate()
        self.assertEqual(rate, 0.0)  # Пустой океанариум

    def test_transfer_animal_success(self):
        """Тест успешного перемещения животного"""
        mock_animal = Mock()
        mock_animal.animal_id = "animal_001"
        
        mock_tank1 = Mock()
        mock_tank1.tank_id = "tank_001"
        mock_tank1.remove_animal.return_value = True
        
        mock_tank2 = Mock()
        mock_tank2.tank_id = "tank_002"
        mock_tank2.add_animal.return_value = True
        
        self.oceanarium.animals["animal_001"] = mock_animal
        self.oceanarium.tanks["tank_001"] = mock_tank1
        self.oceanarium.tanks["tank_002"] = mock_tank2
        
        result = self.oceanarium.transfer_animal("animal_001", "tank_001", "tank_002")
        
        self.assertTrue(result)
        mock_tank1.remove_animal.assert_called_once_with("animal_001")
        mock_tank2.add_animal.assert_called_once_with(mock_animal)

    def test_calculate_monthly_expenses(self):
        """Тест расчета месячных расходов"""
        # Добавляем тестовых сотрудников
        mock_staff1 = Mock()
        mock_staff1.calculate_monthly_salary.return_value = 50000.0
        mock_staff2 = Mock()
        mock_staff2.calculate_monthly_salary.return_value = 75000.0
        
        self.oceanarium.staff = {
            "staff1": mock_staff1,
            "staff2": mock_staff2
        }
        self.oceanarium.animals = {
            "animal1": Mock(),
            "animal2": Mock(),
            "animal3": Mock()
        }
        self.oceanarium.equipment = {
            "equip1": Mock(),
            "equip2": Mock()
        }
        
        expenses = self.oceanarium.calculate_monthly_expenses()
        
        expected_categories = [
            "staff_salaries", "food_costs", "utilities",
            "maintenance", "insurance"
        ]
        
        for category in expected_categories:
            self.assertIn(category, expenses)
            self.assertIsInstance(expenses[category], (int, float))

    def test_get_animal_statistics(self):
        """Тест получения статистики по животным"""
        # Добавляем тестовых животных
        mock_animal1 = Mock()
        mock_animal1.species = "Дельфин"
        mock_animal1.check_health.return_value = "healthy"
        mock_animal1.last_feeding = datetime.now() - timedelta(hours=2)
        mock_animal1.tank_id = "tank_001"
        
        mock_animal2 = Mock()
        mock_animal2.species = "Акула"
        mock_animal2.check_health.return_value = "sick"
        mock_animal2.last_feeding = datetime.now() - timedelta(hours=8)
        mock_animal2.tank_id = "tank_002"
        
        self.oceanarium.animals = {
            "animal1": mock_animal1,
            "animal2": mock_animal2
        }
        
        stats = self.oceanarium.get_animal_statistics()
        
        self.assertEqual(stats["total_animals"], 2)
        self.assertIn("species_count", stats)
        self.assertIn("health_distribution", stats)
        self.assertIn("feeding_status", stats)
        self.assertIn("tank_distribution", stats)


class TestOceanariumEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def setUp(self):
        self.oceanarium = Oceanarium("Тестовый", "Город", 1000)

    def test_empty_collections(self):
        """Тест работы с пустыми коллекциями"""
        # Все методы должны корректно работать с пустыми данными
        self.assertEqual(len(self.oceanarium.animals), 0)
        self.assertEqual(len(self.oceanarium.tanks), 0)
        self.assertEqual(len(self.oceanarium.staff), 0)
        self.assertEqual(len(self.oceanarium.visitors), 0)

    def test_methods_with_empty_data(self):
        """Тест методов с пустыми данными"""
        # Эти методы не должны падать с пустыми данными
        feeding_results = self.oceanarium.feed_all_animals()
        self.assertEqual(feeding_results, {})
        
        water_quality = self.oceanarium.monitor_water_quality()
        self.assertEqual(water_quality, {})
        
        daily_report = self.oceanarium.generate_daily_report()
        self.assertIsInstance(daily_report, dict)
        
        animal_stats = self.oceanarium.get_animal_statistics()
        self.assertEqual(animal_stats["total_animals"], 0)

    def test_invalid_operations(self):
        """Тест некорректных операций"""
        # Перемещение несуществующего животного
        result = self.oceanarium.transfer_animal("none", "tank1", "tank2")
        self.assertFalse(result)
        
        # Тренировка несуществующего животного/тренера
        result = self.oceanarium.conduct_training_session("none", "none", "skill")
        self.assertFalse(result)
        
        # Обслуживание несуществующего оборудования
        result = self.oceanarium.schedule_maintenance("none", "repair")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
