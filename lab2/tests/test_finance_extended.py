"""
Дополнительные тесты для модуля finance.py для повышения покрытия (исправленная версия)
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.finance import BankAccount, CreditCard, PaymentProcessor
from oceanarium.exceptions import *


class TestCreditCardExtended(unittest.TestCase):
    """Расширенные тесты для класса CreditCard"""

    def setUp(self):
        """Настройка тестовых данных"""
        expiry_date = datetime.now() + timedelta(days=365)
        self.card = CreditCard("4111111111111111", "Иван Петров", expiry_date, "123")

    def test_make_payment_success(self):
        """Тест успешного платежа по карте"""
        # Сначала создаем задолженность
        self.card.charge(1000.0, "Магазин")
        initial_balance = self.card.current_balance
        initial_minimum = self.card.minimum_payment

        result = self.card.make_payment(500.0)
        self.assertTrue(result)
        self.assertEqual(self.card.current_balance, initial_balance - 500.0)
        self.assertLess(self.card.minimum_payment, initial_minimum)

    def test_make_payment_full_balance(self):
        """Тест полного погашения долга"""
        self.card.charge(1000.0, "Магазин")
        result = self.card.make_payment(1500.0)  # Больше долга

        self.assertTrue(result)
        self.assertEqual(self.card.current_balance, 0.0)
        self.assertEqual(len([t for t in self.card.transactions if t["type"] == "payment"]), 1)

    def test_make_payment_invalid_amount(self):
        """Тест платежа с неверной суммой"""
        result = self.card.make_payment(-100.0)
        self.assertFalse(result)

    def test_block_unblock_card(self):
        """Тест блокировки и разблокировки карты"""
        self.assertFalse(self.card.is_blocked)

        self.card.block_card()
        self.assertTrue(self.card.is_blocked)

        self.card.unblock_card()
        self.assertFalse(self.card.is_blocked)

    def test_blocked_card_transaction(self):
        """Тест транзакции с заблокированной картой"""
        self.card.block_card()
        result = self.card.charge(100.0, "Попытка покупки")
        self.assertFalse(result)


class TestPaymentProcessor(unittest.TestCase):
    """Тесты для класса PaymentProcessor"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.processor = PaymentProcessor("PROC001")
        expiry_date = datetime.now() + timedelta(days=365)
        self.card = CreditCard("4111111111111111", "Тест", expiry_date, "123")

    def test_processor_initialization(self):
        """Тест инициализации процессора платежей"""
        self.assertEqual(self.processor.processor_id, "PROC001")
        self.assertIn("credit_card", self.processor.supported_methods)
        self.assertIn("cash", self.processor.supported_methods)
        self.assertEqual(self.processor.transaction_fee, 0.025)
        self.assertFalse(self.processor.maintenance_mode)

    def test_process_credit_card_payment(self):
        """Тест обработки платежа кредитной картой"""
        amount = 1000.0
        transaction = self.processor.process_payment("credit_card", amount, self.card)

        self.assertEqual(transaction["amount"], amount)
        self.assertEqual(transaction["fee"], amount * 0.025)
        self.assertEqual(transaction["method"], "credit_card")
        self.assertEqual(transaction["status"], "completed")
        self.assertEqual(len(self.processor.processed_transactions), 1)

    def test_process_cash_payment_within_limit(self):
        """Тест обработки наличного платежа в пределах лимита"""
        amount = 5000.0  # Меньше лимита 10000
        transaction = self.processor.process_payment("cash", amount)

        self.assertEqual(transaction["status"], "completed")
        self.assertEqual(transaction["method"], "cash")

    def test_maintenance_mode(self):
        """Тест режима технического обслуживания"""
        self.processor.maintenance_mode = True

        with self.assertRaises(MaintenanceModeException):
            self.processor.process_payment("cash", 100.0)

    def test_refund_payment_existing(self):
        """Тест возврата существующего платежа"""
        # Сначала создаем транзакцию
        transaction = self.processor.process_payment("cash", 1000.0)
        transaction_id = transaction["transaction_id"]

        result = self.processor.refund_payment(transaction_id)
        self.assertTrue(result)

    def test_refund_payment_nonexistent(self):
        """Тест возврата несуществующего платежа"""
        result = self.processor.refund_payment("FAKE_ID")
        self.assertFalse(result)


class TestBankAccountExtended(unittest.TestCase):
    """Расширенные тесты для класса BankAccount"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.account = BankAccount("EXT001", "Расширенный тест", 20000.0)

    def test_daily_limit_reset(self):
        """Тест сброса дневного лимита"""
        self.account.daily_spent = 5000.0
        self.account.last_reset_date = datetime.now().date() - timedelta(days=1)

        self.account.reset_daily_limit()
        self.assertEqual(self.account.daily_spent, 0.0)
        self.assertEqual(self.account.last_reset_date, datetime.now().date())

    def test_daily_limit_no_reset_same_day(self):
        """Тест отсутствия сброса в тот же день"""
        self.account.daily_spent = 5000.0
        initial_spent = self.account.daily_spent

        self.account.reset_daily_limit()
        self.assertEqual(self.account.daily_spent, initial_spent)

    def test_transaction_history(self):
        """Тест истории транзакций"""
        self.account.deposit(1000.0, "Тест 1")
        self.account.withdraw(500.0, "Тест 2")

        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[0]["type"], "deposit")
        self.assertEqual(self.account.transactions[1]["type"], "withdrawal")


if __name__ == '__main__':
    unittest.main()
