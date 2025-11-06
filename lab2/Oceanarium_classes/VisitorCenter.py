class VisitorCenter:
    """Центр для посетителей."""
    
    def __init__(self, center_id: str, capacity: int):
        self.center_id = center_id
        self.capacity = capacity
        self.facilities = ["information_desk", "restrooms", "cafe", "gift_shop"]
        self.daily_visitors = 0
        self.guided_tours = []
        self.opening_hours = {"open": "09:00", "close": "18:00"}
        self.amenities = []
        self.staff_count = 0

    def add_facility(self, facility: str) -> None:
        """Добавляет объект в центр."""
        if facility not in self.facilities:
            self.facilities.append(facility)

    def register_visitor_entry(self) -> bool:
        """Регистрирует вход посетителя."""
        if self.daily_visitors < self.capacity:
            self.daily_visitors += 1
            return True
        return False

    def schedule_guided_tour(self, tour_name: str, guide: TourGuide, 
                           start_time: datetime, duration: int) -> str:
        """Планирует экскурсию с гидом."""
        tour_id = f"TOUR_{len(self.guided_tours):04d}"
        tour = {
            "tour_id": tour_id,
            "name": tour_name,
            "guide": guide,
            "start_time": start_time,
            "duration": duration,
            "max_participants": 20,
            "participants_registered": 0,
            "status": "scheduled"
        }
        self.guided_tours.append(tour)
        return tour_id

    def calculate_occupancy_rate(self) -> float:
        """Рассчитывает заполненность центра."""
        return (self.daily_visitors / self.capacity) * 100

    def add_amenity(self, amenity: str, capacity: int) -> None:
        """Добавляет удобство для посетителей."""
        self.amenities.append({
            "name": amenity,
            "capacity": capacity,
            "current_usage": 0
        })
