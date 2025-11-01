"""
Юнит тесты для модуля finance.py
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к родительской директории для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oceanarium.finance import BankAccount, CreditCard
from oceanarium.exceptions import *


class TestBankAccount(unittest.TestCase):
    """Тесты для класса BankAccount"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.account = BankAccount("ACC001", "Иван Иванов", 10000.0)

    def test_account_initialization(self):
        """Тест инициализации банковского счета"""
        self.assertEqual(self.account.account_number, "ACC001")
        self.assertEqual(self.account.holder_name, "Иван Иванов")
        self.assertEqual(self.account.balance, 10000.0)
        self.assertEqual(self.account.currency, "RUB")
        self.assertEqual(self.account.account_type, "checking")
        self.assertEqual(self.account.daily_limit, 100000.0)
        self.assertEqual(self.account.daily_spent, 0.0)
        self.assertFalse(self.account.is_frozen)
        self.assertEqual(self.account.overdraft_limit, 0.0)

    def test_deposit_success(self):
        """Тест успешного пополнения счета"""
        initial_balance = self.account.balance
        result = self.account.deposit(5000.0, "Тестовое пополнение")

        self.assertTrue(result)
        self.assertEqual(self.account.balance, initial_balance + 5000.0)
        self.assertEqual(len(self.account.transactions), 1)

        transaction = self.account.transactions[0]
        self.assertEqual(transaction["type"], "deposit")
        self.assertEqual(transaction["amount"], 5000.0)

    def test_deposit_invalid_amount(self):
        """Тест пополнения на недопустимую сумму"""
        result = self.account.deposit(-1000.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 10000.0)

    def test_withdraw_success(self):
        """Тест успешного снятия денег"""
        initial_balance = self.account.balance
        result = self.account.withdraw(3000.0, "Тестовое снятие")

        self.assertTrue(result)
        self.assertEqual(self.account.balance, initial_balance - 3000.0)
        self.assertEqual(self.account.daily_spent, 3000.0)

    def test_withdraw_frozen_account(self):
        """Тест снятия с замороженного счета"""
        self.account.is_frozen = True
        result = self.account.withdraw(1000.0)
        self.assertFalse(result)

    def test_withdraw_exceeds_daily_limit(self):
        """Тест превышения дневного лимита"""
        self.account.daily_spent = 99000.0

        with self.assertRaises(InsufficientFundsException):
            self.account.withdraw(2000.0)

    def test_withdraw_insufficient_funds(self):
        """Тест недостаточности средств"""
        with self.assertRaises(InsufficientFundsException):
            self.account.withdraw(15000.0)

    def test_withdraw_with_overdraft(self):
        """Тест снятия с овердрафтом"""
        self.account.overdraft_limit = 5000.0
        result = self.account.withdraw(12000.0)

        self.assertTrue(result)
        self.assertEqual(self.account.balance, -2000.0)

    def test_transfer_success(self):
        """Тест успешного перевода"""
        target_account = BankAccount("ACC002", "Петр Петров", 5000.0)

        result = self.account.transfer(target_account, 3000.0, "Тестовый перевод")

        self.assertTrue(result)
        self.assertEqual(self.account.balance, 7000.0)
        self.assertEqual(target_account.balance, 8000.0)

    def test_transfer_insufficient_funds(self):
        """Тест перевода при недостатке средств"""
        target_account = BankAccount("ACC002", "Петр Петров", 5000.0)

        with self.assertRaises(InsufficientFundsException):
            self.account.transfer(target_account, 15000.0)

    def test_get_balance(self):
        """Тест получения баланса"""
        balance = self.account.get_balance()
        self.assertEqual(balance, 10000.0)

    def test_reset_daily_limit(self):
        """Тест сброса дневного лимита"""
        self.account.daily_spent = 5000.0
        self.account.last_reset_date = datetime.now().date() - timedelta(days=1)

        self.account.reset_daily_limit()
        self.assertEqual(self.account.daily_spent, 0.0)

    def test_add_transaction(self):
        """Тест добавления транзакции"""
        self.account.add_transaction("test", 1000.0, "Тест")

        self.assertEqual(len(self.account.transactions), 1)
        transaction = self.account.transactions[0]
        self.assertEqual(transaction["type"], "test")
        self.assertEqual(transaction["amount"], 1000.0)
        self.assertEqual(transaction["description"], "Тест")


class TestCreditCard(unittest.TestCase):
    """Тесты для класса CreditCard"""

    def setUp(self):
        """Настройка тестовых данных"""
        expiry_date = datetime.now() + timedelta(days=365)
        self.card = CreditCard("1234567890123456", "Иван Иванов", expiry_date, "123")

    def test_card_initialization(self):
        """Тест инициализации кредитной карты"""
        self.assertEqual(self.card.card_number, "1234567890123456")
        self.assertEqual(self.card.holder_name, "Иван Иванов")
        self.assertEqual(self.card.cvv, "123")
        self.assertGreaterEqual(self.card.credit_limit, 50000)
        self.assertLessEqual(self.card.credit_limit, 500000)
        self.assertEqual(self.card.current_balance, 0.0)
        self.assertTrue(self.card.is_active)
        self.assertFalse(self.card.is_blocked)

    def test_charge_success(self):
        """Тест успешного списания с карты"""
        result = self.card.charge(1000.0, "Тестовый магазин")

        self.assertTrue(result)
        self.assertEqual(self.card.current_balance, 1000.0)
        self.assertEqual(self.card.minimum_payment, 50.0)  # 5% от суммы
        self.assertEqual(len(self.card.transactions), 1)

    def test_charge_inactive_card(self):
        """Тест списания с неактивной карты"""
        self.card.is_active = False
        result = self.card.charge(1000.0, "Магазин")
        self.assertFalse(result)

    def test_charge_blocked_card(self):
        """Тест списания с заблокированной карты"""
        self.card.is_blocked = True
        result = self.card.charge(1000.0, "Магазин")
        self.assertFalse(result)

    def test_charge_expired_card(self):
        """Тест списания с просроченной карты"""
        self.card.expiry_date = datetime.now() - timedelta(days=1)

        with self.assertRaises(TicketExpiredException):
            self.card.charge(1000.0, "Магазин")

    def test_charge_exceeds_credit_limit(self):
        """Тест превышения кредитного лимита"""
        amount = self.card.credit_limit + 1000.0

        with self.assertRaises(InsufficientFundsException):
            self.card.charge(amount, "Дорогой магазин")

    def test_multiple_charges(self):
        """Тест множественных списаний"""
        self.card.charge(1000.0, "Магазин 1")
        self.card.charge(2000.0, "Магазин 2")

        self.assertEqual(self.card.current_balance, 3000.0)
        self.assertEqual(self.card.minimum_payment, 150.0)  # 5% от общей суммы
        self.assertEqual(len(self.card.transactions), 2)

    def test_transaction_details(self):
        """Тест деталей транзакции"""
        self.card.charge(1500.0, "Тестовый магазин")

        transaction = self.card.transactions[0]
        self.assertEqual(transaction["amount"], 1500.0)
        self.assertEqual(transaction["merchant"], "Тестовый магазин")
        self.assertEqual(transaction["type"], "purchase")
        self.assertIsNotNone(transaction["id"])
        self.assertIsNotNone(transaction["timestamp"])


if __name__ == '__main__':
    unittest.main()
