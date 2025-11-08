import unittest
from game_development.exceptions import (
    GameDevelopmentBaseException,
    PlayerNotFoundException,
    InsufficientGameCurrencyException,
    InvalidGameSessionException,
    ServerOverloadException,
    EquipmentMismatchException,
    UnauthorizedGameActionException,
    QuestCompletionException,
    InvalidGameStateException,
    GameAssetNotFoundException,
    PaymentProcessingException,
    GameModerationException,
    GameServerMaintenanceException,
)


class TestExceptions(unittest.TestCase):
    def test_all_custom_exceptions_messages(self):
        with self.assertRaises(PlayerNotFoundException) as cm:
            raise PlayerNotFoundException("p1")
        self.assertIn("Игрок с ID p1 не найден", str(cm.exception))

        with self.assertRaises(InsufficientGameCurrencyException) as cm:
            raise InsufficientGameCurrencyException(100, 50, "gold")
        self.assertIn("Недостаточно gold", str(cm.exception))

        with self.assertRaises(InvalidGameSessionException) as cm:
            raise InvalidGameSessionException("s1")
        self.assertIn("Неверная игровая сессия s1", str(cm.exception))

        with self.assertRaises(ServerOverloadException) as cm:
            raise ServerOverloadException("srv", 101, 100)
        self.assertIn("Сервер srv перегружен", str(cm.exception))

        with self.assertRaises(EquipmentMismatchException) as cm:
            raise EquipmentMismatchException("Sword", "mage", "warrior")
        self.assertIn("Оборудование Sword несовместимо", str(cm.exception))

        with self.assertRaises(UnauthorizedGameActionException) as cm:
            raise UnauthorizedGameActionException("equip", 10, 5)
        self.assertIn("Недостаточный уровень для действия equip", str(cm.exception))

        with self.assertRaises(QuestCompletionException) as cm:
            raise QuestCompletionException("q1", "bug")
        self.assertIn("Ошибка выполнения квеста q1", str(cm.exception))

        with self.assertRaises(InvalidGameStateException) as cm:
            raise InvalidGameStateException("bad", "good")
        self.assertIn("Недопустимое состояние игры", str(cm.exception))

        with self.assertRaises(GameAssetNotFoundException) as cm:
            raise GameAssetNotFoundException("a1", "texture")
        self.assertIn("Игровой ресурс texture с ID a1 не найден", str(cm.exception))

        with self.assertRaises(PaymentProcessingException) as cm:
            raise PaymentProcessingException("t1", "declined")
        self.assertIn("Ошибка обработки платежа", str(cm.exception))

        with self.assertRaises(GameModerationException) as cm:
            raise GameModerationException("p2", "spam", 2)
        self.assertIn("Нарушение правил игроком p2", str(cm.exception))

        with self.assertRaises(GameServerMaintenanceException) as cm:
            raise GameServerMaintenanceException("srv2", "tomorrow")
        self.assertIn("Сервер srv2 на техническом обслуживании", str(cm.exception))


if __name__ == '__main__':
    unittest.main()
