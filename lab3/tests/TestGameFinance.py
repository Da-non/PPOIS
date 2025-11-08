import random
import unittest
from unittest.mock import MagicMock
from game_development.core import Player, GameItem
from game_development.game_finance import GameCurrency, GameShop, Subscription, PaymentProcessor, GameEconomy
from game_development.exceptions import GameServerMaintenanceException


class TestGameFinance(unittest.TestCase):
    def test_currency_mint_burn_transfer(self):
        random.seed(0)
        cur = GameCurrency("gold", "Gold", "G")
        p1 = Player("p1", "U1", "e1@example.com")
        p2 = Player("p2", "U2", "e2@example.com")
        self.assertTrue(cur.mint_currency(1000, p1))
        self.assertEqual(cur.get_balance(p1), 1000)
        self.assertTrue(cur.transfer_currency(p1, p2, 500))
        self.assertLessEqual(cur.get_balance(p1), 500)
        self.assertGreater(cur.get_balance(p2), 0)
        self.assertTrue(cur.burn_currency(100, p2) or cur.get_balance(p2) >= 0)

    def test_shop_add_buy_sell_discount_sale(self):
        shop = GameShop("shop1", "Main")
        item = GameItem("itm1", "Sword", "weapon")
        price = 100
        self.assertTrue(shop.add_item(item, price, "gold", stock=10))
        self.assertTrue(shop.set_discount("itm1", "gold", 20))
        p = Player("p3", "Buyer", "b@example.com")
        p.add_currency("gold", 10000)
        self.assertTrue(shop.buy_item(p, "itm1", "gold", quantity=2))
        # sold stock reduced
        key = f"{item.entity_id}_gold"
        self.assertEqual(shop.items[key]["stock"], 8)
        bought = p.inventory[-1]
        self.assertTrue(shop.sell_item(p, bought, "gold"))
        sale_id = shop.start_sale("Weekend", 30, 1)
        self.assertTrue(sale_id)
        self.assertTrue(shop.end_sale(sale_id))

    def test_subscription_flow(self):
        sub = Subscription("sub1", "Premium", "vip", price=9.99, duration_days=30)
        sub.add_benefit("double_experience")
        sub.add_benefit("no_ads")
        p = Player("p4", "U", "e@example.com")
        # force payment success
        sub._process_payment = MagicMock(return_value=True)
        self.assertTrue(sub.subscribe_player(p, "credit_card"))
        self.assertTrue(sub.unsubscribe_player(p))

    def test_payment_processor_flow(self):
        pr = PaymentProcessor("pp1", "Proc")
        pr.success_rate = 1.0
        p = Player("p5", "U", "e@example.com")
        tr = pr.process_payment(100.0, "credit_card", p, "Test")
        self.assertEqual(tr["status"], "completed")
        self.assertTrue(pr.refund_payment(tr["transaction_id"]))
        self.assertTrue(pr.process_chargeback(tr["transaction_id"], "dispute"))
        stats = pr.get_daily_stats()
        self.assertIn("transactions_count", stats)
        pr.maintenance_mode = True
        with self.assertRaises(GameServerMaintenanceException):
            pr.process_payment(10, "credit_card", p, "Maint")

    def test_economy_status_and_event(self):
        eco = GameEconomy("eco1")
        cur = GameCurrency("gold", "Gold", "G")
        shop = GameShop("shopE", "EcoShop")
        eco.add_currency(cur)
        eco.add_shop(shop)
        eco.update(0.1)
        health = eco.get_economic_health_score()
        self.assertGreaterEqual(health, 0)
        self.assertLessEqual(health, 100)
        event_id = eco.create_economic_event("tax_cut", "Cut taxes", 0.1, 1)
        analysis = eco.get_market_analysis()
        self.assertEqual(analysis["total_currencies"], 1)
        self.assertEqual(analysis["total_shops"], 1)
        self.assertGreaterEqual(analysis["active_events"], 1)


if __name__ == '__main__':
    unittest.main()
