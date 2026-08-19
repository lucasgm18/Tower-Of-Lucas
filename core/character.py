from dataclasses import dataclass
from core.stats import Stats
from core.exp import ExperienceSystem
from core.inventory import Inventory
from core.mana_pool import ManaPool
from core.skill_cooldowns import SkillCooldowns
from core.gold import Gold
from data.classes import CharacterClass
from data.races import Race


@dataclass
class Character:
    name: str
    character_class: CharacterClass
    race: Race
    base_stats: Stats
    mana_pool: ManaPool
    exp_system: ExperienceSystem
    inventory: Inventory
    current_floor: int
    cooldowns: SkillCooldowns
    gold: Gold = None  # type: ignore

    def __post_init__(self) -> None:
        if self.gold is None:
            object.__setattr__(self, "gold", Gold.zero())

    @classmethod
    def create(cls, name: str, character_class: CharacterClass, race: Race) -> "Character":
        base = Stats.create(
            hp=character_class.base_hp,
            atk=character_class.base_atk,
            defense=character_class.base_defense,
            speed=character_class.base_speed,
        )
        final_stats, final_mana = race.apply_to(base, character_class.base_mana)
        mana_pool = ManaPool.full(final_mana) if final_mana > 0 else ManaPool.empty()
        return cls(
            name=name,
            character_class=character_class,
            race=race,
            base_stats=final_stats,
            mana_pool=mana_pool,
            exp_system=ExperienceSystem.new(),
            inventory=Inventory.empty(),
            current_floor=1,
            cooldowns=SkillCooldowns.from_skills(character_class.skills),
            gold=Gold.zero(),
        )

    def effective_stats(self) -> Stats:
        return self.inventory.apply_bonuses(self.base_stats)

    def effective_mana_pool(self) -> ManaPool:
        return self.inventory.apply_mana_bonus(self.mana_pool)

    def is_alive(self) -> bool:
        return self.base_stats.is_alive()

    def has_mana(self, cost: int) -> bool:
        return self.mana_pool.has(cost)

    def spend_mana(self, cost: int) -> "Character":
        return self._with(mana_pool=self.mana_pool.spend(cost))

    def restore_mana(self, amount: int) -> "Character":
        return self._with(mana_pool=self.mana_pool.restore(amount))

    def take_damage(self, amount: int) -> "Character":
        return self._with(base_stats=self.base_stats.take_damage(amount))

    def heal(self, amount: int) -> "Character":
        return self._with(base_stats=self.base_stats.heal(amount))

    def earn_gold(self, amount: int) -> "Character":
        return self._with(gold=self.gold.earn(amount))

    def spend_gold(self, cost: int) -> "Character":
        return self._with(gold=self.gold.spend(cost))

    def gain_exp(self, amount: int) -> "tuple[Character, int]":
        new_exp_system, levels_gained = self.exp_system.add_exp(amount)
        new_stats = self.base_stats
        new_mana_pool = self.mana_pool
        for _ in range(levels_gained):
            new_stats = new_stats.apply_bonus(hp=5, atk=1, defense=1, speed=0)
            new_mana_pool = new_mana_pool.expand(5)
        return self._with(
            base_stats=new_stats,
            exp_system=new_exp_system,
            mana_pool=new_mana_pool,
        ), levels_gained

    def equip(self, item) -> "Character":
        return self._with(inventory=self.inventory.equip(item))

    def advance_floor(self) -> "Character":
        return self._with(current_floor=self.current_floor + 1)

    def tick_cooldowns(self) -> "Character":
        return self._with(cooldowns=self.cooldowns.tick())

    def use_skill(self, skill_name: str) -> "Character":
        skill = next((s for s in self.character_class.skills if s.name == skill_name), None)
        if skill is None:
            return self
        return self._with(cooldowns=self.cooldowns.set_cooldown(skill_name, skill.cooldown))

    def skill_is_ready(self, skill_name: str) -> bool:
        return self.cooldowns.is_ready(skill_name)

    def _with(self, **kwargs) -> "Character":
        return Character(
            name=kwargs.get("name", self.name),
            character_class=kwargs.get("character_class", self.character_class),
            race=kwargs.get("race", self.race),
            base_stats=kwargs.get("base_stats", self.base_stats),
            mana_pool=kwargs.get("mana_pool", self.mana_pool),
            exp_system=kwargs.get("exp_system", self.exp_system),
            inventory=kwargs.get("inventory", self.inventory),
            current_floor=kwargs.get("current_floor", self.current_floor),
            cooldowns=kwargs.get("cooldowns", self.cooldowns),
            gold=kwargs.get("gold", self.gold),
        )

    def summary(self) -> str:
        stats = self.effective_stats()
        eff_mana = self.effective_mana_pool()
        mana_line = f"  {eff_mana}\n" if not eff_mana.is_empty() else ""
        items = self.inventory.all_items()
        inv_section = ""
        if items:
            inv_section = "\n  Equipamentos:\n" + "\n".join(f"    {i}" for i in items)
        return (
            f"  {self.name}  |  {self.character_class.name} {self.race.name}\n"
            f"  {self.exp_system}\n"
            f"  {stats}\n"
            f"{mana_line}"
            f"  Andar: {self.current_floor}  |  {self.gold}"
            f"{inv_section}"
        )
