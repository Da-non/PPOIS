class UnderwaterTunnel:
    """Подводный туннель для посетителей."""
    
    def __init__(self, tunnel_id: str, length: float):
        self.tunnel_id = tunnel_id
        self.length = length
        self.viewing_windows = []
        self.cleaning_schedule = []
        self.visitor_capacity = 50
        self.current_visitors = 0
        self.water_depth = random.uniform(5, 15)
        self.marine_life_visible = []
        self.lighting_system = "LED"
        self.emergency_exits = []

    def add_viewing_window(self, window_id: str, size: str, location: float) -> None:
        """Добавляет смотровое окно."""
        window = {
            "window_id": window_id,
            "size": size,
            "location": location,  # позиция вдоль туннеля
            "cleanliness": 100.0,
            "last_cleaned": datetime.now()
        }
        self.viewing_windows.append(window)

    def enter_visitor(self) -> bool:
        """Регистрирует вход посетителя в туннель."""
        if self.current_visitors < self.visitor_capacity:
            self.current_visitors += 1
            return True
        return False

    def exit_visitor(self) -> bool:
        """Регистрирует выход посетителя из туннеля."""
        if self.current_visitors > 0:
            self.current_visitors -= 1
            return True
        return False

    def schedule_cleaning(self, cleaning_type: str, date: datetime) -> str:
        """Планирует очистку туннеля."""
        cleaning_id = f"CLEAN_{len(self.cleaning_schedule):04d}"
        cleaning = {
            "cleaning_id": cleaning_id,
            "type": cleaning_type,
            "scheduled_date": date,
            "completed": False,
            "crew_assigned": []
        }
        self.cleaning_schedule.append(cleaning)
        return cleaning_id

    def add_marine_life(self, animal_species: str, count: int) -> None:
        """Добавляет морскую жизнь для наблюдения."""
        self.marine_life_visible.append({
            "species": animal_species,
            "count": count,
            "visibility_rating": random.uniform(70, 95)
        })
