from dataclasses import dataclass


@dataclass
class Stats:
    hp: int
    max_hp: int
    atk: int
    defense: int
    speed: int

    @classmethod
    def create(cls, hp: int, atk: int, defense: int, speed: int) -> "Stats":
        return cls(hp=hp, max_hp=hp, atk=atk, defense=defense, speed=speed)

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> "Stats":
        new_hp = max(0, self.hp - amount)
        return Stats(hp=new_hp, max_hp=self.max_hp, atk=self.atk, defense=self.defense, speed=self.speed)

    def heal(self, amount: int) -> "Stats":
        new_hp = min(self.max_hp, self.hp + amount)
        return Stats(hp=new_hp, max_hp=self.max_hp, atk=self.atk, defense=self.defense, speed=self.speed)

    def apply_bonus(self, hp: int = 0, atk: int = 0, defense: int = 0, speed: int = 0) -> "Stats":
        new_max = self.max_hp + hp
        return Stats(
            hp=self.hp + hp,
            max_hp=new_max,
            atk=self.atk + atk,
            defense=self.defense + defense,
            speed=self.speed + speed,
        )

    def __str__(self) -> str:
        return f"HP {self.hp}/{self.max_hp} | ATK {self.atk} | DEF {self.defense} | VEL {self.speed}"
