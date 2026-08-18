from dataclasses import dataclass


@dataclass
class ExperienceSystem:
    current_exp: int
    level: int

    @classmethod
    def new(cls) -> "ExperienceSystem":
        return cls(current_exp=0, level=1)

    def exp_needed_for_next_level(self) -> int:
        return self.level * 100

    def add_exp(self, amount: int) -> tuple["ExperienceSystem", int]:
        new_exp = self.current_exp + amount
        levels_gained = 0
        level = self.level
        while new_exp >= level * 100:
            new_exp -= level * 100
            level += 1
            levels_gained += 1
        return ExperienceSystem(current_exp=new_exp, level=level), levels_gained

    def __str__(self) -> str:
        return f"Nivel {self.level} | EXP {self.current_exp}/{self.exp_needed_for_next_level()}"
