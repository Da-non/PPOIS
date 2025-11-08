class GameAssetNotFoundException(GameDevelopmentBaseException):
    """Исключение при попытке найти несуществующий игровой ресурс."""
    def __init__(self, asset_id, asset_type):
        self.asset_id = asset_id
        self.asset_type = asset_type
        super().__init__(f"Игровой ресурс {asset_type} с ID {asset_id} не найден")
