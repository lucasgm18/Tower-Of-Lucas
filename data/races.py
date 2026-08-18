from dataclasses import dataclass
from core.stats import Stats


@dataclass(frozen=True)
class Race:
    name: str
    hp_bonus: int
    atk_bonus: int
    defense_bonus: int
    speed_bonus: int
    mana_bonus: int
    description: str

    def apply_to(self, base: Stats, base_mana: int) -> tuple[Stats, int]:
        new_stats = base.apply_bonus(
            hp=self.hp_bonus,
            atk=self.atk_bonus,
            defense=self.defense_bonus,
            speed=self.speed_bonus,
        )
        return new_stats, max(0, base_mana + self.mana_bonus)

    def __str__(self) -> str:
        return f"{self.name} — {self.description}"


HUMAN = Race(
    name="Humano",
    hp_bonus=0,
    atk_bonus=0,
    defense_bonus=1,
    speed_bonus=2,
    mana_bonus=5,
    description="Equilibrado e veloz. Bonus de DEF, VEL e Mana.",
)

ORC = Race(
    name="Orc",
    hp_bonus=15,
    atk_bonus=2,
    defense_bonus=-1,
    speed_bonus=-2,
    mana_bonus=-10,
    description="Bruto e resistente. Bonus de HP e ATK, penalidade em DEF, VEL e Mana.",
)

ALL_RACES: dict[str, Race] = {
    HUMAN.name: HUMAN,
    ORC.name: ORC,
}
