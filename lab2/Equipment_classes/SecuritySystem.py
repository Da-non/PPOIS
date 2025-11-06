class SecuritySystem:
    """
    Система безопасности океанариума.

    Attributes:
        system_id (str): Идентификатор системы
        access_zones (Dict): Зоны доступа
        key_cards (List[Dict]): Список карт доступа
        security_logs (List[Dict]): Журнал безопасности
    """

    def __init__(self, system_id: str):
        self.system_id = system_id
        self.access_zones = {}
        self.key_cards = []
        self.security_logs = []
        self.emergency_mode = False
        self.cameras = []
        self.motion_sensors = []
        self.alarm_status = "disarmed"

    def create_access_zone(self, zone_id: str, zone_name: str, required_level: int) -> None:
        """Создаёт зону доступа."""
        self.access_zones[zone_id] = {
            "name": zone_name,
            "required_level": required_level,
            "current_occupants": [],
            "max_occupancy": random.randint(5, 50),
            "emergency_lockdown": False
        }

    def issue_keycard(self, user_id: str, user_name: str, access_level: int) -> str:
        """Выдаёт карту доступа."""
        card_id = f"CARD_{len(self.key_cards):04d}"
        keycard = {
            "card_id": card_id,
            "user_id": user_id,
            "user_name": user_name,
            "access_level": access_level,
            "issued_date": datetime.now(),
            "expires_date": datetime.now() + timedelta(days=365),
            "active": True,
            "access_attempts": []
        }
        self.key_cards.append(keycard)
        return card_id

    def check_access(self, card_id: str, zone_id: str) -> bool:
        """Проверяет доступ к зоне."""
        # Находим карту
        keycard = None
        for card in self.key_cards:
            if card["card_id"] == card_id:
                keycard = card
                break

        if not keycard or not keycard["active"]:
            self.log_security_event("access_denied", f"Неактивная карта {card_id}", zone_id)
            return False

        # Проверяем истечение срока
        if datetime.now() > keycard["expires_date"]:
            self.log_security_event("access_denied", f"Просроченная карта {card_id}", zone_id)
            return False

        # Проверяем уровень доступа
        if zone_id in self.access_zones:
            required_level = self.access_zones[zone_id]["required_level"]
            if keycard["access_level"] >= required_level:
                self.log_security_event("access_granted", f"Доступ разрешён для {keycard['user_name']}", zone_id)
                self.access_zones[zone_id]["current_occupants"].append(keycard["user_id"])
                return True
            else:
                self.log_security_event("access_denied", f"Недостаточный уровень доступа {keycard['user_name']}", zone_id)
                raise UnauthorizedAccessException(keycard["access_level"], required_level)

        return False

    def log_security_event(self, event_type: str, description: str, zone_id: str = None) -> None:
        """Записывает событие безопасности."""
        log_entry = {
            "timestamp": datetime.now(),
            "event_type": event_type,
            "description": description,
            "zone_id": zone_id,
            "log_id": f"LOG_{len(self.security_logs):04d}"
        }
        self.security_logs.append(log_entry)

    def activate_emergency_mode(self) -> None:
        """Активирует режим чрезвычайной ситуации."""
        self.emergency_mode = True
        for zone in self.access_zones.values():
            zone["emergency_lockdown"] = True
        self.log_security_event("emergency", "Активирован режим чрезвычайной ситуации")
