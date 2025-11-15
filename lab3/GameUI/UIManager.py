class UIManager(GameEntity):
    """Менеджер UI, регистрирующий и обновляющий элементы интерфейса."""

    def __init__(self, manager_id: str):
        super().__init__(manager_id, "UIManager")
        self.elements: Dict[str, GameEntity] = {}
        self.theme: str = "light"
        self.scale: float = 1.0
        self.focused_element: Optional[str] = None

    def update(self, delta_time: float) -> None:
        """Обновляет все зарегистрированные UI-элементы"""
        for element in self.elements.values():
            element.update(delta_time)

    def register(self, element: GameEntity) -> None:
        """Регистрирует новый UI-элемент в менеджере"""
        self.elements[element.entity_id] = element

    def unregister(self, element_id: str) -> bool:
        """Удаляет UI-элемент из менеджера"""
        return self.elements.pop(element_id, None) is not None

    def set_theme(self, theme: str) -> None:
        """Устанавливает тему интерфейса"""
        self.theme = theme
