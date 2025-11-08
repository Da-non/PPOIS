import random
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from game_development.core import Player, Character, GameItem, Skill
from game_development.game_mechanics import CombatSystem, InventorySystem, SkillSystem, CraftingSystem, Quest
from game_development.exceptions import InvalidGameStateException


class TestGameMechanicsExtra(unittest.TestCase):
    def test_combat_errors_and_end_conditions(self):
        c1 = Character("c10", "W", "warrior", "human")
        c2 = Character("c11", "M", "mage", "elf")
        cs = CombatSystem("cmbX")
        # attack when not active
        cs.add_participant(c1)
        cs.add_participant(c2)
        with self.assertRaises(InvalidGameStateException):
            cs.attack(c1, c2)
        cs.start_combat()
        # attacker not in participants
        outsider = Character("c12", "O", "warrior", "human")
        with self.assertRaises(ValueError):
            cs.attack(outsider, c2)
        # dead attacker
        c1.health = 0
        with self.assertRaises(ValueError):
            cs.attack(c1, c2)
        c1.health = c1.max_health
        # deterministic damage modifier
        with patch.object(random, 'uniform', return_value=1.0):
            log = cs.attack(c1, c2, attack_type="critical")
            self.assertGreater(log["damage"], 0)
        # kill target -> combat ends
        c2.health = 1
        cs.attack(c1, c2)
        self.assertEqual(cs.combat_state, "finished")

    def test_quest_requirements_and_timing(self):
        p = Player("p100", "U", "e@example.com")
        q = Quest("qq1", "Q", "desc", "side")
        q.add_objective("collect", "Collect", "herb", 1)
        # level too low
        q.requirements["level"] = 5
        self.assertFalse(q.start_quest(p))
        p.level = 5
        self.assertTrue(q.start_quest(p))
        # cannot complete yet
        self.assertFalse(q.complete_quest(p))
        q.update_objective("collect", "herb", 1)
        self.assertTrue(q.complete_quest(p))
        # time limit fail path
        q2 = Quest("qq2", "Timed", "desc", "side")
        q2.status = "active"
        q2.time_limit = datetime.now() - timedelta(seconds=1)
        q2.update(0.1)
        self.assertEqual(q2.status, "failed")

    def test_inventory_weight_and_slot_and_fit(self):
        owner = Player("pp1", "U", "e@example.com")
        inv = InventorySystem("invX", owner, max_slots=2, weight_limit=10)
        heavy = GameItem("H", "Heavy", "misc")
        heavy.weight = 50
        self.assertFalse(inv.add_item(heavy))  # too heavy
        a = GameItem("A", "A", "misc")
        a.weight = 4
        b = GameItem("B", "B", "misc")
        b.weight = 5
        self.assertTrue(inv.add_item(a))
        self.assertTrue(inv.can_fit_item(b))
        self.assertTrue(inv.add_item(b))
        c = GameItem("C", "C", "misc")
        c.weight = 1
        self.assertFalse(inv.add_item(c))  # no slots
        # try to put into specific slot beyond current len -> should fail
        inv2 = InventorySystem("inv2", owner, max_slots=3, weight_limit=100)
        self.assertTrue(inv2.add_item(a))
        self.assertTrue(inv2.add_item(b))
        self.assertFalse(inv2.add_item(c, slot=2))

    def test_skill_system_available_and_prereq(self):
        ss = SkillSystem("skX")
        p = Player("pp2", "U", "e@example.com")
        p.level = 10
        s1 = Skill("sA", "A", "combat", 1)
        s2 = Skill("sB", "B", "combat", 5)
        ss.add_skill(s1)
        ss.add_skill(s2)
        ss.add_skill_to_tree("t", "sA")
        ss.add_skill_to_tree("t", "sB")
        avail = ss.get_available_skills_for_player(p)
        ids = {s.entity_id for s in avail}
        self.assertEqual(ids, {"sA"})
        self.assertTrue(ss.learn_skill(p, "sA"))
        avail2 = ss.get_available_skills_for_player(p)
        self.assertGreaterEqual({s.entity_id for s in avail2}, {"sB"})
        self.assertTrue(ss.learn_skill(p, "sB"))

    def test_crafting_consumes_and_removes_items(self):
        cr = CraftingSystem("craftX")
        p = Player("pp3", "U", "e@example.com")
        mat = GameItem("mat", "Mat", "material")
        mat.stack_size = 10
        mat.current_stack = 3
        mat2 = GameItem("mat", "Mat", "material")
        mat2.stack_size = 10
        mat2.current_stack = 2
        p.add_item(mat)
        p.add_item(mat2)
        cr.add_recipe("r1", {"required_level": 1, "materials": {"mat": 5}, "result": {"item_id": "res", "name": "Res", "item_type": "misc"}})
        item = cr.craft_item(p, "r1")
        self.assertTrue(item)
        self.assertFalse(any(i.entity_id == "mat" and i.current_stack > 0 for i in p.inventory))


if __name__ == '__main__':
    unittest.main()
