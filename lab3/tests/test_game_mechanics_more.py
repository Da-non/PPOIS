import unittest
from game_development.core import Player, Character, GameItem, Skill
from game_development.game_mechanics import CombatSystem, InventorySystem, SkillSystem, CraftingSystem, Quest


class TestGameMechanicsMore(unittest.TestCase):
    def test_combat_turns_remove_and_current_character_states(self):
        c1 = Character("cm1", "A", "warrior", "human")
        c2 = Character("cm2", "B", "rogue", "elf")
        cs = CombatSystem("cmb-turns")
        # not active -> no current character
        self.assertIsNone(cs.get_current_character())
        cs.add_participant(c1)
        cs.add_participant(c2)
        cs.start_combat()
        first = cs.get_current_character()
        cs.next_turn()
        _ = cs.get_current_character()
        # go through a full round
        cs.next_turn()
        self.assertGreaterEqual(cs.round_number, 2)
        # remove participant during combat
        self.assertTrue(cs.remove_participant(c2))
        cs.end_combat()

    def test_combat_use_skill_insufficient_mana(self):
        c1 = Character("cm3", "Mage", "mage", "elf")
        c2 = Character("cm4", "Dummy", "warrior", "human")
        s = Skill("big", "BigSpell", "magic", required_level=1)
        s.mana_cost = 10000
        c1.learn_skill(s)
        cs = CombatSystem("cmb-skill")
        cs.add_participant(c1)
        cs.add_participant(c2)
        cs.start_combat()
        with self.assertRaises(ValueError):
            cs.use_skill(c1, c2, "big")

    def test_inventory_get_by_id_and_sort_variants(self):
        owner = Player("pi1", "U", "e@example.com")
        inv = InventorySystem("inv-sort", owner)
        a = GameItem("ia", "Alpha", "weapon")
        a.value = 10
        b = GameItem("ib", "Beta", "armor")
        b.value = 20
        c = GameItem("ic", "Gamma", "weapon")
        c.value = 5
        inv.add_item(a)
        inv.add_item(b)
        inv.add_item(c)
        self.assertIs(inv.get_item_by_id("ib"), b)
        self.assertIsNone(inv.get_item_by_id("xx"))
        inv.sort_inventory("type")
        self.assertLessEqual(inv.items[0].item_type, inv.items[-1].item_type)
        inv.sort_inventory("name")
        self.assertLessEqual(inv.items[0].name, inv.items[-1].name)

    def test_skill_progression_not_learned_and_requirements(self):
        ss = SkillSystem("sk-more")
        p = Player("ps1", "U", "e@example.com")
        p.level = 3
        s = Skill("s-more", "More", "craft", required_level=1)
        ss.add_skill(s)
        prog = ss.get_skill_progression(p, "s-more")
        self.assertEqual(prog["level"], 0)
        self.assertEqual(prog["progress"], 0)
        # prereq tree prevents learning until previous learned
        s2 = Skill("s2", "Two", "craft", required_level=1)
        ss.add_skill(s2)
        ss.add_skill_to_tree("craft", "s-more")
        ss.add_skill_to_tree("craft", "s2")
        self.assertFalse(ss.learn_skill(p, "s2"))  # s-more must be learned first

    def test_crafting_skill_requirement_levels(self):
        cr = CraftingSystem("craft-more")
        p = Player("pc1", "U", "e@example.com")
        s = Skill("smith", "Smith", "craft", required_level=1)
        p.learn_skill(s)
        # requires skill level 3 -> currently 1 so cannot craft
        cr.add_recipe("blade", {
            "required_level": 1,
            "required_skills": {"smith": 3},
            "materials": {},
            "result": {"item_id": "blade", "name": "Blade", "item_type": "weapon"}
        })
        self.assertFalse(cr.can_craft(p, "blade"))
        s.gain_experience(300)  # level up skill
        self.assertTrue(cr.can_craft(p, "blade"))

    def test_quest_class_requirement_and_statuses(self):
        p = Player("pq1", "U", "e@example.com")
        p.character_class = "warrior"
        q = Quest("q-more", "More", "desc", "side")
        q.requirements["class"] = "mage"
        self.assertFalse(q.start_quest(p))
        # change class to satisfy requirement
        p.character_class = "mage"
        self.assertTrue(q.start_quest(p))
        # wrong status blocks start
        self.assertFalse(q.start_quest(p))
        q.fail_quest(p)
        self.assertEqual(q.status, "failed")
        # update_objective for nonexistent should be False
        self.assertFalse(q.update_objective("collect", "x", 1))


if __name__ == '__main__':
    unittest.main()
