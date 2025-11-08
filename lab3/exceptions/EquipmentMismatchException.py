class EquipmentMismatchException(GameDevelopmentBaseException):
    """Исключение при несовместимости игрового оборудования."""
    def __init__(self, equipment_name, required_class, player_class):
        self.equipment_name = equipment_name
        self.required_class = required_class
        self.player_class = player_class
        super().__init__(f"Оборудование {equipment_name} несовместимо: требуется {required_class}, у игрока {player_class}")
