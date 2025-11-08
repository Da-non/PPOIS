import random
import unittest
from datetime import datetime, timedelta
from game_development.game_development import (
    GameDevelopment, GameDesigner, LevelDesigner, GameBalanceManager, 
    QualityAssuranceTester, NarrativeDesigner, SoundDesigner, 
    ArtDirector, TechnicalArtist, CommunityManager
)
from game_development.core import Player, GameItem, Character


class TestGameDevelopmentExtended(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gd = GameDevelopment("TestWorld")
        self.server = self.gd.servers["MAIN_SERVER"]
        self.server.start_server()
        self.player = self.gd.register_player("TestUser", "test@example.com", "password")
        self.character = self.gd.create_character(self.player, "TestHero", "mage", "elf")

    def test_game_designer_functionality(self):
        """Тестирование функциональности геймдизайнера"""
        designer = self.gd.designers["lead_designer"]
        
        # Создание дизайна квеста
        quest_design = designer.create_quest_design(
            "test_quest", 
            "Test Quest", 
            "A test quest for testing",
            [{"type": "kill", "target": "goblin", "amount": 5, "difficulty": 2}],
            {"experience": 1000, "currency": {"gold": 500}}
        )
        
        self.assertEqual(quest_design["quest_id"], "test_quest")
        self.assertIn("test_quest", designer.designed_quests)
        self.assertIn("balance_score", quest_design)
        
        # Создание дизайна предмета
        item_design = designer.create_item_design(
            "test_sword",
            "Test Sword",
            "weapon",
            {"damage": 25, "speed": 1.2},
            "rare"
        )
        
        self.assertEqual(item_design["item_id"], "test_sword")
        self.assertIn("test_sword", designer.designed_items)
        self.assertGreater(item_design["power_level"], 0)
        
        # Предложение баланса
        proposal_id = designer.propose_balance_change(
            "class", "warrior", 
            {"strength": -2, "health": +20}, 
            "Warrior is too strong in PvP"
        )
        
        self.assertTrue(proposal_id.startswith("balance_"))
        self.assertEqual(len(designer.balance_proposals), 1)

    def test_level_designer_functionality(self):
        """Тестирование функциональности дизайнера уровней"""
        level_designer = self.gd.level_designers["main_level_designer"]
        
        # Создание уровня
        level_design = level_designer.create_level(
            "test_level",
            "Test Dungeon",
            "dungeon",
            (100, 100),
            {"terrain_type": "cave", "difficulty": "medium"}
        )
        
        self.assertEqual(level_design["level_id"], "test_level")
        self.assertIn("test_level", level_designer.designed_levels)
        
        # Добавление точек спавна
        self.assertTrue(level_designer.add_spawn_point(
            "test_level", "player", (10.0, 5.0, 0.0), (0.0, 0.0, 0.0)
        ))
        
        self.assertTrue(level_designer.add_spawn_point(
            "test_level", "enemy", (20.0, 15.0, 0.0), (0.0, 90.0, 0.0)
        ))
        
        self.assertEqual(len(level_designer.level_templates["test_level"]["spawn_points"]), 2)
        
        # Генерация навигационной сетки
        nav_mesh = level_designer.generate_navigation_mesh("test_level", 0.5)
        self.assertEqual(nav_mesh["level_id"], "test_level")
        self.assertIn("test_level", level_designer.navigation_meshes)
        
        # Оптимизация производительности
        optimization_report = level_designer.optimize_level_performance("test_level")
        self.assertIn("performance_gain", optimization_report)
        self.assertIn("original_polycount", optimization_report)

    def test_game_balance_manager_functionality(self):
        """Тестирование функциональности менеджера баланса"""
        balance_manager = self.gd.balance_managers["main_balance_manager"]
        
        # Сбор данных баланса
        balance_manager.collect_balance_data(self.gd)
        
        # Проверка метрик
        self.assertIn("class_win_rates", balance_manager.monitored_metrics)
        self.assertIn("item_usage_stats", balance_manager.monitored_metrics)
        
        # Принудительная проверка баланса
        balance_manager._check_game_balance()
        
        # Проверка создания патчей баланса
        issues = [{
            "type": "class_imbalance",
            "target": "warrior",
            "current_win_rate": 0.7,
            "suggested_adjustment": "adjust_class_stats"
        }]
        
        patch_id = balance_manager._create_balance_patch(issues)
        self.assertTrue(patch_id.startswith("balance_patch_"))
        self.assertEqual(len(balance_manager.balance_patches), 1)

    def test_quality_assurance_tester_functionality(self):
        """Тестирование функциональности тестировщика качества"""
        qa_tester = self.gd.qa_testers["lead_tester"]
        
        # Создание тест-кейсов
        test_case = qa_tester.create_test_case(
            "TC001",
            "combat",
            "Test basic combat mechanics",
            ["Attack enemy", "Use skill", "Check damage"],
            "Enemy takes correct damage"
        )
        
        self.assertEqual(test_case["case_id"], "TC001")
        self.assertEqual(test_case["status"], "not_tested")
        
        # Выполнение тест-кейса (успешное)
        result = qa_tester.execute_test_case("TC001", "Enemy takes correct damage")
        self.assertEqual(result["status"], "passed")
        
        # Выполнение тест-кейса (неуспешное)
        test_case2 = qa_tester.create_test_case(
            "TC002",
            "ui",
            "Test inventory UI",
            ["Open inventory", "Drag item", "Check position"],
            "Item moves correctly"
        )
        
        result2 = qa_tester.execute_test_case("TC002", "Item disappears")
        self.assertEqual(result2["status"], "failed")
        
        # Проверка создания баг-репортов
        self.assertEqual(len(qa_tester.found_bugs), 1)
        self.assertEqual(qa_tester.found_bugs[0]["title"], "Test case TC002 failed")
        
        # Тест производительности
        perf_report = qa_tester.performance_test(self.gd)
        self.assertIn("average_frame_rate", perf_report)
        self.assertIn("meets_standards", perf_report)

    def test_narrative_designer_functionality(self):
        """Тестирование функциональности нарративного дизайнера"""
        narrative_designer = self.gd.narrative_designers["lead_writer"]
        
        # Создание предыстории персонажа
        backstory = narrative_designer.create_character_backstory(
            "test_char",
            "Born in a small village, trained as a mage",
            ["intelligent", "curious", "reserved"],
            ["seek knowledge", "protect the innocent"]
        )
        
        self.assertEqual(backstory["character_id"], "test_char")
        self.assertIn("test_char", narrative_designer.character_backstories)
        
        # Написание нарратива квеста
        quest_narrative = narrative_designer.write_quest_narrative(
            "story_quest",
            "Welcome to our village, stranger...",
            "You have proven yourself worthy!",
            {"old_man": "The crystals are in danger!", "mayor": "Thank you for saving us!"}
        )
        
        self.assertEqual(quest_narrative["quest_id"], "story_quest")
        self.assertIn("story_quest", narrative_designer.written_quests)
        
        # Добавление лора мира
        lore = narrative_designer.add_world_lore(
            "ancient_empire",
            "The Fallen Empire",
            "Once a great civilization that fell due to magical catastrophe",
            "history"
        )
        
        self.assertEqual(lore["lore_id"], "ancient_empire")
        self.assertIn("ancient_empire", narrative_designer.world_lore)
        
        # Создание дерева диалогов
        dialogue_tree = narrative_designer.create_dialogue_tree(
            "merchant_npc",
            [
                {"text": "Welcome to my shop!", "responses": ["Browse", "Leave"]},
                {"text": "Fine goods for fine adventurers!", "responses": ["Buy", "Sell", "Leave"]}
            ]
        )
        
        self.assertEqual(dialogue_tree["npc_id"], "merchant_npc")
        self.assertIn("merchant_npc", narrative_designer.dialogue_trees)

    def test_sound_designer_functionality(self):
        """Тестирование функциональности звукового дизайнера"""
        sound_designer = self.gd.sound_designers["lead_sound"]
        
        # Создание звуковых эффектов
        sound_effect = sound_designer.create_sound_effect(
            "sword_swing",
            "Sword Swing",
            "weapon",
            "/sounds/weapons/sword_swing.wav",
            1.5
        )
        
        self.assertEqual(sound_effect["sound_id"], "sword_swing")
        self.assertIn("sword_swing", sound_designer.created_sounds)
        
        # Добавление фоновой музыки
        music_track = sound_designer.add_background_music(
            "forest_theme",
            "Forest Ambience",
            "John Composer",
            "/music/forest_theme.ogg",
            180.0,
            "peaceful"
        )
        
        self.assertEqual(music_track["track_id"], "forest_theme")
        self.assertEqual(len(sound_designer.background_music), 1)
        
        # Запись озвучки
        voice_over = sound_designer.record_voice_over(
            "npc_greeting",
            "merchant_01",
            [{"text": "Welcome traveler!", "emotion": "friendly"}],
            "Anna Voiceactor"
        )
        
        self.assertEqual(voice_over["voice_id"], "npc_greeting")
        self.assertIn("npc_greeting", sound_designer.voice_overs)
        
        # Создание аудио-микса
        audio_mix = sound_designer.create_audio_mix(
            "main_mix",
            {
                "master_volume": 0.9,
                "music_volume": 0.7,
                "sfx_volume": 1.0,
                "voice_volume": 0.8
            }
        )
        
        self.assertEqual(audio_mix["mix_id"], "main_mix")
        self.assertIn("main_mix", sound_designer.audio_mix)

    def test_art_director_functionality(self):
        """Тестирование функциональности арт-директора"""
        art_director = self.gd.art_directors["lead_art"]
        
        # Установка арт-стиля
        art_director.set_art_style("stylized", "Colorful and exaggerated proportions")
        self.assertEqual(art_director.art_style, "stylized")
        self.assertIn("art_style", art_director.visual_guides)
        
        # Создание визуального гайда
        visual_guide = art_director.create_visual_guide(
            "character_design",
            "Character Design Guide",
            {
                "proportions": "7.5 heads tall",
                "color_palette": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
                "style_notes": "Exaggerated features, bold outlines"
            }
        )
        
        self.assertEqual(visual_guide["guide_id"], "character_design")
        self.assertIn("character_design", art_director.visual_guides)
        
        # Одобрение ассетов
        approval = art_director.approve_asset(
            "sword_01",
            "weapon",
            "artist_john",
            0.85
        )
        
        self.assertEqual(approval["asset_id"], "sword_01")
        self.assertIn("sword_01", art_director.approved_assets)
        self.assertTrue(approval["meets_style_guide"])
        
        # Создание цветовой палитры
        color_palette = art_director.create_color_palette(
            "forest_theme",
            {
                "primary": "#2E8B57",
                "secondary": "#8FBC8F", 
                "accent": "#FFD700"
            },
            "natural"
        )
        
        self.assertEqual(color_palette["palette_id"], "forest_theme")
        self.assertIn("forest_theme", art_director.color_palettes)
        
        # Ревью качества арта
        assets = [
            {"id": "asset_01", "type": "character", "artist": "artist1"},
            {"id": "asset_02", "type": "environment", "artist": "artist2"},
            {"id": "asset_03", "type": "prop", "artist": "artist3"}
        ]
        
        review_report = art_director.review_art_quality(assets)
        self.assertIn("total_assets", review_report)
        self.assertIn("average_quality_score", review_report)
        self.assertIn("issues_found", review_report)

    def test_technical_artist_functionality(self):
        """Тестирование функциональности технического художника"""
        tech_artist = self.gd.technical_artists["lead_tech_art"]
        
        # Создание шейдера
        shader = tech_artist.create_shader(
            "water_shader",
            "Water Shader",
            "surface",
            "void surf() { /* shader code */ }",
            {"wave_speed": 1.0, "transparency": 0.8}
        )
        
        self.assertEqual(shader["shader_id"], "water_shader")
        self.assertIn("water_shader", tech_artist.created_shaders)
        
        # Создание визуального эффекта
        vfx_effect = tech_artist.create_vfx_effect(
            "fireball_vfx",
            "Fireball Effect",
            "magic",
            3.0,
            {"particle_count": 500, "color": "#FF4500"}
        )
        
        self.assertEqual(vfx_effect["vfx_id"], "fireball_vfx")
        self.assertIn("fireball_vfx", tech_artist.vfx_effects)
        
        # Разработка инструмента оптимизации
        tool = tech_artist.develop_optimization_tool(
            "texture_compressor",
            "Texture Compressor",
            "Reduce texture size without quality loss",
            35.0
        )
        
        self.assertEqual(tool["tool_id"], "texture_compressor")
        self.assertEqual(len(tech_artist.optimization_tools), 1)
        
        # Создание системы риггинга
        rigging_system = tech_artist.create_rigging_system(
            "humanoid_rig",
            "human",
            54,
            {
                "ik_controls": True,
                "facial_rig": True,
                "finger_controls": True
            }
        )
        
        self.assertEqual(rigging_system["rig_id"], "humanoid_rig")
        self.assertIn("humanoid_rig", tech_artist.rigging_systems)
        
        # Оптимизация ассетов
        assets_to_optimize = [
            {"size_mb": 25.0},
            {"size_mb": 40.0},
            {"size_mb": 15.0}
        ]
        
        optimization_report = tech_artist.optimize_assets(assets_to_optimize)
        self.assertIn("reduction_percentage", optimization_report)
        self.assertIn("performance_improvement", optimization_report)
        self.assertGreater(optimization_report["reduction_percentage"], 0)

    def test_community_manager_functionality(self):
        """Тестирование функциональности менеджера сообщества"""
        community_manager = self.gd.community_managers["lead_community"]
        
        # Организация мероприятия
        event = community_manager.organize_community_event(
            "summer_tournament",
            "Summer Tournament 2024",
            "tournament",
            datetime.now() + timedelta(days=7),
            48
        )
        
        self.assertEqual(event["event_id"], "summer_tournament")
        self.assertEqual(len(community_manager.community_events), 1)
        
        # Сбор обратной связи
        feedback = community_manager.collect_player_feedback(
            "FB001",
            "player_123",
            "gameplay",
            "Combat feels too slow in early game",
            3
        )
        
        self.assertEqual(feedback["feedback_id"], "FB001")
        self.assertIn("FB001", community_manager.feedback_reports)
        
        # Создание отчета по сообществу
        report = community_manager.create_community_report("weekly_001", "weekly")
        
        self.assertEqual(report["report_id"], "weekly_001")
        self.assertIn("average_sentiment", report)
        self.assertIn("top_issues", report)
        self.assertIn("recommendations", report)
        
        # Проверка приоритетов обратной связи
        self.assertEqual(community_manager._calculate_feedback_priority("bugs", 1), "high")
        self.assertEqual(community_manager._calculate_feedback_priority("performance", 4), "medium")
        self.assertEqual(community_manager._calculate_feedback_priority("suggestions", 5), "low")

    def test_integrated_development_workflow(self):
        """Тестирование интегрированного рабочего процесса разработки"""
        
        # Геймдизайнер создает контент
        designer = self.gd.designers["lead_designer"]
        quest_design = designer.create_quest_design(
            "integrated_quest", "Integrated Quest", "Test integrated workflow",
            [{"type": "collect", "target": "artifact", "amount": 3, "difficulty": 3}],
            {"experience": 1500, "currency": {"gold": 750}}
        )
        
        # Нарративный дизайнер добавляет историю
        narrative = self.gd.narrative_designers["lead_writer"]
        narrative.write_quest_narrative(
            "integrated_quest",
            "The ancient artifacts hold great power...",
            "You have collected all the artifacts!",
            {"wise_man": "Be careful with these powerful items!"}
        )
        
        # Арт-директор одобряет ассеты для квеста
        art_dir = self.gd.art_directors["lead_art"]
        art_dir.approve_asset("artifact_model", "prop", "artist_sarah", 0.9)
        
        # Тестировщик проверяет квест
        qa = self.gd.qa_testers["lead_tester"]
        test_case = qa.create_test_case(
            "QC_INT_001", 
            "quests", 
            "Test integrated quest completion",
            ["Accept quest", "Collect 3 artifacts", "Return to NPC"],
            "Quest completes successfully"
        )
        
        result = qa.execute_test_case("QC_INT_001", "Quest completes successfully")
        self.assertEqual(result["status"], "passed")
        
        # Менеджер баланса проверяет награды
        balance_mgr = self.gd.balance_managers["main_balance_manager"]
        balance_mgr.collect_balance_data(self.gd)
        
        # Обновление всей системы
        self.gd.update_system(1.0)
        
        # Проверка, что все специалисты обновились
        self.assertGreater(designer.creativity_score, 0)
        self.assertGreater(narrative.writing_style, "")
        self.assertGreater(art_dir.art_style, "")
        self.assertGreaterEqual(qa.bugs_fixed, 0)

    def test_game_development_comprehensive_flow(self):
        """Комплексный тест всего игрового цикла с новым функционалом"""
        
        # Базовый игровой цикл
        session = self.gd.start_game_session(self.player, "MAIN_SERVER")
        session.add_action("explore", {"area": "forest"})
        session.add_experience(200)
        
        # Использование навыков
        skill_id = next(iter(self.gd.skills.keys()))
        self.gd.learn_skill(self.player, skill_id)
        self.gd.use_skill(self.player, skill_id, self.character)
        
        # Завершение сессии
        result = self.gd.end_game_session(session.entity_id)
        self.assertGreater(result["experience_gained"], 0)
        
        # Проверка работы команды разработки после игрового процесса
        community_mgr = self.gd.community_managers["lead_community"]
        community_mgr.collect_player_feedback(
            "POST_SESSION_001",
            self.player.entity_id,
            "gameplay", 
            "Great session! Combat feels smooth.",
            5
        )
        
        # Создание отчета сообщества
        report = community_mgr.create_community_report("post_session", "daily")
        self.assertIn("average_sentiment", report)
        
        # Проверка экономики
        economy_status = self.gd.get_economy_status()
        self.assertIn("gdp", economy_status)
        
        # Полный системный отчет
        daily_report = self.gd.get_daily_report()
        self.assertIn("active_players", daily_report)
        self.assertIn("economy_health", daily_report)
        
        # Выключение системы
        shutdown_report = self.gd.shutdown_system()
        self.assertEqual(self.gd.system_status, "offline")
        self.assertIn("total_players", shutdown_report)


if __name__ == '__main__':
    unittest.main(verbosity=2)