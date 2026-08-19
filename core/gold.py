from dataclasses import dataclass


@dataclass(frozen=True)
class Gold:
    amount: int = 0

    @classmethod
    def zero(cls) -> "Gold":
        return cls(amount=0)

    def earn(self, amount: int) -> "Gold":
        return Gold(amount=self.amount + amount)

    def spend(self, cost: int) -> "Gold":
        return Gold(amount=max(0, self.amount - cost))

    def can_afford(self, cost: int) -> bool:
        return self.amount >= cost

    def __str__(self) -> str:
        return f"{self.amount} ouro"
