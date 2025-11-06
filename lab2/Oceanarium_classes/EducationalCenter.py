class EducationalCenter:
    """Образовательный центр."""
    
    def __init__(self, center_id: str, classrooms: int):
        self.center_id = center_id
        self.classrooms = classrooms
        self.workshops = []
        self.student_groups = []
        self.educational_materials = []
        self.available_classrooms = classrooms
        self.booking_schedule = []

    def create_workshop(self, workshop_name: str, target_audience: str, duration: int, 
                       instructor: Staff) -> str:
        """Создаёт мастер-класс."""
        workshop_id = f"WORKSHOP_{len(self.workshops) + 1}"
        workshop = {
            "workshop_id": workshop_id,
            "name": workshop_name,
            "target_audience": target_audience,
            "duration": duration,
            "instructor": instructor,
            "max_participants": random.randint(15, 30),
            "participants": [],
            "status": "scheduled"
        }
        self.workshops.append(workshop)
        return workshop_id

    def register_student_group(self, group_name: str, age_range: str, size: int, 
                              teacher: str) -> str:
        """Регистрирует группу студентов."""
        group_id = f"GROUP_{len(self.student_groups) + 1}"
        group = {
            "group_id": group_id,
            "name": group_name,
            "age_range": age_range,
            "size": size,
            "teacher": teacher,
            "visit_history": [],
            "preferences": []
        }
        self.student_groups.append(group)
        return group_id

    def add_educational_material(self, material_type: str, title: str, 
                               target_audience: str) -> str:
        """Добавляет учебный материал."""
        material_id = f"MATERIAL_{len(self.educational_materials) + 1}"
        material = {
            "material_id": material_id,
            "type": material_type,  # book, video, interactive, etc.
            "title": title,
            "target_audience": target_audience,
            "usage_count": 0,
            "added_date": datetime.now()
        }
        self.educational_materials.append(material)
        return material_id

    def book_classroom(self, booking_date: datetime, duration: int, purpose: str, 
                      group_id: str) -> bool:
        """Бронирует классную комнату."""
        if self.available_classrooms > 0:
            booking = {
                "booking_id": f"BOOKING_{len(self.booking_schedule) + 1}",
                "date": booking_date,
                "duration": duration,
                "purpose": purpose,
                "group_id": group_id,
                "classroom_number": self.classrooms - self.available_classrooms + 1
            }
            self.booking_schedule.append(booking)
            self.available_classrooms -= 1
            return True
        return False

    def conduct_workshop(self, workshop_id: str) -> Dict[str, Any]:
        """Проводит мастер-класс."""
        workshop = next((w for w in self.workshops if w["workshop_id"] == workshop_id), None)
        if not workshop:
            return {"success": False, "error": "Мастер-класс не найден"}

        participation_rate = len(workshop["participants"]) / workshop["max_participants"] * 100
        success = participation_rate >= 60

        if success:
            workshop["status"] = "completed"
            # Увеличиваем счётчик использования материалов
            for material in self.educational_materials:
                if material["target_audience"] == workshop["target_audience"]:
                    material["usage_count"] += 1

        return {
            "success": success,
            "workshop_id": workshop_id,
            "participation_rate": participation_rate,
            "participants_count": len(workshop["participants"]),
            "completion_date": datetime.now() if success else None
        }

    def get_center_statistics(self) -> Dict[str, Any]:
        """Возвращает статистику центра."""
        active_workshops = len([w for w in self.workshops if w["status"] == "scheduled"])
        completed_workshops = len([w for w in self.workshops if w["status"] == "completed"])
        total_students = sum(group["size"] for group in self.student_groups)
        
        return {
            "center_id": self.center_id,
            "active_workshops": active_workshops,
            "completed_workshops": completed_workshops,
            "student_groups": len(self.student_groups),
            "total_students": total_students,
            "educational_materials": len(self.educational_materials),
            "available_classrooms": self.available_classrooms,
            "bookings_today": len([b for b in self.booking_schedule if b["date"].date() == datetime.now().date()])
        }

