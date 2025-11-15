class QualityAssuranceTester(GameEntity):
    """
    Класс тестировщика качества.
    
    Attributes:
        tester_id (str): Уникальный идентификатор тестировщика
        found_bugs (List[Dict]): Найденные баги
        test_cases (List[Dict]): Тест-кейсы
    """

    def __init__(self, tester_id: str, name: str):
        super().__init__(tester_id, name)
        self.found_bugs = []
        self.test_cases = []
        self.specialization = "functional"  # functional, performance, compatibility
        self.bugs_fixed = 0
        self.test_areas = ["combat", "quests", "economy", "ui", "performance"]

    def update(self, delta_time: float) -> None:
        """Обновляет состояние тестировщика."""
        pass

    def create_test_case(self, case_id: str, area: str, description: str,
                        steps: List[str], expected_result: str) -> Dict[str, Any]:
        """Создает тест-кейс."""
        test_case = {
            "case_id": case_id,
            "area": area,
            "description": description,
            "steps": steps,
            "expected_result": expected_result,
            "created_by": self.entity_id,
            "status": "not_tested"
        }
        
        self.test_cases.append(test_case)
        return test_case

    def execute_test_case(self, case_id: str, actual_result: str) -> Dict[str, Any]:
        """Выполняет тест-кейс."""
        test_case = next((tc for tc in self.test_cases if tc["case_id"] == case_id), None)
        if not test_case:
            return {}
        
        test_case["actual_result"] = actual_result
        test_case["executed_at"] = datetime.now()
        test_case["status"] = "passed" if actual_result == test_case["expected_result"] else "failed"
        
        if test_case["status"] == "failed":
            self._report_bug(
                f"Test case {case_id} failed",
                f"Expected: {test_case['expected_result']}, Got: {actual_result}",
                "medium",
                test_case["area"]
            )
        
        return test_case

    def _report_bug(self, title: str, description: str, severity: str, area: str) -> str:
        """Сообщает о найденном баге."""
        bug_id = f"bug_{len(self.found_bugs):04d}"
        bug_report = {
            "bug_id": bug_id,
            "title": title,
            "description": description,
            "severity": severity,  # low, medium, high, critical
            "area": area,
            "reported_by": self.entity_id,
            "reported_at": datetime.now(),
            "status": "open",
            "steps_to_reproduce": [],
            "assigned_to": None
        }
        
        self.found_bugs.append(bug_report)
        return bug_id

    def performance_test(self, game_system: 'GameDevelopment') -> Dict[str, Any]:
        """Проводит тест производительности."""
        performance_report = {
            "test_date": datetime.now(),
            "average_frame_rate": random.uniform(45, 120),
            "memory_usage_mb": random.uniform(500, 2000),
            "load_times_seconds": random.uniform(1, 10),
            "network_latency_ms": random.uniform(20, 100),
            "server_performance": random.uniform(70, 95)
        }
        
        # Проверка на соответствие стандартам
        performance_report["meets_standards"] = (
            performance_report["average_frame_rate"] >= 60 and
            performance_report["memory_usage_mb"] <= 1500 and
            performance_report["load_times_seconds"] <= 5
        )
        
        if not performance_report["meets_standards"]:
            self._report_bug(
                "Performance below standards",
                f"Frame rate: {performance_report['average_frame_rate']:.1f} FPS",
                "high",
                "performance"
            )
        
        return performance_report

