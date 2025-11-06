"""
Тесты для модуля oceanarium.py с покрытием более 85%
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
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
from oceanarium.exceptions import AnimalHealthException, TankOverflowException
from oceanarium.core import Animal, Staff, Trainer, Veterinarian, Feeder
from oceanarium.equipment import Tank, Equipment
from oceanarium.finance import Visitor, TicketOffice
from oceanarium.management import ResearchScientist, TourGuide


class TestAquariumShow(unittest.TestCase):
    """Тесты для класса AquariumShow"""
    
    def setUp(self):
        self.show = AquariumShow("show_001", "Дельфинье шоу", 45)
        self.mock_animal = Mock(spec=Animal)
        self.mock_animal.animal_id = "dolphin_001"
        self.mock_animal.activity_level = 50  # Добавляем недостающий атрибут
        self.mock_animal.stress_level = 30    # Добавляем недостающий атрибут
        self.mock_trainer = Mock(spec=Trainer)
        self.mock_trainer.staff_id = "trainer_001"

    def test_initialization(self):
        """Тест инициализации шоу"""
        self.assertEqual(self.show.show_id, "show_001")
        self.assertEqual(self.show.name, "Дельфинье шоу")
        self.assertEqual(self.show.duration, 45)
        self.assertEqual(self.show.schedule, [])
        self.assertEqual(self.show.animals_involved, [])
        self.assertEqual(self.show.trainers_required, [])

    def test_schedule_show(self):
        """Тест планирования шоу"""
        show_date = datetime.now() + timedelta(days=1)
        result = self.show.schedule_show(show_date, "main_pool", ["trainer_001"])
        
        self.assertTrue(result)
        self.assertEqual(len(self.show.schedule), 1)
        self.assertEqual(self.show.schedule[0]["location"], "main_pool")

    def test_add_animal(self):
        """Тест добавления животного"""
        self.mock_animal.activity_level = 50
        result = self.show.add_animal(self.mock_animal)
        
        self.assertTrue(result)
        self.assertIn(self.mock_animal, self.show.animals_involved)
        self.assertEqual(self.mock_animal.activity_level, 55)

    def test_add_trainer(self):
        """Тест добавления тренера"""
        result = self.show.add_trainer(self.mock_trainer)
        
        self.assertTrue(result)
        self.assertIn(self.mock_trainer, self.show.trainers_required)

    def test_conduct_show_success(self):
        """Тест успешного проведения шоу"""
        self.show.animals_involved = [self.mock_animal]
        self.show.trainers_required = [self.mock_trainer]
        
        result = self.show.conduct_show()
        
        self.assertIn("success", result)
        self.assertIn("spectator_satisfaction", result)
        self.assertEqual(result["animals_count"], 1)

    def test_conduct_show_no_animals(self):
        """Тест проведения шоу без животных"""
        with self.assertRaises(ValueError):
            self.show.conduct_show()

    def test_conduct_show_no_trainers(self):
        """Тест проведения шоу без тренеров"""
        self.show.animals_involved = [self.mock_animal]
        with self.assertRaises(ValueError):
            self.show.conduct_show()

    def test_get_show_statistics(self):
        """Тест получения статистики шоу"""
        stats = self.show.get_show_statistics()
        
        self.assertEqual(stats["total_scheduled"], 0)
        self.assertEqual(stats["animals_involved"], 0)
        self.assertIn("success_rate", stats)


class TestConservationProgram(unittest.TestCase):
    """Тесты для класса ConservationProgram"""
    
    def setUp(self):
        self.program = ConservationProgram("cons_001", "Дельфины", "Защита популяции")
        self.mock_researcher = Mock(spec=ResearchScientist)
        self.mock_researcher.staff_id = "researcher_001"
        self.mock_researcher.name = "Доктор Иванов"

    def test_initialization(self):
        """Тест инициализации программы"""
        self.assertEqual(self.program.program_id, "cons_001")
        self.assertEqual(self.program.species, "Дельфины")
        self.assertEqual(self.program.goal, "Защита популяции")
        self.assertEqual(self.program.budget, 0.0)

    def test_allocate_budget(self):
        """Тест выделения бюджета"""
        result = self.program.allocate_budget(100000.0)
        
        self.assertTrue(result)
        self.assertEqual(self.program.budget, 100000.0)

    def test_allocate_negative_budget(self):
        """Тест выделения отрицательного бюджета"""
        result = self.program.allocate_budget(-50000.0)
        
        self.assertFalse(result)
        self.assertEqual(self.program.budget, 0.0)

    def test_add_researcher(self):
        """Тест добавления исследователя"""
        result = self.program.add_researcher(self.mock_researcher)
        
        self.assertTrue(result)
        self.assertIn(self.mock_researcher, self.program.researchers)

    def test_add_milestone(self):
        """Тест добавления вехи"""
        deadline = datetime.now() + timedelta(days=30)
        result = self.program.add_milestone("Исследование поведения", deadline)
        
        self.assertTrue(result)
        self.assertEqual(len(self.program.milestones), 1)

    def test_complete_milestone(self):
        """Тест завершения вехи"""
        deadline = datetime.now() + timedelta(days=30)
        self.program.add_milestone("Исследование поведения", deadline)
        
        result = self.program.complete_milestone("MILESTONE_1")
        
        self.assertTrue(result)
        self.assertTrue(self.program.milestones[0]["completed"])

    def test_complete_nonexistent_milestone(self):
        """Тест завершения несуществующей вехи"""
        result = self.program.complete_milestone("NONEXISTENT")
        
        self.assertFalse(result)

    def test_publish_research(self):
        """Тест публикации исследования"""
        publication_id = self.program.publish_research(
            "Исследование дельфинов", 
            "Важные находки о поведении"
        )
        
        self.assertTrue(publication_id.startswith("PUB_"))
        self.assertEqual(len(self.program.published_research), 1)

    def test_get_program_progress(self):
        """Тест получения прогресса программы"""
        progress = self.program.get_program_progress()
        
        self.assertEqual(progress["program_id"], "cons_001")
        self.assertEqual(progress["species"], "Дельфины")
        self.assertEqual(progress["progress"], 0)


class TestWaterTreatmentSystem(unittest.TestCase):
    """Тесты для класса WaterTreatmentSystem"""
    
    def setUp(self):
        self.system = WaterTreatmentSystem("water_001", 1000.0)

    def test_initialization(self):
        """Тест инициализации системы"""
        self.assertEqual(self.system.system_id, "water_001")
        self.assertEqual(self.system.capacity, 1000.0)
        self.assertEqual(self.system.filtration_level, 95.0)
        self.assertIn("ph", self.system.chemical_balance)

    def test_perform_maintenance(self):
        """Тест выполнения обслуживания"""
        self.system.filtration_media_age = 100
        self.system.filtration_level = 80.0
        self.system.status = "needs_maintenance"
        
        result = self.system.perform_maintenance()
        
        self.assertTrue(result)
        self.assertEqual(self.system.filtration_media_age, 0)
        self.assertEqual(self.system.filtration_level, 95.0)
        self.assertEqual(self.system.status, "operational")

    def test_treat_water_success(self):
        """Тест успешной обработки воды"""
        source_quality = {
            "ph": 7.0,
            "ammonia": 5.0,
            "nitrates": 15.0,
            "turbidity": 20.0
        }
        
        result = self.system.treat_water(500.0, source_quality)
        
        self.assertIn("ph", result)
        self.assertIn("ammonia", result)
        self.assertEqual(result["chlorine"], 0.0)
        self.assertLess(result["ammonia"], source_quality["ammonia"])

    def test_treat_water_overflow(self):
        """Тест обработки воды с превышением ёмкости"""
        source_quality = {"ph": 7.0}
        
        with self.assertRaises(TankOverflowException):
            self.system.treat_water(1500.0, source_quality)

    def test_schedule_maintenance(self):
        """Тест планирования обслуживания"""
        maintenance_date = datetime.now() + timedelta(days=7)
        result = self.system.schedule_maintenance(maintenance_date, "routine")
        
        self.assertTrue(result)
        self.assertEqual(len(self.system.maintenance_schedule), 1)

    def test_get_water_quality_report(self):
        """Тест получения отчёта о качестве воды"""
        report = self.system.get_water_quality_report()
        
        self.assertEqual(report["system_id"], "water_001")
        self.assertIn("filtration_level", report)
        self.assertIn("maintenance_due", report)


class TestBreedingProgram(unittest.TestCase):
    """Тесты для класса BreedingProgram"""
    
    def setUp(self):
        self.program = BreedingProgram("breed_001", "Дельфины")
        self.mock_animal1 = Mock(spec=Animal)
        self.mock_animal1.animal_id = "dolphin_001"
        self.mock_animal1.species = "Дельфины"
        self.mock_animal2 = Mock(spec=Animal)
        self.mock_animal2.animal_id = "dolphin_002"
        self.mock_animal2.species = "Дельфины"

    def test_initialization(self):
        """Тест инициализации программы"""
        self.assertEqual(self.program.program_id, "breed_001")
        self.assertEqual(self.program.target_species, "Дельфины")
        self.assertEqual(self.program.breeding_pairs, [])
        self.assertEqual(self.program.successful_births, 0)

    def test_add_breeding_pair_success(self):
        """Тест успешного добавления пары"""
        result = self.program.add_breeding_pair(self.mock_animal1, self.mock_animal2)
        
        self.assertTrue(result)
        self.assertEqual(len(self.program.breeding_pairs), 1)

    def test_add_breeding_pair_wrong_species(self):
        """Тест добавления пары неправильного вида"""
        wrong_species_animal = Mock(spec=Animal)
        wrong_species_animal.animal_id = "shark_001"
        wrong_species_animal.species = "Акулы"
        
        result = self.program.add_breeding_pair(self.mock_animal1, wrong_species_animal)
        
        self.assertFalse(result)
        self.assertEqual(len(self.program.breeding_pairs), 0)

    def test_add_breeding_pair_same_animal(self):
        """Тест добавления одного и того же животного"""
        result = self.program.add_breeding_pair(self.mock_animal1, self.mock_animal1)
        
        self.assertFalse(result)
        self.assertEqual(len(self.program.breeding_pairs), 0)

    def test_attempt_breeding_success(self):
        """Тест попытки размножения"""
        self.program.add_breeding_pair(self.mock_animal1, self.mock_animal2)
        
        with patch('random.random', return_value=0.1):  # Гарантируем успех
            result = self.program.attempt_breeding(0)
            
            self.assertTrue(result["success"])
            self.assertGreater(self.program.successful_births, 0)

    def test_attempt_breeding_invalid_index(self):
        """Тест попытки размножения с неверным индексом"""
        with self.assertRaises(ValueError):
            self.program.attempt_breeding(999)

    def test_introduce_new_genetics(self):
        """Тест введения новой генетики"""
        new_animal = Mock(spec=Animal)
        new_animal.species = "Дельфины"
        
        initial_diversity = self.program.genetic_diversity
        result = self.program.introduce_new_genetics(new_animal)
        
        self.assertTrue(result)
        self.assertGreater(self.program.genetic_diversity, initial_diversity)

    def test_introduce_wrong_species_genetics(self):
        """Тест введения генетики неправильного вида"""
        wrong_species_animal = Mock(spec=Animal)
        wrong_species_animal.species = "Акулы"
        
        initial_diversity = self.program.genetic_diversity
        result = self.program.introduce_new_genetics(wrong_species_animal)
        
        self.assertFalse(result)
        self.assertEqual(self.program.genetic_diversity, initial_diversity)

    def test_get_program_statistics(self):
        """Тест получения статистики программы"""
        stats = self.program.get_program_statistics()
        
        self.assertEqual(stats["program_id"], "breed_001")
        self.assertEqual(stats["target_species"], "Дельфины")
        self.assertEqual(stats["breeding_pairs"], 0)


class TestVisitorCenter(unittest.TestCase):
    """Тесты для класса VisitorCenter"""
    
    def setUp(self):
        self.center = VisitorCenter("center_001", 200)
        self.mock_visitor = Mock(spec=Visitor)
        self.mock_visitor.visitor_id = "visitor_001"
        self.mock_guide = Mock(spec=TourGuide)
        self.mock_guide.staff_id = "guide_001"

    def test_initialization(self):
        """Тест инициализации центра"""
        self.assertEqual(self.center.center_id, "center_001")
        self.assertEqual(self.center.capacity, 200)
        self.assertIn("cafe", self.center.facilities)
        self.assertEqual(self.center.daily_visitors, 0)

    def test_add_facility(self):
        """Тест добавления удобства"""
        result = self.center.add_facility("cinema")
        
        self.assertTrue(result)
        self.assertIn("cinema", self.center.facilities)

    def test_add_existing_facility(self):
        """Тест добавления существующего удобства"""
        result = self.center.add_facility("cafe")
        
        self.assertFalse(result)

    def test_register_visitor_success(self):
        """Тест успешной регистрации посетителя"""
        self.center.current_visitors = []
        self.center.facility_cleanliness = 100.0
        
        result = self.center.register_visitor(self.mock_visitor)
        
        self.assertTrue(result)
        self.assertEqual(self.center.daily_visitors, 1)
        self.assertLess(self.center.facility_cleanliness, 100.0)

    def test_register_visitor_at_capacity(self):
        """Тест регистрации посетителя при полной заполненности"""
        self.center.current_visitors = [Mock(spec=Visitor) for _ in range(200)]
        
        result = self.center.register_visitor(self.mock_visitor)
        
        self.assertFalse(result)

    def test_remove_visitor(self):
        """Тест удаления посетителя"""
        self.center.current_visitors = [self.mock_visitor]
        
        result = self.center.remove_visitor(self.mock_visitor)
        
        self.assertTrue(result)
        self.assertEqual(len(self.center.current_visitors), 0)

    def test_remove_nonexistent_visitor(self):
        """Тест удаления несуществующего посетителя"""
        result = self.center.remove_visitor(self.mock_visitor)
        
        self.assertFalse(result)

    def test_schedule_guided_tour(self):
        """Тест планирования экскурсии"""
        tour_time = datetime.now() + timedelta(hours=2)
        tour_id = self.center.schedule_guided_tour(tour_time, self.mock_guide, 20)
        
        self.assertTrue(tour_id.startswith("TOUR_"))
        self.assertEqual(len(self.center.guided_tours), 1)

    def test_clean_facilities(self):
        """Тест очистки удобств"""
        self.center.facility_cleanliness = 50.0
        result = self.center.clean_facilities()
        
        self.assertTrue(result)
        self.assertEqual(self.center.facility_cleanliness, 100.0)

    def test_get_center_status(self):
        """Тест получения статуса центра"""
        status = self.center.get_center_status()
        
        self.assertEqual(status["center_id"], "center_001")
        self.assertIn("occupancy_rate", status)
        self.assertIn("facility_cleanliness", status)


class TestResearchLaboratory(unittest.TestCase):
    """Тесты для класса ResearchLaboratory"""
    
    def setUp(self):
        self.lab = ResearchLaboratory("lab_001", "Морская биология")
        self.mock_equipment = Mock(spec=Equipment)
        self.mock_scientist = Mock(spec=ResearchScientist)
        self.mock_scientist.name = "Доктор Петров"

    def test_initialization(self):
        """Тест инициализации лаборатории"""
        self.assertEqual(self.lab.lab_id, "lab_001")
        self.assertEqual(self.lab.specialization, "Морская биология")
        self.assertEqual(self.lab.equipment, [])
        self.assertEqual(self.lab.research_projects, [])

    def test_add_equipment(self):
        """Тест добавления оборудования"""
        result = self.lab.add_equipment(self.mock_equipment)
        
        self.assertTrue(result)
        self.assertIn(self.mock_equipment, self.lab.equipment)

    def test_add_existing_equipment(self):
        """Тест добавления существующего оборудования"""
        self.lab.equipment = [self.mock_equipment]
        result = self.lab.add_equipment(self.mock_equipment)
        
        self.assertFalse(result)

    def test_start_research_project(self):
        """Тест начала исследовательского проекта"""
        project_id = self.lab.start_research_project(
            "Исследование кораллов",
            self.mock_scientist,
            180,
            500000.0
        )
        
        self.assertTrue(project_id.startswith("PROJ_"))
        self.assertEqual(len(self.lab.research_projects), 1)

    def test_add_team_member(self):
        """Тест добавления члена команды"""
        project_id = self.lab.start_research_project(
            "Исследование кораллов",
            self.mock_scientist,
            180,
            500000.0
        )
        
        new_scientist = Mock(spec=ResearchScientist)
        result = self.lab.add_team_member(project_id, new_scientist)
        
        self.assertTrue(result)
        self.assertIn(new_scientist, self.lab.research_projects[0]["team"])

    def test_add_team_member_invalid_project(self):
        """Тест добавления члена команды в несуществующий проект"""
        result = self.lab.add_team_member("INVALID_PROJECT", self.mock_scientist)
        
        self.assertFalse(result)

    def test_record_finding(self):
        """Тест записи находки"""
        project_id = self.lab.start_research_project(
            "Исследование кораллов",
            self.mock_scientist,
            180,
            500000.0
        )
        
        result = self.lab.record_finding(project_id, "Важное открытие", 8)
        
        self.assertTrue(result)
        self.assertEqual(len(self.lab.research_projects[0]["findings"]), 1)

    def test_publish_research_success(self):
        """Тест успешной публикации исследования"""
        project_id = self.lab.start_research_project(
            "Исследование кораллов",
            self.mock_scientist,
            1,  # Короткий проект для быстрого завершения
            500000.0
        )
        
        # Устанавливаем прогресс на 100%
        self.lab.research_projects[0]["progress"] = 100.0
        
        publication_id = self.lab.publish_research(project_id, "Nature")
        
        self.assertTrue(publication_id.startswith("PUB_"))
        self.assertEqual(self.lab.research_projects[0]["status"], "completed")

    def test_publish_research_incomplete(self):
        """Тест публикации незавершённого исследования"""
        project_id = self.lab.start_research_project(
            "Исследование кораллов",
            self.mock_scientist,
            180,
            500000.0
        )
        
        publication_id = self.lab.publish_research(project_id, "Nature")
        
        self.assertEqual(publication_id, "")

    def test_get_laboratory_report(self):
        """Тест получения отчёта лаборатории"""
        report = self.lab.get_laboratory_report()
        
        self.assertEqual(report["lab_id"], "lab_001")
        self.assertEqual(report["specialization"], "Морская биология")
        self.assertEqual(report["active_projects"], 0)


class TestAnimalHospital(unittest.TestCase):
    """Тесты для класса AnimalHospital"""
    
    def setUp(self):
        self.hospital = AnimalHospital("hospital_001", 10)
        self.mock_animal = Mock(spec=Animal)
        self.mock_animal.animal_id = "dolphin_001"
        self.mock_animal.health_status = "sick"  # Добавляем недостающий атрибут
        self.mock_animal.stress_level = 80       # Добавляем недостающий атрибут
        self.mock_veterinarian = Mock(spec=Veterinarian)
        self.mock_veterinarian.staff_id = "vet_001"

    def test_initialization(self):
        """Тест инициализации больницы"""
        self.assertEqual(self.hospital.hospital_id, "hospital_001")
        self.assertEqual(self.hospital.capacity, 10)
        self.assertEqual(self.hospital.quarantine_units, [])
        self.assertEqual(self.hospital.patients, [])

    def test_add_quarantine_unit(self):
        """Тест добавления карантинного отделения"""
        result = self.hospital.add_quarantine_unit("quarantine_001", 5)
        
        self.assertTrue(result)
        self.assertEqual(len(self.hospital.quarantine_units), 1)

    def test_add_surgical_room(self):
        """Тест добавления операционной"""
        result = self.hospital.add_surgical_room("surgery_001", ["стол", "лампы"])
        
        self.assertTrue(result)
        self.assertEqual(len(self.hospital.surgical_rooms), 1)

    def test_admit_patient_success(self):
        """Тест успешного приёма пациента"""
        case_id = self.hospital.admit_patient(self.mock_animal, "инфекция", 3)
        
        self.assertTrue(case_id.startswith("CASE_"))
        self.assertEqual(len(self.hospital.patients), 1)

    def test_admit_patient_at_capacity(self):
        """Тест приёма пациента при полной заполненности"""
        # Заполняем больницу
        for i in range(10):
            animal = Mock(spec=Animal)
            animal.animal_id = f"animal_{i}"
            self.hospital.admit_patient(animal, "болезнь", 1)
        
        with self.assertRaises(Exception):
            self.hospital.admit_patient(self.mock_animal, "инфекция", 3)

    def test_assign_veterinarian(self):
        """Тест назначения ветеринара"""
        case_id = self.hospital.admit_patient(self.mock_animal, "инфекция", 3)
        result = self.hospital.assign_veterinarian(case_id, self.mock_veterinarian)
        
        self.assertTrue(result)
        self.assertEqual(self.hospital.patients[0]["assigned_vet"], self.mock_veterinarian)

    def test_assign_veterinarian_invalid_case(self):
        """Тест назначения ветеринара на несуществующий случай"""
        result = self.hospital.assign_veterinarian("INVALID_CASE", self.mock_veterinarian)
        
        self.assertFalse(result)

    def test_perform_surgery_success(self):
        """Тест успешного проведения операции"""
        case_id = self.hospital.admit_patient(self.mock_animal, "травма", 4)
        self.hospital.add_surgical_room("surgery_001", ["стол", "лампы"])
        
        with patch('random.random', return_value=0.1):  # Гарантируем успех
            result = self.hospital.perform_surgery(case_id, "лапаротомия", "surgery_001")
            
            self.assertTrue(result["success"])
            self.assertEqual(result["patient_status"], "recovering")

    def test_perform_surgery_room_occupied(self):
        """Тест проведения операции в занятой операционной"""
        case_id = self.hospital.admit_patient(self.mock_animal, "травма", 4)
        self.hospital.add_surgical_room("surgery_001", ["стол", "лампы"])
        self.hospital.surgical_rooms[0]["is_occupied"] = True
        
        result = self.hospital.perform_surgery(case_id, "лапаротомия", "surgery_001")
        
        self.assertFalse(result["success"])

    def test_discharge_patient(self):
        """Тест выписки пациента"""
        self.mock_animal.health_status = "sick"
        self.mock_animal.stress_level = 80
        
        case_id = self.hospital.admit_patient(self.mock_animal, "инфекция", 3)
        result = self.hospital.discharge_patient(case_id)
        
        self.assertTrue(result)
        self.assertEqual(self.mock_animal.health_status, "healthy")
        self.assertEqual(self.mock_animal.stress_level, 60)

    def test_discharge_nonexistent_patient(self):
        """Тест выписки несуществующего пациента"""
        result = self.hospital.discharge_patient("INVALID_CASE")
        
        self.assertFalse(result)

    def test_get_hospital_status(self):
        """Тест получения статуса больницы"""
        status = self.hospital.get_hospital_status()
        
        self.assertEqual(status["hospital_id"], "hospital_001")
        self.assertEqual(status["current_patients"], 0)
        self.assertIn("success_rate", status)


class TestUnderwaterTunnel(unittest.TestCase):
    """Тесты для класса UnderwaterTunnel"""
    
    def setUp(self):
        self.tunnel = UnderwaterTunnel("tunnel_001", 50.5)
        self.mock_visitor = Mock(spec=Visitor)
        self.mock_visitor.visitor_id = "visitor_001"

    def test_initialization(self):
        """Тест инициализации туннеля"""
        self.assertEqual(self.tunnel.tunnel_id, "tunnel_001")
        self.assertEqual(self.tunnel.length, 50.5)
        self.assertEqual(self.tunnel.viewing_windows, [])
        self.assertEqual(self.tunnel.visitor_capacity, 50)

    def test_add_viewing_window(self):
        """Тест добавления смотрового окна"""
        result = self.tunnel.add_viewing_window("window_001", "large", 25.0)
        
        self.assertTrue(result)
        self.assertEqual(len(self.tunnel.viewing_windows), 1)

    def test_enter_tunnel_success(self):
        """Тест успешного входа в туннель"""
        initial_visibility = self.tunnel.water_visibility
        result = self.tunnel.enter_tunnel(self.mock_visitor)
        
        self.assertTrue(result)
        self.assertIn(self.mock_visitor, self.tunnel.current_visitors)
        self.assertLess(self.tunnel.water_visibility, initial_visibility)

    def test_enter_tunnel_at_capacity(self):
        """Тест входа в туннель при полной заполненности"""
        self.tunnel.current_visitors = [Mock(spec=Visitor) for _ in range(50)]
        result = self.tunnel.enter_tunnel(self.mock_visitor)
        
        self.assertFalse(result)

    def test_exit_tunnel(self):
        """Тест выхода из туннеля"""
        self.tunnel.current_visitors = [self.mock_visitor]
        result = self.tunnel.exit_tunnel(self.mock_visitor)
        
        self.assertTrue(result)
        self.assertEqual(len(self.tunnel.current_visitors), 0)

    def test_exit_tunnel_nonexistent_visitor(self):
        """Тест выхода несуществующего посетителя"""
        result = self.tunnel.exit_tunnel(self.mock_visitor)
        
        self.assertFalse(result)

    def test_schedule_cleaning(self):
        """Тест планирования очистки"""
        cleaning_date = datetime.now() + timedelta(days=7)
        cleaning_id = self.tunnel.schedule_cleaning(cleaning_date, ["worker_001", "worker_002"])
        
        self.assertTrue(cleaning_id.startswith("CLEAN_"))
        self.assertEqual(len(self.tunnel.cleaning_schedule), 1)

    def test_perform_cleaning(self):
        """Тест выполнения очистки"""
        self.tunnel.water_visibility = 60.0
        self.tunnel.add_viewing_window("window_001", "large", 25.0)
        self.tunnel.viewing_windows[0]["cleanliness"] = 50.0
        
        result = self.tunnel.perform_cleaning()
        
        self.assertTrue(result)
        self.assertEqual(self.tunnel.water_visibility, 100.0)
        self.assertEqual(self.tunnel.viewing_windows[0]["cleanliness"], 100.0)

    def test_get_tunnel_status(self):
        """Тест получения статуса туннеля"""
        status = self.tunnel.get_tunnel_status()
        
        self.assertEqual(status["tunnel_id"], "tunnel_001")
        self.assertEqual(status["length"], 50.5)
        self.assertIn("occupancy_rate", status)

class TestEducationalCenter(unittest.TestCase):
    """Тесты для класса EducationalCenter"""
    
    def setUp(self):
        self.center = EducationalCenter("edu_001", 5)
        self.mock_instructor = Mock(spec=Staff)
        self.mock_instructor.name = "Инструктор Иванов"

    def test_initialization(self):
        """Тест инициализации центра"""
        self.assertEqual(self.center.center_id, "edu_001")
        self.assertEqual(self.center.classrooms, 5)
        self.assertEqual(self.center.workshops, [])
        self.assertEqual(self.center.available_classrooms, 5)

    def test_create_workshop(self):
        """Тест создания мастер-класса"""
        workshop_id = self.center.create_workshop(
            "Морская биология для детей",
            "дети 8-12 лет",
            120,
            self.mock_instructor
        )
        
        self.assertTrue(workshop_id.startswith("WORKSHOP_"))
        self.assertEqual(len(self.center.workshops), 1)

    def test_register_student_group(self):
        """Тест регистрации группы студентов"""
        group_id = self.center.register_student_group(
            "Школа №1",
            "10-12 лет",
            25,
            "Учитель Петрова"
        )
        
        self.assertTrue(group_id.startswith("GROUP_"))
        self.assertEqual(len(self.center.student_groups), 1)

    def test_add_educational_material(self):
        """Тест добавления учебного материала"""
        material_id = self.center.add_educational_material(
            "book",
            "Морские обитатели",
            "дети"
        )
        
        self.assertTrue(material_id.startswith("MATERIAL_"))
        self.assertEqual(len(self.center.educational_materials), 1)

    def test_book_classroom_success(self):
        """Тест успешного бронирования класса"""
        booking_date = datetime.now() + timedelta(days=1)
        result = self.center.book_classroom(booking_date, 120, "урок", "group_001")
        
        self.assertTrue(result)
        self.assertEqual(self.center.available_classrooms, 4)

    def test_book_classroom_no_availability(self):
        """Тест бронирования класса при отсутствии доступных"""
        self.center.available_classrooms = 0
        booking_date = datetime.now() + timedelta(days=1)
        result = self.center.book_classroom(booking_date, 120, "урок", "group_001")
        
        self.assertFalse(result)

    def test_conduct_workshop_success(self):
        """Тест успешного проведения мастер-класса"""
        workshop_id = self.center.create_workshop(
            "Морская биология",
            "дети",
            120,
            self.mock_instructor
        )
        
        # Добавляем участников
        self.center.workshops[0]["participants"] = [Mock() for _ in range(20)]
        
        result = self.center.conduct_workshop(workshop_id)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["participants_count"], 20)

    def test_conduct_workshop_low_participation(self):
        """Тест проведения мастер-класса с низкой посещаемостью"""
        workshop_id = self.center.create_workshop(
            "Морская биология",
            "дети",
            120,
            self.mock_instructor
        )
        
        # Добавляем мало участников
        self.center.workshops[0]["participants"] = [Mock() for _ in range(5)]
        self.center.workshops[0]["max_participants"] = 30
        
        result = self.center.conduct_workshop(workshop_id)
        
        self.assertFalse(result["success"])

    def test_conduct_workshop_invalid_id(self):
        """Тест проведения несуществующего мастер-класса"""
        result = self.center.conduct_workshop("INVALID_WORKSHOP")
        
        self.assertFalse(result["success"])

    def test_get_center_statistics(self):
        """Тест получения статистики центра"""
        stats = self.center.get_center_statistics()
        
        self.assertEqual(stats["center_id"], "edu_001")
        self.assertEqual(stats["active_workshops"], 0)
        self.assertEqual(stats["available_classrooms"], 5)


class TestAquacultureFacility(unittest.TestCase):
    """Тесты для класса AquacultureFacility"""
    
    def setUp(self):
        self.facility = AquacultureFacility("aqua_001", "Рыбоводство")

    def test_initialization(self):
        """Тест инициализации предприятия"""
        self.assertEqual(self.facility.facility_id, "aqua_001")
        self.assertEqual(self.facility.production_type, "Рыбоводство")
        self.assertEqual(self.facility.production_capacity, 0.0)
        self.assertEqual(self.facility.species_cultured, [])

    def test_add_species(self):
        """Тест добавления вида"""
        result = self.facility.add_species("Лосось", 1000, 1.5)
        
        self.assertTrue(result)
        self.assertEqual(len(self.facility.species_cultured), 1)
        self.assertGreater(self.facility.production_capacity, 0)

    def test_schedule_harvest(self):
        """Тест планирования сбора урожая"""
        self.facility.add_species("Лосось", 1000, 1.5)
        harvest_date = datetime.now() + timedelta(days=90)
        harvest_id = self.facility.schedule_harvest("Лосось", harvest_date, 800.0)
        
        self.assertTrue(harvest_id.startswith("HARVEST_"))
        self.assertEqual(len(self.facility.harvest_schedule), 1)

    def test_monitor_growth_success(self):
        """Тест успешного мониторинга роста"""
        self.facility.add_species("Лосось", 1000, 1.5)
        result = self.facility.monitor_growth("Лосось")
        
        self.assertIn("stock_count", result)
        self.assertIn("health_index", result)

    def test_monitor_growth_invalid_species(self):
        """Тест мониторинга роста несуществующего вида"""
        result = self.facility.monitor_growth("Несуществующий вид")
        
        self.assertIn("error", result)

    def test_perform_harvest_success(self):
        """Тест успешного сбора урожая"""
        self.facility.add_species("Лосось", 1000, 1.5)
        harvest_date = datetime.now() + timedelta(days=90)
        harvest_id = self.facility.schedule_harvest("Лосось", harvest_date, 800.0)
        
        with patch('random.random', return_value=0.1):  # Гарантируем успех
            result = self.facility.perform_harvest(harvest_id)
            
            self.assertTrue(result["success"])
            self.assertGreater(result["actual_yield"], 0)

    def test_perform_harvest_invalid_id(self):
        """Тест сбора урожая с неверным ID"""
        result = self.facility.perform_harvest("INVALID_HARVEST")
        
        self.assertFalse(result["success"])

    def test_get_facility_report(self):
        """Тест получения отчёта предприятия"""
        report = self.facility.get_facility_report()
        
        self.assertEqual(report["facility_id"], "aqua_001")
        self.assertEqual(report["production_type"], "Рыбоводство")
        self.assertEqual(report["species_count"], 0)


class TestMarineConservation(unittest.TestCase):
    """Тесты для класса MarineConservation"""
    
    def setUp(self):
        self.conservation = MarineConservation("dept_001", ["Защита видов", "Исследования"])

    def test_initialization(self):
        """Тест инициализации отдела"""
        self.assertEqual(self.conservation.department_id, "dept_001")
        self.assertEqual(self.conservation.focus_areas, ["Защита видов", "Исследования"])
        self.assertEqual(self.conservation.conservation_projects, [])
        self.assertEqual(self.conservation.research_grants, [])

    def test_create_conservation_project(self):
        """Тест создания проекта по сохранению"""
        project_id = self.conservation.create_conservation_project(
            "Защита дельфинов",
            "Дельфины",
            24,
            500000.0
        )
        
        self.assertTrue(project_id.startswith("CONS_"))
        self.assertEqual(len(self.conservation.conservation_projects), 1)

    def test_apply_for_grant(self):
        """Тест подачи заявки на грант"""
        with patch('random.random', return_value=0.1):  # Гарантируем успех
            result = self.conservation.apply_for_grant(
                "Исследование кораллов",
                250000.0,
                "Научное исследование"
            )
            
            self.assertTrue(result["approved"])
            self.assertGreater(result["amount_approved"], 0)

    def test_organize_community_event(self):
        """Тест организации мероприятия для сообщества"""
        event_id = self.conservation.organize_community_event(
            "День океана",
            "фестиваль",
            "все возрасты",
            500
        )
        
        self.assertTrue(event_id.startswith("EVENT_"))
        self.assertEqual(len(self.conservation.community_outreach), 1)

    def test_record_success_story(self):
        """Тест записи истории успеха"""
        story_id = self.conservation.record_success_story(
            "Спасение дельфинов",
            "Успешно реабилитировали группу дельфинов",
            "Дельфины",
            "фотографии, отчёты"
        )
        
        self.assertTrue(story_id.startswith("STORY_"))
        self.assertEqual(len(self.conservation.success_stories), 1)

    def test_get_conservation_report(self):
        """Тест получения отчёта по консервации"""
        report = self.conservation.get_conservation_report()
        
        self.assertEqual(report["department_id"], "dept_001")
        self.assertEqual(report["focus_areas"], ["Защита видов", "Исследования"])
        self.assertEqual(report["active_projects"], 0)


class TestOceanographicResearch(unittest.TestCase):
    """Тесты для класса OceanographicResearch"""
    
    def setUp(self):
        self.research = OceanographicResearch("research_001", "Тихий океан")

    def test_initialization(self):
        """Тест инициализации исследований"""
        self.assertEqual(self.research.research_id, "research_001")
        self.assertEqual(self.research.ocean_region, "Тихий океан")
        self.assertEqual(self.research.research_vessels, [])
        self.assertEqual(self.research.data_collection, [])

    def test_add_research_vessel(self):
        """Тест добавления исследовательского судна"""
        vessel_id = self.research.add_research_vessel(
            "Исследователь-1",
            20,
            ["сонар", "гидролокатор"]
        )
        
        self.assertTrue(vessel_id.startswith("VESSEL_"))
        self.assertEqual(len(self.research.research_vessels), 1)

    def test_plan_expedition(self):
        """Тест планирования экспедиции"""
        vessel_id = self.research.add_research_vessel("Исследователь-1", 20, [])
        expedition_id = self.research.plan_expedition(
            "Изучение течений",
            ["картирование", "забор проб"],
            30,
            vessel_id
        )
        
        self.assertTrue(expedition_id.startswith("EXPED_"))
        self.assertEqual(len(self.research.research_expeditions), 1)

    def test_collect_ocean_data(self):
        """Тест сбора океанографических данных"""
        data_id = self.research.collect_ocean_data(
            "temperature",
            "Тихий океан, точка А",
            100.0,
            {"temp": 15.5, "salinity": 35.0}
        )
        
        self.assertTrue(data_id.startswith("DATA_"))
        self.assertEqual(len(self.research.data_collection), 1)

    def test_record_discovery(self):
        """Тест записи научного открытия"""
        discovery_id = self.research.record_discovery(
            "Новый вид кораллов",
            "Обнаружен ранее неизвестный вид кораллов",
            8,
            ["фотографии", "образцы"]
        )
        
        self.assertTrue(discovery_id.startswith("DISCOV_"))
        self.assertEqual(len(self.research.scientific_discoveries), 1)

    def test_get_research_summary(self):
        """Тест получения сводки исследований"""
        summary = self.research.get_research_summary()
        
        self.assertEqual(summary["research_id"], "research_001")
        self.assertEqual(summary["ocean_region"], "Тихий океан")
        self.assertEqual(summary["research_vessels"], 0)


class TestOceanariumIntegration(unittest.TestCase):
    """Интеграционные тесты для класса Oceanarium"""
    
    def setUp(self):
        self.oceanarium = Oceanarium("Тестовый океанариум", "Москва", 1000)
        self.mock_animal = Mock(spec=Animal)
        self.mock_animal.animal_id = "animal_001"
        self.mock_animal.species = "Дельфин"
        self.mock_animal.check_health.return_value = "healthy"
        self.mock_animal.last_feeding = datetime.now() - timedelta(hours=2)
        self.mock_animal.get_feeding_requirements.return_value = {"рыба": 5.0}
        self.mock_animal.tank_id = "tank_001"  # Добавляем недостающий атрибут
        
        self.mock_tank = Mock(spec=Tank)
        self.mock_tank.tank_id = "tank_001"
        self.mock_tank.add_animal.return_value = True
        self.mock_tank.remove_animal.return_value = True
        self.mock_tank.check_water_quality.return_value = {"temperature": True, "ph": True}
        self.mock_tank.animals = [self.mock_animal]
        self.mock_tank.last_cleaned = datetime.now()
        
        self.mock_staff = Mock(spec=Staff)
        self.mock_staff.staff_id = "staff_001"
        self.mock_staff.name = "Иван Иванов"
        self.mock_staff.access_level = 2
        self.mock_staff.calculate_monthly_salary.return_value = 50000.0
        
        self.mock_feeder = Mock(spec=Feeder)
        self.mock_feeder.staff_id = "feeder_001"
        self.mock_feeder.feed_animal.return_value = True
        
        self.mock_veterinarian = Mock(spec=Veterinarian)
        self.mock_veterinarian.staff_id = "vet_001"
        self.mock_veterinarian.examine_animal.return_value = {"status": "healthy"}
        
        self.mock_visitor = Mock(spec=Visitor)
        self.mock_visitor.visitor_id = "visitor_001"
        self.mock_visitor.visit_history = [{"exit_time": None}]
        self.mock_visitor.age_group = "adult"
        self.mock_visitor.visit_duration = timedelta(hours=2)
        
        self.mock_equipment = Mock(spec=Equipment)
        self.mock_equipment.equipment_id = "equip_001"
        self.mock_equipment.needs_maintenance = False
        self.mock_equipment.perform_maintenance.return_value = True

    def test_add_animal_success(self):
        """Тест успешного добавления животного"""
        self.oceanarium.tanks["tank_001"] = self.mock_tank
        
        result = self.oceanarium.add_animal(self.mock_animal, "tank_001")
        
        self.assertTrue(result)
        self.assertIn("animal_001", self.oceanarium.animals)

    def test_add_animal_tank_not_found(self):
        """Тест добавления животного в несуществующий резервуар"""
        with self.assertRaises(ValueError):
            self.oceanarium.add_animal(self.mock_animal, "nonexistent_tank")

    def test_hire_staff(self):
        """Тест найма сотрудника"""
        with patch.object(self.oceanarium.security_system, 'issue_keycard') as mock_issue:
            self.oceanarium.hire_staff(self.mock_staff)
            
            self.assertIn("staff_001", self.oceanarium.staff)
            mock_issue.assert_called_once()

    def test_add_visitor(self):
        """Тест добавления посетителя"""
        self.oceanarium.add_visitor(self.mock_visitor)
        
        self.assertIn("visitor_001", self.oceanarium.visitors)
        self.assertEqual(self.oceanarium.daily_visitors, 1)

    def test_create_ticket_office(self):
        """Тест создания кассы"""
        office = self.oceanarium.create_ticket_office("office_001", "Кассир")
        
        self.assertEqual(office.office_id, "office_001")
        self.assertEqual(len(self.oceanarium.ticket_offices), 1)

    def test_feed_all_animals_with_feeder(self):
        """Тест кормления животных с доступным кормильцем"""
        self.oceanarium.animals["animal_001"] = self.mock_animal
        self.oceanarium.staff["feeder_001"] = self.mock_feeder
        
        results = self.oceanarium.feed_all_animals()
        
        self.assertTrue(results["animal_001"])
        self.mock_feeder.feed_animal.assert_called_once()

    def test_feed_all_animals_no_feeder(self):
        """Тест кормления животных без кормильца"""
        self.oceanarium.animals["animal_001"] = self.mock_animal
        
        results = self.oceanarium.feed_all_animals()
        
        self.assertFalse(results["animal_001"])

    def test_conduct_health_checks_with_vet(self):
        """Тест медицинских осмотров с ветеринаром"""
        self.oceanarium.animals["animal_001"] = self.mock_animal
        self.oceanarium.staff["vet_001"] = self.mock_veterinarian
        
        results = self.oceanarium.conduct_health_checks()
        
        self.assertIn("animal_001", results)
        self.mock_veterinarian.examine_animal.assert_called_once_with(self.mock_animal)

    def test_conduct_health_checks_no_vet(self):
        """Тест медицинских осмотров без ветеринара"""
        self.oceanarium.animals["animal_001"] = self.mock_animal
        
        with self.assertRaises(AnimalHealthException):
            self.oceanarium.conduct_health_checks()

    def test_monitor_water_quality(self):
        """Тест мониторинга качества воды"""
        self.oceanarium.tanks["tank_001"] = self.mock_tank
        
        results = self.oceanarium.monitor_water_quality()
        
        self.assertIn("tank_001", results)
        self.mock_tank.check_water_quality.assert_called_once()

    def test_generate_daily_report(self):
        """Тест генерации ежедневного отчёта"""
        self.oceanarium.tanks["tank_001"] = self.mock_tank
        self.oceanarium.animals = {"animal1": self.mock_animal}
        self.oceanarium.daily_visitors = 100
        
        report = self.oceanarium.generate_daily_report()
        
        self.assertEqual(report["visitor_count"], 100)
        self.assertEqual(report["animal_count"], 1)
        self.assertIn("tank_001", report["tank_status"])

    def test_close_and_open_for_day(self):
        """Тест закрытия и открытия на день"""
        mock_office = Mock()
        mock_office.daily_sales = []
        mock_office.end_shift.return_value = {"total_sales": 1000.0}
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
        self.oceanarium.visitors["visitor_001"] = self.mock_visitor
        
        rate = self.oceanarium.get_occupancy_rate()
        self.assertGreaterEqual(rate, 0.0)
        self.assertLessEqual(rate, 100.0)

    def test_transfer_animal_success(self):
        """Тест успешного перемещения животного"""
        mock_tank2 = Mock(spec=Tank)
        mock_tank2.tank_id = "tank_002"
        mock_tank2.add_animal.return_value = True
        
        self.oceanarium.animals["animal_001"] = self.mock_animal
        self.oceanarium.tanks["tank_001"] = self.mock_tank
        self.oceanarium.tanks["tank_002"] = mock_tank2
        
        result = self.oceanarium.transfer_animal("animal_001", "tank_001", "tank_002")
        
        self.assertTrue(result)
        self.mock_tank.remove_animal.assert_called_once_with("animal_001")
        mock_tank2.add_animal.assert_called_once_with(self.mock_animal)

    def test_transfer_animal_invalid(self):
        """Тест перемещения несуществующего животного"""
        result = self.oceanarium.transfer_animal("none", "tank1", "tank2")
        self.assertFalse(result)

    def test_calculate_monthly_expenses(self):
        """Тест расчета месячных расходов"""
        self.oceanarium.staff = {"staff1": self.mock_staff}
        self.oceanarium.animals = {"animal1": self.mock_animal}
        self.oceanarium.equipment = {"equip1": self.mock_equipment}
        
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
        self.oceanarium.animals = {
            "animal1": self.mock_animal,
        }
        
        stats = self.oceanarium.get_animal_statistics()
        
        self.assertEqual(stats["total_animals"], 1)
        self.assertIn("species_count", stats)
        self.assertIn("health_distribution", stats)
        self.assertIn("feeding_status", stats)
        self.assertIn("tank_distribution", stats)


if __name__ == '__main__':
    unittest.main()
