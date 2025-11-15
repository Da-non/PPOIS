GameEntity 8 5 → Player, Character, GameItem, Skill, Ability, ItemEffect, SkillEffect, AbilityEffect, Enchantment

Player 25 21 → Character

Character 11 6 → 

GameItem 19 11 → ItemEffect, Enchantment

Skill 14 4 → SkillEffect

Ability 12 4 → AbilityEffect

ItemEffect 8 4 → 

SkillEffect 6 3 → 

AbilityEffect 6 3 → 

Enchantment 7 3 → 

GameDesigner 10 6 → 

GameBalanceManager 5 6 → 

QualityAssuranceTester 7 5 → 

NarrativeDesigner 7 6 → 

SoundDesigner 7 5 → 

ArtDirector 8 6 → 

TechnicalArtist 8 6 → 

CommunityManager 8 7 → 

GameDevelopment 46 28 → Player, Character, GameServer, GameSession, Quest, GameItem, Skill, Ability, CombatSystem, InventorySystem, SkillSystem, CraftingSystem, Moderator, GameStatistics, GameEvent, GameAnalytics, GameCurrency, GameShop, Subscription, PaymentProcessor, GameEconomy, GameDesigner, LevelDesigner, GameBalanceManager, QualityAssuranceTester, NarrativeDesigner, SoundDesigner, ArtDirector, TechnicalArtist, CommunityManager

GameCurrency 19 7 → 

GameShop 16 9 → 

Subscription 13 6 → 

PaymentProcessor 14 7 → 

GameEconomy 13 8 → 

GameServer 18 11 → 

GameSession 13 9 → 

Moderator 12 7 → 

GameStatistics 28 19 → 

GameEvent 15 5 → 

GameAnalytics 10 5 → 

ServerCluster 12 11 → 

LoadBalancer 9 10 → 

AdminSystem 10 9 → 

Admin 16 9 → 

GameMaster 12 9 → 

SupportTicket 14 8 → 

CombatSystem 9 10 → Character, Player, GameItem, Skill

Quest 14 9 → Player, GameItem

InventorySystem 7 8 → Player, GameItem

SkillSystem 5 6 → Player, Skill

CraftingSystem 5 5 → Player, GameItem

SocialSystem 8 9 → Player, Friendship, Party

Friendship 8 3 → Player

Party 10 9 → Player, GameItem

UIManager 7 5 → GameEntity

Menu 3 5 → GameEntity

HUD 4 3 → GameEntity, Player

NotificationSystem 4 4 → GameEntity

Tooltip 4 3 → GameEntity

PvPSystem.py 8 8 → 

GameDevelopmentBaseException 0 1 →

PlayerNotFoundException 1 1 → GameDevelopmentBaseException

InsufficientGameCurrencyException 3 1 → GameDevelopmentBaseException

InvalidGameSessionException 1 1 → GameDevelopmentBaseException

ServerOverloadException 3 1 → GameDevelopmentBaseException

EquipmentMismatchException 3 1 → GameDevelopmentBaseException

UnauthorizedGameActionException 3 1 → GameDevelopmentBaseException

QuestCompletionException 2 1 → GameDevelopmentBaseException

InvalidGameStateException 2 1 → GameDevelopmentBaseException

GameAssetNotFoundException 2 1 → GameDevelopmentBaseException

PaymentProcessingException 2 1 → GameDevelopmentBaseException

GameModerationException 3 1 → GameDevelopmentBaseException

GameServerMaintenanceException 2 1 → GameDevelopmentBaseException

Итого:50 классов,13 исключений,290 полей,300 методов,72 ассоциации
