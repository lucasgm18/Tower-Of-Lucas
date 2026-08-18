from dataclasses import dataclass, field
from core.items import Item, ItemSlot
from core.stats import Stats


@dataclass
class Inventory:
    _equipped: dict[ItemSlot, Item] = field(default_factory=dict)

    @classmethod
    def empty(cls) -> "Inventory":
        return cls(_equipped={})

    def equip(self, item: Item) -> "Inventory":
        new_equipped = dict(self._equipped)
        new_equipped[item.slot] = item
        return Inventory(_equipped=new_equipped)

    def unequip(self, slot: ItemSlot) -> "Inventory":
        return Inventory(_equipped={k: v for k, v in self._equipped.items() if k != slot})

    def item_in(self, slot: ItemSlot) -> Item | None:
        return self._equipped.get(slot)

    def apply_bonuses(self, base: Stats) -> Stats:
        result = base
        for item in self._equipped.values():
            result = result.apply_bonus(
                hp=item.hp_bonus,
                atk=item.atk_bonus,
                defense=item.defense_bonus,
                speed=item.speed_bonus,
            )
        return result

    def all_items(self) -> list[Item]:
        return list(self._equipped.values())

    def is_empty(self) -> bool:
        return len(self._equipped) == 0

    def __str__(self) -> str:
        if self.is_empty():
            return "Inventario vazio."
        return "\n".join(str(item) for item in self._equipped.values())
