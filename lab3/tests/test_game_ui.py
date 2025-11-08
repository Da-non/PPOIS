import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import unittest
from game_development.core import Player
from game_development.game_ui import UIManager, Menu, HUD, NotificationSystem, Tooltip


class TestGameUI(unittest.TestCase):
    def test_ui_manager_register_update_unregister(self):
        ui = UIManager("ui1")
        menu = Menu("m1", "Main")
        tip = Tooltip("t1", "Hello")
        ui.register(menu)
        ui.register(tip)
        self.assertIn("m1", ui.elements)
        self.assertIn("t1", ui.elements)
        # update should call update on children (no errors expected)
        ui.update(0.1)
        ui.set_theme("dark")
        self.assertEqual(ui.theme, "dark")
        self.assertTrue(ui.unregister("m1"))
        self.assertNotIn("m1", ui.elements)

    def test_menu_add_remove_trigger(self):
        menu = Menu("m2", "Main")
        state = {"clicked": False}

        def cb():
            state["clicked"] = True
        menu.add_item("start", cb)
        self.assertTrue(menu.trigger("start"))
        self.assertTrue(state["clicked"])
        self.assertTrue(menu.remove_item("start"))
        self.assertFalse(menu.trigger("start"))

    def test_hud_snapshot_and_toggle(self):
        p = Player("p1", "User", "u@example.com")
        hud = HUD("hud1", p)
        p.health = 77
        p.mana = 33
        p.stamina = 55
        hud.update(0.1)
        snap = hud.last_snapshot
        self.assertEqual(snap["health"], 77)
        self.assertEqual(snap["mana"], 33)
        self.assertEqual(snap["level"], p.level)
        hud.toggle()
        self.assertFalse(hud.visible)
        # when hidden, update should not change snapshot
        p.health = 10
        hud.update(0.1)
        self.assertEqual(hud.last_snapshot, snap)

    def test_notifications_push_and_flush_history(self):
        ns = NotificationSystem("n1")
        ns.max_history = 3
        for i in range(6):
            ns.push(f"msg{i}")
        out1 = ns.flush(2)
        self.assertEqual(len(out1), 2)
        self.assertEqual(len(ns.queue), 4)
        out2 = ns.flush(10)
        self.assertEqual(len(out2), 4)
        self.assertEqual(len(ns.queue), 0)
        # history capped
        self.assertEqual(len(ns.history), ns.max_history)

    def test_tooltip_show_hide(self):
        tt = Tooltip("tt1", "Tip")
        tt.show("anchor42")
        self.assertTrue(tt.visible)
        self.assertEqual(tt.anchor, "anchor42")
        tt.hide()
        self.assertFalse(tt.visible)
        self.assertIsNone(tt.anchor)


if __name__ == '__main__':
    unittest.main()
