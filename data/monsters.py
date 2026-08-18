from dataclasses import dataclass
from core.stats import Stats


@dataclass(frozen=True)
class Monster:
    name: str
    stats: Stats
    exp_reward: int
    min_floor: int
    description: str
    sprite: str = ""

    def is_alive(self) -> bool:
        return self.stats.is_alive()

    def take_damage(self, amount: int) -> "Monster":
        return Monster(
            name=self.name, stats=self.stats.take_damage(amount),
            exp_reward=self.exp_reward, min_floor=self.min_floor,
            description=self.description, sprite=self.sprite,
        )

    def __str__(self) -> str:
        return f"{self.name} [{self.stats}]"


GOBLIN        = Monster("Goblin",           Stats.create(18, 5, 1, 6),  20, 1, "Pequeno e agil.",               "goblin.png")
GIANT_RAT     = Monster("Rato Gigante",     Stats.create(12, 4, 0, 8),  15, 1, "Morde rapido.",                 "rato_gigante.png")
SLIME         = Monster("Slime",            Stats.create(22, 3, 3, 2),  18, 1, "Gelatinoso. DEF natural.",      "slime.png")
LESSER_SKEL   = Monster("Esqueleto Menor",  Stats.create(15, 6, 2, 4),  22, 2, "Ossos animados.",               "esqueleto.png")
ZOMBIE        = Monster("Zumbi",            Stats.create(30, 7, 2, 2),  35, 3, "Lento e implacavel.",           "zumbi.png")
STONE_TROLL   = Monster("Troll das Pedras", Stats.create(45,10, 5, 3),  55, 5, "Regenera entre rodadas.",       "troll.png")
WILD_ORC      = Monster("Orc Selvagem",     Stats.create(38,11, 3, 5),  50, 5, "Ataca sem recuar.",             "orc_selvagem.png")
SPECTER       = Monster("Espectro",         Stats.create(28,13, 0,10),  60, 6, "Sem corpo. Rapido.",            "espectro.png")
SHADOW_WOLF   = Monster("Lobo das Sombras", Stats.create(32,12, 2,12),  55, 6, "Ataque surpresa.",              "lobo_sombras.png")
GARGOYLE      = Monster("Gargula",          Stats.create(42,10, 7, 4),  65, 7, "DEF alta.",                     "gargula.png")
OGRE          = Monster("Ogro",             Stats.create(55,14, 4, 2),  70, 7, "Golpes atordoam.",              "ogro.png")
CULTIST       = Monster("Cultista",         Stats.create(25,15, 1, 7),  60, 8, "Magia sombria.",                "cultista.png")
LESSER_LICH   = Monster("Lich Menor",       Stats.create(60,17, 5, 6), 120, 9, "Drena HP.",                     "lich.png")
VESTAL_DEMON  = Monster("Demonio Vestal",   Stats.create(50,18, 6, 8), 130,10, "Guarda do Arquiteto.",          "demonio.png")

MONSTERS_BY_FLOOR: dict[int, list[Monster]] = {
    1:  [GOBLIN, GIANT_RAT, SLIME],
    2:  [GOBLIN, GIANT_RAT, SLIME, LESSER_SKEL],
    3:  [LESSER_SKEL, ZOMBIE, GOBLIN, SLIME],
    4:  [LESSER_SKEL, ZOMBIE, GIANT_RAT, GOBLIN],
    5:  [STONE_TROLL, WILD_ORC, ZOMBIE, GOBLIN],
    6:  [SPECTER, SHADOW_WOLF, STONE_TROLL, WILD_ORC],
    7:  [GARGOYLE, OGRE, SPECTER, SHADOW_WOLF],
    8:  [CULTIST, GARGOYLE, OGRE, SPECTER],
    9:  [LESSER_LICH, CULTIST, GARGOYLE, OGRE],
    10: [LESSER_LICH, VESTAL_DEMON, CULTIST, SHADOW_WOLF],
}
