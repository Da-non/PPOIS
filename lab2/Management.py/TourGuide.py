class TourGuide(Staff):
    """
    Класс экскурсовода.
    """
    
    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int):
        super().__init__(staff_id, name, "Tour Guide", salary, experience_years)
        self.languages = ["russian"]
        self.tour_routes = []
        self.groups_per_day = random.randint(3, 8)
        self.visitor_satisfaction = random.uniform(80, 98)
        self.knowledge_base = {}
        self.access_level = 2
        self.tours_conducted = 0
        self.specializations = []

    def perform_daily_tasks(self) -> List[str]:
        tasks = [
            "Проведение экскурсий",
            "Ответы на вопросы посетителей",
            "Обновление знаний о животных",
            "Подготовка экскурсионных материалов",
            "Координация с другими гидами"
        ]
        self.workload = min(100, self.workload + 25)
        return tasks

    def conduct_tour(self, visitors: List[Visitor], route: str, language: str = "russian") -> Dict[str, any]:
        """Проводит экскурсию."""
        if language not in self.languages:
            return {"error": "Язык не поддерживается"}

        if not visitors:
            return {"error": "Нет посетителей для экскурсии"}

        # Расчет качества экскурсии
        base_quality = self.visitor_satisfaction
        experience_bonus = self.experience_years * 2
        language_penalty = 0 if language == "russian" else 5
        
        final_quality = base_quality + experience_bonus - language_penalty
        final_quality = max(50, min(100, final_quality))

        tour_result = {
            "route": route,
            "visitor_count": len(visitors),
            "duration": random.uniform(45, 120),
            "satisfaction_score": final_quality,
            "questions_answered": random.randint(5, 20),
            "language": language,
            "guide": self.name,
            "timestamp": datetime.now()
        }

        self.tours_conducted += 1
        self.workload = min(100, self.workload + 15)
        return tour_result

    def add_language(self, language: str) -> None:
        """Добавляет знание языка."""
        if language not in self.languages:
            self.languages.append(language)
            self.visitor_satisfaction = min(100, self.visitor_satisfaction + 2)

    def learn_animal_facts(self, animal_species: str, facts: List[str]) -> None:
        """Изучает факты о животных."""
        if animal_species not in self.knowledge_base:
            self.knowledge_base[animal_species] = []
        
        new_facts = [fact for fact in facts if fact not in self.knowledge_base[animal_species]]
        self.knowledge_base[animal_species].extend(new_facts)
        
        # Улучшение удовлетворенности за изучение
        if new_facts:
            self.visitor_satisfaction = min(100, self.visitor_satisfaction + len(new_facts) * 0.5)

    def add_tour_route(self, route_name: str, stops: List[str]) -> None:
        """Добавляет экскурсионный маршрут."""
        route = {
            "name": route_name,
            "stops": stops,
            "duration": len(stops) * 10,  # минут на остановку
            "difficulty": "easy"  # easy, medium, hard
        }
        self.tour_routes.append(route)
