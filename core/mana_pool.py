from dataclasses import dataclass


@dataclass(frozen=True)
class ManaPool:
    current: int
    maximum: int

    @classmethod
    def empty(cls) -> "ManaPool":
        return cls(current=0, maximum=0)

    @classmethod
    def full(cls, capacity: int) -> "ManaPool":
        return cls(current=capacity, maximum=capacity)

    def has(self, amount: int) -> bool:
        return self.current >= amount

    def spend(self, amount: int) -> "ManaPool":
        return ManaPool(current=max(0, self.current - amount), maximum=self.maximum)

    def restore(self, amount: int) -> "ManaPool":
        return ManaPool(current=min(self.maximum, self.current + amount), maximum=self.maximum)

    def expand(self, amount: int) -> "ManaPool":
        new_maximum = self.maximum + amount
        return ManaPool(current=new_maximum, maximum=new_maximum)

    def is_empty(self) -> bool:
        return self.maximum == 0

    def __str__(self) -> str:
        return f"Mana: {self.current}/{self.maximum}"
