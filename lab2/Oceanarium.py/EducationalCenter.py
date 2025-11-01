class EducationalCenter:
    """Образовательный центр."""
    
    def __init__(self, center_id: str, classrooms: int):
        self.center_id = center_id
        self.classrooms = classrooms
        self.workshops = []
        self.student_groups = []
        self.educational_materials = []
        self.teachers = []
        self.daily_students = 0
        self.equipment_available = []
        self.research_facilities = []

    def schedule_workshop(self, workshop_name: str, instructor: Staff,
                         date: datetime, duration: int, max_students: int) -> str:
        """Планирует образовательный семинар."""
        workshop_id = f"WORKSHOP_{len(self.workshops):04d}"
        workshop = {
            "workshop_id": workshop_id,
            "name": workshop_name,
            "instructor": instructor,
            "date": date,
            "duration": duration,
            "max_students": max_students,
            "students_registered": 0,
            "materials_required": [],
            "status": "scheduled"
        }
        self.workshops.append(workshop)
        return workshop_id

    def register_student_group(self, group_name: str, age_range: str, 
                             student_count: int, teacher: str) -> str:
        """Регистрирует группу студентов."""
        group_id = f"GROUP_{len(self.student_groups):04d}"
        group = {
            "group_id": group_id,
            "name": group_name,
            "age_range": age_range,
            "student_count": student_count,
            "teacher": teacher,
            "visit_date": None,
            "activities_scheduled": []
        }
        self.student_groups.append(group)
        return group_id

    def add_educational_material(self, material_type: str, title: str, 
                               target_audience: str) -> None:
        """Добавляет образовательный материал."""
        material = {
            "type": material_type,  # book, video, interactive
            "title": title,
            "target_audience": target_audience,
            "added_date": datetime.now(),
            "usage_count": 0
        }
        self.educational_materials.append(material)

    def calculate_educational_impact(self) -> float:
        """Рассчитывает образовательное воздействие."""
        workshops_impact = len(self.workshops) * 10
        students_impact = self.daily_students * 2
        materials_impact = len(self.educational_materials) * 5
        
        total_impact = workshops_impact + students_impact + materials_impact
        return min(100, total_impact / 10)
