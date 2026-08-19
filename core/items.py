from dataclasses import dataclass
from enum import Enum


class ItemSlot(Enum):
    WEAPON = "Arma"
    ARMOR = "Armadura"
    HELMET = "Capacete"
    BOOTS = "Botas"
    RING = "Anel"


class Rarity(Enum):
    COMMON = "Comum"
    UNCOMMON = "Incomum"
    RARE = "Raro"
    EPIC = "Epico"

    def color_tag(self) -> str:
        colors = {
            Rarity.COMMON:   "[CINZA]",
            Rarity.UNCOMMON: "[VERDE]",
            Rarity.RARE:     "[AZUL] ",
            Rarity.EPIC:     "[ROXO] ",
        }
        return colors[self]

    def stars(self) -> str:
        stars = {
            Rarity.COMMON:   "★",
            Rarity.UNCOMMON: "★★",
            Rarity.RARE:     "★★★",
            Rarity.EPIC:     "★★★★",
        }
        return stars[self]


@dataclass(frozen=True)
class Item:
    name: str
    slot: ItemSlot
    rarity: Rarity
    hp_bonus: int
    atk_bonus: int
    defense_bonus: int
    speed_bonus: int
    description: str
    mana_bonus: int = 0
    upgrade_level: int = 0
    sprite: str = ""

    def upgrade_cost(self) -> int:
        return 15 + self.upgrade_level * 15

    def upgraded(self) -> "Item":
        bonus = 2
        level = self.upgrade_level + 1
        base_name = self.name.split(" +")[0]
        return Item(
            name=f"{base_name} +{level}",
            slot=self.slot,
            rarity=self.rarity,
            hp_bonus=self.hp_bonus + (bonus if self.hp_bonus > 0 else 0),
            atk_bonus=self.atk_bonus + (bonus if self.atk_bonus > 0 else 0),
            defense_bonus=self.defense_bonus + (bonus if self.defense_bonus > 0 else 0),
            speed_bonus=self.speed_bonus + (bonus if self.speed_bonus > 0 else 0),
            mana_bonus=self.mana_bonus + (bonus if self.mana_bonus > 0 else 0),
            upgrade_level=level,
            description=self.description,
            sprite=self.sprite,
        )

    def bonus_summary(self) -> str:
        parts = []
        if self.hp_bonus:      parts.append(f"+{self.hp_bonus} HP")
        if self.atk_bonus:     parts.append(f"+{self.atk_bonus} ATK")
        if self.defense_bonus: parts.append(f"+{self.defense_bonus} DEF")
        if self.speed_bonus:   parts.append(f"+{self.speed_bonus} VEL")
        if self.mana_bonus:    parts.append(f"+{self.mana_bonus} Mana")
        return ", ".join(parts) if parts else "sem bonus"

    def __str__(self) -> str:
        return (
            f"{self.rarity.color_tag()} [{self.slot.value}] {self.name} "
            f"({self.bonus_summary()}) {self.rarity.stars()}"
        )
