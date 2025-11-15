class UnderwaterTunnel:
    """Подводный туннель для посетителей."""
    
    def __init__(self, tunnel_id: str, length: float):
        self.tunnel_id = tunnel_id
        self.length = length
        self.viewing_windows = []
        self.cleaning_schedule = []
        self.visitor_capacity = 50
        self.current_visitors = []
        self.water_visibility = random.uniform(80, 100)
        self.lighting_intensity = random.uniform(70, 100)
        self.maintenance_status = "operational"

    def add_viewing_window(self, window_id: str, size: str, location: float) -> bool:
        """Добавляет смотровое окно."""
        window = {
            "window_id": window_id,
            "size": size,
            "location": location,  # положение вдоль туннеля
            "cleanliness": 100.0,
            "last_cleaned": datetime.now()
        }
        self.viewing_windows.append(window)
        return True

    def enter_tunnel(self, visitor: Visitor) -> bool:
        """Посетитель входит в туннель."""
        if len(self.current_visitors) < self.visitor_capacity:
            self.current_visitors.append(visitor)
            # Небольшое снижение видимости из-за посетителей
            self.water_visibility = max(60, self.water_visibility - 0.1)
            return True
        return False

    def exit_tunnel(self, visitor: Visitor) -> bool:
        """Посетитель выходит из туннеля."""
        if visitor in self.current_visitors:
            self.current_visitors.remove(visitor)
            return True
        return False

    def schedule_cleaning(self, cleaning_date: datetime, cleaning_crew: List[str]) -> str:
        """Планирует очистку туннеля."""
        cleaning_id = f"CLEAN_{len(self.cleaning_schedule) + 1}"
        cleaning = {
            "cleaning_id": cleaning_id,
            "date": cleaning_date,
            "crew": cleaning_crew,
            "status": "scheduled",
            "duration_hours": random.randint(2, 6)
        }
        self.cleaning_schedule.append(cleaning)
        return cleaning_id

    def perform_cleaning(self) -> bool:
        """Выполняет очистку туннеля."""
        self.water_visibility = 100.0
        for window in self.viewing_windows:
            window["cleanliness"] = 100.0
            window["last_cleaned"] = datetime.now()
        return True

    def get_tunnel_status(self) -> Dict[str, Any]:
        """Возвращает статус туннеля."""
        occupancy = (len(self.current_visitors) / self.visitor_capacity) * 100
        
        return {
            "tunnel_id": self.tunnel_id,
            "length": self.length,
            "current_visitors": len(self.current_visitors),
            "occupancy_rate": occupancy,
            "water_visibility": self.water_visibility,
            "viewing_windows": len(self.viewing_windows),
            "maintenance_status": self.maintenance_status,
            "next_cleaning": self.cleaning_schedule[0]["date"] if self.cleaning_schedule else None
        }


