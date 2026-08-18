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
            Rarity.RARE:     "[AZUL]",
            Rarity.EPIC:     "[ROXO]",
        }
        return colors[self]

    def stars(self) -> str:
        stars = {
            Rarity.COMMON:   "*",
            Rarity.UNCOMMON: "**",
            Rarity.RARE:     "***",
            Rarity.EPIC:     "****",
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
    sprite: str = ""  # nome do arquivo PNG, ex: "espada_madeira.png"

    def bonus_summary(self) -> str:
        parts = []
        if self.hp_bonus:      parts.append(f"+{self.hp_bonus} HP")
        if self.atk_bonus:     parts.append(f"+{self.atk_bonus} ATK")
        if self.defense_bonus: parts.append(f"+{self.defense_bonus} DEF")
        if self.speed_bonus:   parts.append(f"+{self.speed_bonus} VEL")
        return ", ".join(parts) if parts else "sem bonus"

    def __str__(self) -> str:
        return (
            f"{self.rarity.color_tag()} [{self.slot.value}] {self.name} "
            f"({self.bonus_summary()}) {self.rarity.stars()}"
        )
