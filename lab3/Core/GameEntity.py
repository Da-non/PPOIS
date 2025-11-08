class GameEntity(ABC):
    """
    Абстрактный базовый класс для всех игровых сущностей.

    Attributes:
        entity_id (str): Уникальный идентификатор сущности
        name (str): Название сущности
        creation_date (datetime): Дата создания
        last_modified (datetime): Дата последнего изменения
    """

    def __init__(self, entity_id: str, name: str):
        self.entity_id = entity_id
        self.name = name
        self.creation_date = datetime.now()
        self.last_modified = datetime.now()
        self.is_active = True
        self.tags = []
        self.metadata = {}

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Обновляет состояние сущности."""
        pass

    def add_tag(self, tag: str) -> None:
        """Добавляет тег к сущности."""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> bool:
        """Удаляет тег у сущности."""
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    def set_metadata(self, key: str, value: Any) -> None:
        """Устанавливает метаданные."""
        self.metadata[key] = value
        self.last_modified = datetime.now()

