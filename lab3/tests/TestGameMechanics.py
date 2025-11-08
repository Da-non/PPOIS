import random
import unittest
from game_development.core import Player, Character, GameItem, Skill
from game_development.game_mechanics import CombatSystem, InventorySystem, SkillSystem, CraftingSystem, Quest
from game_development.exceptions import InvalidGameStateException


class TestGameMechanics(unittest.TestCase):
    def test_combat_system_basic_flow(self):
        random.seed(0)
        c1 = Character("c1", "War", "warrior", "human")
        c2 = Character("c2", "Mage", "mage", "elf")
        cs = CombatSystem("cmb1")
        self.assertTrue(cs.add_participant(c1))
        self.assertTrue(cs.add_participant(c2))
        cs.start_combat()
        current = cs.get_current_character()
        self.assertIn(current, [c1, c2])
        # add a free skill to caster and use
        s = Skill("s1", "Zap", "magic", required_level=1)
        s.mana_cost = 0
        c1.learn_skill(s)
        log = cs.use_skill(c1, c2, "s1")
        self.assertTrue(log["success"])
        atk = cs.attack(c1, c2)
        self.assertGreater(atk["damage"], 0)
        cs.next_turn()
        self.assertIn(cs.get_current_character(), [c1, c2])
        cs.end_combat()
        self.assertEqual(cs.combat_state, "finished")

    def test_combat_system_errors(self):
        cs = CombatSystem("cmb2")
        c1 = Character("c3", "Solo", "warrior", "human")
        cs.add_participant(c1)
        with self.assertRaises(InvalidGameStateException):
            cs.start_combat()

    def test_inventory_system_add_remove_sort_and_queries(self):
        owner = Player("p1", "U", "e@example.com")
        inv = InventorySystem("inv1", owner, max_slots=5, weight_limit=100)
        w1 = GameItem("w1", "Axe", "weapon")
        w1.weight = 10
        w1.value = 100
        w2 = GameItem("w2", "Bow", "weapon")
        w2.weight = 5
        w2.value = 50
        a1 = GameItem("a1", "Armor", "armor")
        a1.weight = 20
        a1.value = 200
        self.assertTrue(inv.add_item(w1))
        self.assertTrue(inv.add_item(w2))
        self.assertTrue(inv.add_item(a1))
        self.assertEqual(len(inv.get_items_by_type("weapon")), 2)
        inv.sort_inventory("value")
        self.assertGreaterEqual(inv.items[0].value, inv.items[1].value)
        total_weight = inv.get_inventory_weight()
        self.assertEqual(total_weight, w1.weight + w2.weight + a1.weight)
        self.assertTrue(inv.remove_item(w2))

    def test_skill_system_learn_and_progression(self):
        ss = SkillSystem("sk_sys")
        p = Player("p2", "U", "e@example.com")
        p.level = 10
        s1 = Skill("sk_basic", "Basic", "combat", required_level=1)
        s2 = Skill("sk_mid", "Mid", "combat", required_level=5)
        ss.add_skill(s1)
        ss.add_skill(s2)
        ss.add_skill_to_tree("combat", "sk_basic")
        ss.add_skill_to_tree("combat", "sk_mid")
        self.assertTrue(ss.learn_skill(p, "sk_basic"))
        self.assertTrue(ss.learn_skill(p, "sk_mid"))
        prog = ss.get_skill_progression(p, "sk_mid")
        self.assertEqual(prog["level"], 1)
        self.assertEqual(prog["max_level"], 100)

    def test_crafting_system_with_materials(self):
        cr = CraftingSystem("craft")
        p = Player("p3", "U", "e@example.com")
        mat = GameItem("herb", "Herb", "material")
        mat.stack_size = 20
        mat.current_stack = 10
        p.add_item(mat)
        cr.add_recipe("potion", {
            "required_level": 1,
            "materials": {"herb": 5},
            "result": {"item_id": "potion_health", "name": "Potion", "item_type": "consumable"}
        })
        self.assertTrue(cr.can_craft(p, "potion"))
        item = cr.craft_item(p, "potion")
        self.assertTrue(item)
        self.assertEqual(item.entity_id, "potion_health")
        # materials consumed
        self.assertTrue(mat.current_stack == 5 or not any(i.entity_id == "herb" and i.current_stack > 0 for i in p.inventory))

    def test_quest_flow(self):
        q = Quest("q1", "Test", "desc", "tutorial")
        p = Player("p4", "U", "e@example.com")
        q.add_objective("kill", "Kill rats", "rat", 2)
        self.assertTrue(q.start_quest(p))
        self.assertTrue(q.update_objective("kill", "rat", 1))
        self.assertTrue(q.update_objective("kill", "rat", 1))
        self.assertTrue(q.complete_quest(p))


if __name__ == '__main__':
    unittest.main()
