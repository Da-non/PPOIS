class VisitorCenter:
    """Центр для посетителей."""
    
    def __init__(self, center_id: str, capacity: int):
        self.center_id = center_id
        self.capacity = capacity
        self.facilities = ["cafe", "gift_shop", "restrooms", "information_desk"]
        self.daily_visitors = 0
        self.guided_tours = []
        self.current_visitors = []
        self.opening_time = "09:00"
        self.closing_time = "18:00"
        self.facility_cleanliness = 100.0

    def add_facility(self, facility: str) -> bool:
        """Добавляет удобство в центр."""
        if facility not in self.facilities:
            self.facilities.append(facility)
            return True
        return False

    def register_visitor(self, visitor: Visitor) -> bool:
        """Регистрирует посетителя в центре."""
        if len(self.current_visitors) < self.capacity:
            self.current_visitors.append(visitor)
            self.daily_visitors += 1
            self.facility_cleanliness -= 0.1  # Небольшое снижение чистоты
            return True
        return False

    def remove_visitor(self, visitor: Visitor) -> bool:
        """Удаляет посетителя из центра."""
        if visitor in self.current_visitors:
            self.current_visitors.remove(visitor)
            return True
        return False

    def schedule_guided_tour(self, tour_time: datetime, guide: TourGuide, max_participants: int) -> str:
        """Планирует экскурсию с гидом."""
        tour_id = f"TOUR_{len(self.guided_tours) + 1}"
        tour = {
            "tour_id": tour_id,
            "time": tour_time,
            "guide": guide,
            "max_participants": max_participants,
            "participants": [],
            "status": "scheduled"
        }
        self.guided_tours.append(tour)
        return tour_id

    def clean_facilities(self) -> bool:
        """Очищает удобства центра."""
        self.facility_cleanliness = 100.0
        return True

    def get_center_status(self) -> Dict[str, Any]:
        """Возвращает статус центра."""
        occupancy_rate = (len(self.current_visitors) / self.capacity) * 100
        
        return {
            "center_id": self.center_id,
            "current_visitors": len(self.current_visitors),
            "daily_visitors": self.daily_visitors,
            "occupancy_rate": occupancy_rate,
            "facility_cleanliness": self.facility_cleanliness,
            "scheduled_tours": len([t for t in self.guided_tours if t["status"] == "scheduled"]),
            "available_facilities": len(self.facilities)
        }
